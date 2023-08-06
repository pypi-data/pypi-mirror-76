from copy import deepcopy

import hyperchamber as hc
import numpy as np
import inspect
import torch
from torch.nn.parameter import Parameter
from torch.autograd import grad as torch_grad
import torch.nn as nn
from operator import itemgetter
from hypergan.train_hooks.base_train_hook import BaseTrainHook

class OnlineEWCTrainHook(BaseTrainHook):
  """ https://faculty.washington.edu/ratliffl/research/2019conjectures.pdf """
  def __init__(self, gan=None, config=None):
      super().__init__(config=config, gan=gan)
      self.d_loss = None
      self.g_loss = None
      self.gan = gan

      self.d_ewc_params = []
      self.d_ewc_fisher = []

      for p in self.gan.d_parameters():
          self.d_ewc_params += [Parameter(p, requires_grad=False)]
          self.d_ewc_fisher += [Parameter((self.config.initial_gamma or 1.0) * torch.rand(p.shape), requires_grad=False)]

      self.g_ewc_params = []
      self.g_ewc_fisher = []

      for p in self.gan.g_parameters():
          self.g_ewc_params += [Parameter(p, requires_grad=False)]
          self.g_ewc_fisher += [Parameter((self.config.initial_gamma or 1.0) * torch.rand(p.shape), requires_grad=False)]

      for i, (param, fisher) in enumerate(zip(self.d_ewc_params, self.d_ewc_fisher)):
          self.register_parameter('d_ewc'+str(i), param)
          self.register_parameter('d_fisher'+str(i), fisher)

      for i, (param, fisher) in enumerate(zip(self.g_ewc_params, self.g_ewc_fisher)):
          self.register_parameter('g_ewc'+str(i), param)
          self.register_parameter('g_fisher'+str(i), fisher)
      self.g_ewc_params = [e.cuda() for e in self.g_ewc_params]
      self.d_ewc_params = [e.cuda() for e in self.d_ewc_params]
      self.d_ewc_fisher = [e.cuda() for e in self.d_ewc_fisher]
      self.g_ewc_fisher = [e.cuda() for e in self.g_ewc_fisher]

      self.d_gamma = torch.Tensor([self.config.d_gamma or self.config.gamma]).float()[0].cuda()
      self.g_gamma = torch.Tensor([self.config.g_gamma or self.config.gamma]).float()[0].cuda()

      self.d_new_fisher_gamma = torch.Tensor([self.config.d_new_fisher_gamma or self.config.new_fisher_gamma or 1e4]).float()[0].cuda()
      self.g_new_fisher_gamma = torch.Tensor([self.config.g_new_fisher_gamma or self.config.new_fisher_gamma or 1e4]).float()[0].cuda()

      self.g_mean_decay = torch.Tensor([self.config.g_mean_decay or self.config.mean_decay]).float()[0].cuda()
      self.d_mean_decay = torch.Tensor([self.config.d_mean_decay or self.config.mean_decay]).float()[0].cuda()
      self.g_mean_decay_1m = torch.Tensor([1.0 - (self.config.g_mean_decay or self.config.mean_decay)]).float()[0].cuda()
      self.d_mean_decay_1m = torch.Tensor([1.0 - (self.config.d_mean_decay or self.config.mean_decay)]).float()[0].cuda()

      self.d_beta = torch.Tensor([self.config.d_beta or self.config.beta]).float()[0].cuda()
      self.g_beta = torch.Tensor([self.config.g_beta or self.config.beta]).float()[0].cuda()

      self.d_loss_start = torch.zeros(1).float()[0].cuda()
      self.g_loss_start = torch.zeros(1).float()[0].cuda()


  def forward(self, d_loss, g_loss):
      if self.config.skip_after_steps and self.config.skip_after_steps < self.gan.steps:
          return [None, None]

      self.d_loss = self.d_loss_start.clone()
      if d_loss is not None:
          d_loss = d_loss.mean()
          d_params = list(self.gan.d_parameters())
          d_grads = torch_grad(d_loss, d_params, create_graph=True, retain_graph=True)
          for i, (dp, dp_g) in enumerate(zip(d_params, d_grads)):
              res = self.d_beta * ((dp - self.d_ewc_params[i]) ** 2 * self.d_ewc_fisher[i]).sum()
              self.d_loss = self.d_loss + self.d_beta * ((dp - self.d_ewc_params[i]) ** 2 * self.d_ewc_fisher[i]).sum()
              with torch.no_grad():
                  self.d_ewc_fisher[i] = self.d_gamma * self.d_ewc_fisher[i] + self.d_new_fisher_gamma * dp_g**2
                  self.d_ewc_params[i] = self.d_mean_decay_1m * dp.clone() + self.d_mean_decay * self.d_ewc_params[i]
          self.gan.add_metric('ewc_d', self.d_loss)

      skip_g_after_steps = False
      if self.config.skip_g_after_steps:
          skip_g_after_steps = self.config.skip_g_after_steps < self.gan.steps
      skip_g = self.config.skip_g or skip_g_after_steps
      if skip_g:
          return [self.d_loss, None]

      self.g_loss = self.g_loss_start.clone()
      if g_loss is not None:
          g_loss = g_loss.mean()
          g_params = list(self.gan.g_parameters())
          g_grads = torch_grad(g_loss, g_params, create_graph=True, retain_graph=True)
          for i, (gp, gp_g) in enumerate(zip(g_params, g_grads)):
              self.g_loss += self.g_beta * ((gp - self.g_ewc_params[i]) ** 2 * self.g_ewc_fisher[i]).sum()
              with torch.no_grad():
                  self.g_ewc_fisher[i] = self.g_gamma * self.g_ewc_fisher[i] + self.g_new_fisher_gamma * gp_g**2
                  self.g_ewc_params[i] = self.g_mean_decay_1m * gp.clone() + self.g_mean_decay * self.g_ewc_params[i]
          self.gan.add_metric('ewc_g', self.g_loss)

      return [self.d_loss, self.g_loss]


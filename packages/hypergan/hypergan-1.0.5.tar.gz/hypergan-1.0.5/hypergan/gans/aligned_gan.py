from .base_gan import BaseGAN
from hyperchamber import Config
from hypergan.discriminators import *
from hypergan.distributions import *
from hypergan.gan_component import ValidationException, GANComponent
from hypergan.generators import *
from hypergan.inputs import *
from hypergan.samplers import *
from hypergan.trainers import *
import copy
import hyperchamber as hc
import hypergan as hg
import importlib
import json
import numpy as np
import os
import sys
import time
import torch
import uuid


class AlignedGAN(BaseGAN):
    """ 
    """
    def __init__(self, *args, **kwargs):
        BaseGAN.__init__(self, *args, **kwargs)

    def create(self):
        self.latent = self.create_component("latent")
        self.x = self.inputs.next()[0]
        self.generator = self.create_component("generator", input=self.x)
        self.discriminator = self.create_component("discriminator")
        self.loss = self.create_component("loss")
        self.trainer = self.create_component("trainer")

    def forward_discriminator(self, inputs):
        return self.discriminator(inputs[0])

    def forward_pass(self):
        self.x = self.inputs.next()
        self.y = self.inputs.next(1)
        self.latent.next()
        g = self.generator(self.x)
        self.g = g
        d_real = self.forward_discriminator([self.y])
        d_fake = self.forward_discriminator([self.g])
        self.d_fake = d_fake
        self.d_real = d_real
        return d_real, d_fake

    def discriminator_components(self):
        return [self.discriminator]

    def generator_components(self):
        return [self.generator]

    def discriminator_fake_inputs(self, discriminator_index=0):
        return [self.g]

    def discriminator_real_inputs(self, discriminator_index=0):
        if hasattr(self, 'y'):
            return [self.x]
        else:
            return [self.inputs.next()]

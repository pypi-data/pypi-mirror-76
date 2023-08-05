#From https://gist.github.com/EndingCredits/b5f35e84df10d46cfa716178d9c862a3
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import hyperchamber as hc
import numpy as np
import inspect
from operator import itemgetter
from hypergan.train_hooks.base_train_hook import BaseTrainHook

class RollingMemoryTrainHook(BaseTrainHook):
  "Keeps a rolling memory of the best scoring discriminator samples."
  def __init__(self, gan=None, config=None, trainer=None, name="RollingMemoryTrainHook"):
    super().__init__(config=config, gan=gan, trainer=trainer, name=name)
    config = hc.Config(config)
    s = self.gan.ops.shape(self.gan.generator.sample)
    self.shape = s#[self.gan.batch_size() * (self.config.memory_size or 1), s[1], s[2], s[3]]
    with tf.variable_scope((self.config.name or self.name), reuse=self.gan.reuse) as scope:
        self.mx=tf.get_variable(self.gan.ops.generate_name()+"_dontsave", s, dtype=tf.float32,
                  initializer=tf.compat.v1.constant_initializer(-100), aggregation=tf.VariableAggregation.ONLY_FIRST_REPLICA, trainable=False)
        self.mg=tf.get_variable(self.gan.ops.generate_name()+"_dontsave", s, dtype=tf.float32,
                  initializer=tf.compat.v1.constant_initializer(100), aggregation=tf.VariableAggregation.ONLY_FIRST_REPLICA, trainable=False)
    self.m_discriminator = gan.create_component(gan.config.discriminator, name="discriminator", input=tf.concat([self.mx, self.mg],axis=0), features=[gan.features], reuse=True)
    self.m_loss = gan.create_component(gan.config.loss, discriminator=self.m_discriminator)
    swx = self.m_loss.d_real
    swg = self.m_loss.d_fake
    if self.config.reverse_mx:
        swx = -swx
    if self.config.reverse_mg:
        swg = -swg
    swx = tf.reshape(swx, [-1])
    swg = tf.reshape(swg, [-1])
    _, swx = tf.nn.top_k(swx, k=(self.config.top_k or 1), sorted=True, name=None)
    _, swg = tf.nn.top_k(swg, k=(self.config.top_k or 1), sorted=True, name=None)
    swx = tf.one_hot(swx, self.gan.batch_size(), dtype=tf.float32)
    swg = tf.one_hot(swg, self.gan.batch_size(), dtype=tf.float32)
    swx = tf.reduce_sum(swx, reduction_indices=0)
    swg = tf.reduce_sum(swg, reduction_indices=0)
    swx = tf.reshape(swx, [self.gan.batch_size(), 1, 1, 1])
    swg = tf.reshape(swg, [self.gan.batch_size(), 1, 1, 1])
    self.swx = swx
    self.swg = swg
    self.assign_mx = tf.assign(self.mx, self.gan.inputs.x * swx + (1.0 - swx) * self.mx)
    self.assign_mg = tf.assign(self.mg, self.gan.generator.sample * swg + (1.0 - swg) * self.mg)
    self.assign_ops = tf.group(*[self.assign_mx, self.assign_mg])
    self.train_hook_index = len(trainer.train_hooks)
    self.loss = [tf.zeros(1), tf.zeros(1)]
    for _type in self.config.types or ['mx/mg']:
        if _type == 'mg/g':
            self.mg_discriminator = gan.create_component(gan.config.discriminator, name="discriminator", input=tf.concat([self.mg, self.gan.generator.sample],axis=0), features=[gan.features], reuse=True)
            self.mg_loss = gan.create_component(gan.config.loss, discriminator=self.mg_discriminator)
            self.gan.losses += [self.mg_loss]
            self.loss[0] += (self.config.lam or 1.0) * self.mg_loss.sample[0]
            self.loss[1] += (self.config.lam or 1.0) * self.mg_loss.sample[1]
            self.gan.add_metric('roll_loss_mg/g', self.loss[0])
        elif _type == 'mx/mg': 
            self.loss[0] += (self.config.lam or 1.0) * self.m_loss.sample[0]
            self.loss[1] += (self.config.lam or 1.0) * self.m_loss.sample[1]
            self.gan.add_metric('roll_loss_mx/mg', self.loss[0])
        elif _type == 'mx/g': 
            self.mg_discriminator = gan.create_component(gan.config.discriminator, name="discriminator", input=tf.concat([self.mx, self.gan.generator.sample],axis=0), features=[gan.features], reuse=True)
            self.mg_loss = gan.create_component(gan.config.loss, discriminator=self.mg_discriminator)
            self.loss[0] += (self.config.lam or 1.0) * self.mg_loss.sample[0]
            self.loss[1] += (self.config.lam or 1.0) * self.mg_loss.sample[1]
            self.gan.add_metric('roll_loss_mx/g', self.loss[0])
        elif _type == 'x/mg': 
            self.mg_discriminator = gan.create_component(gan.config.discriminator, name="discriminator", input=tf.concat([self.gan.inputs.x, self.mg],axis=0), features=[gan.features], reuse=True)
            self.mg_loss = gan.create_component(gan.config.loss, discriminator=self.mg_discriminator)
            self.loss[0] += (self.config.lam or 1.0) * self.mg_loss.sample[0]
            self.loss[1] += (self.config.lam or 1.0) * self.mg_loss.sample[1]
            self.gan.add_metric('roll_loss_x/mg', self.loss[0])
        elif _type == 'x/mx': 
            self.mg_discriminator = gan.create_component(gan.config.discriminator, name="discriminator", input=tf.concat([self.mg, self.gan.generator.sample],axis=0), features=[gan.features], reuse=True)
            self.mg_loss = gan.create_component(gan.config.loss, discriminator=self.mg_discriminator)
            self.loss[0] += (self.config.lam or 1.0) * self.mg_loss.sample[0]
            self.loss[1] += (self.config.lam or 1.0) * self.mg_loss.sample[1]
            self.gan.add_metric('roll_loss_x/mx', self.loss[0])


  def distributed_step(self, input_iterator_next):
    def assign_mx(mx, inp, swx):
        inp2 = self.gan.replica.inputs.x
        op=self.gan.replica.trainer.train_hooks[self.train_hook_index].assign_mx
        with tf.control_dependencies([op]):
            return tf.no_op()
    def assign_mg(mg, gen, swg):
        op = self.gan.replica.trainer.train_hooks[self.train_hook_index].assign_mg
        with tf.control_dependencies([op]):
            return tf.no_op()
    mxop = self.gan.distribution_strategy.extended.call_for_each_replica(assign_mx, args=(self.mx, input_iterator_next, self.swx,))
    mgop = self.gan.distribution_strategy.extended.call_for_each_replica(assign_mg, args=(self.mg, self.gan.generator.sample, self.swg,))

    return [mxop, mgop]

  def distributed_debug(self):
    mxop = self.gan.distribution_strategy.extended.read_var(self.mx)
    mgop = self.gan.distribution_strategy.extended.read_var(self.mg)

    return [mxop, mgop]

  def distributed_initial_step(self, input_iterator_next):
    def assign_mx(mx, inp):
        return mx.assign(inp)

    def assign_mg(mg, gen):
        return mg.assign(gen)

    mxop = self.gan.distribution_strategy.extended.call_for_each_replica(assign_mx, args=(self.mx,input_iterator_next,))
    mgop = self.gan.distribution_strategy.extended.call_for_each_replica(assign_mg, args=(self.mg,self.gan.generator.sample,))
    return [mxop, mgop]


  def before_step(self, step, feed_dict):
      if step == 0:
          self.gan.session.run(tf.assign(self.mx, self.gan.inputs.x))
          self.gan.session.run(tf.assign(self.mg, self.gan.generator.sample))

  def after_step(self, step, feed_dict):
      self.gan.session.run(self.assign_ops)

  def variables(self):
      return [self.mx, self.mg]

  def losses(self):
    return self.loss

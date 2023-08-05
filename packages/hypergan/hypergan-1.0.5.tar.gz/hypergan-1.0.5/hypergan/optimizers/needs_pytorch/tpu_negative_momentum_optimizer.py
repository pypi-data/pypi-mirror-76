from tensorflow.python.framework import ops
from tensorflow.python.ops import control_flow_ops
from tensorflow.python.ops import math_ops
from tensorflow.python.ops import resource_variable_ops
from tensorflow.python.ops import state_ops
from tensorflow.python.ops import variable_scope
from tensorflow.python.training import optimizer


class TPUNegativeMomentumOptimizer(optimizer.Optimizer):
    def __init__(self, learning_rate=1.0, decay=1.0, gan=None, config=None, use_locking=False, name="TPUNegativeMomentumOptimizer", optimizer=None):
        super(TPUNegativeMomentumOptimizer, self).__init__(use_locking, name)
        self._decay = decay
        self.gan = gan
        self.config = config
        self.name = name
        self.optimizer = self.gan.create_optimizer(optimizer)

    def _prepare(self):
        self.optimizer._prepare()

    def _create_slots(self, var_list):
        super(TPUNegativeMomentumOptimizer, self)._create_slots(var_list)
        self.optimizer._create_slots(var_list)
        for v in var_list :
            self._zeros_slot(v, "nm", self._name)

    def _apply_dense(self, grad, var):
      nm = self.get_slot(var, "nm")
      new_val = grad - nm
      var_update = self.optimizer._apply_dense(new_val, var)
      with tf.control_dependencies([var_update]):
          save = tf.assign(nm, ((self.config.alpha or 0.666) *grad+ (1-self.config.beta or 0.5)*nm))
          return save

    def _resource_apply_dense(self, grad, var):
      grad = tf.to_float(grad)
      nm = self.get_slot(var, "nm")
      new_val = grad - nm
      var_update = self.optimizer._resource_apply_dense(new_val, var)
      with tf.control_dependencies([var_update]):
          save = tf.assign(nm, ((self.config.alpha or 0.666) *grad+ (1-self.config.beta or 0.5)*nm))
          return save

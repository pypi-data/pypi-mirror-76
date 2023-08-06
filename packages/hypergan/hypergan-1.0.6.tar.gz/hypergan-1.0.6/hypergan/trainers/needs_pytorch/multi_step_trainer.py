import numpy as np
import hyperchamber as hc
import inspect

from hypergan.trainers.base_trainer import BaseTrainer

TINY = 1e-12

class MultiStepTrainer(BaseTrainer):
    def __init__(self, gan, config, losses=[], var_lists=[], metrics=None):
        self.losses = losses
        self.var_lists = var_lists
        self.metrics = metrics or [None for i in self.losses]
        BaseTrainer.__init__(self, gan, config)

    def _create(self):
        gan = self.gan
        config = self.config
        losses = self.losses

        optimizers = []
        for i, _ in enumerate(losses):
            loss = losses[i][1]
            var_list = self.var_lists[i]
            is_generator = 'generator' in losses[i][0]

            if is_generator:
                optimizer = self.build_optimizer(config, 'g_', config.g_trainer, self.g_lr, var_list, loss)
            else:
                optimizer = self.build_optimizer(config, 'd_', config.d_trainer, self.d_lr, var_list, loss)
            optimizers.append(optimizer)

        self.optimizers = optimizers


        if config.d_clipped_weights:
            self.clip = [tf.assign(d,tf.clip_by_value(d, -config.d_clipped_weights, config.d_clipped_weights))  for d in d_vars]
        else:
            self.clip = []

        return None

    def _step(self, feed_dict):
        gan = self.gan
        sess = gan.session
        config = self.config
        losses = self.losses
        metrics = self.metrics

        for i, _ in enumerate(losses):
            loss = losses[i]
            optimizer = self.optimizers[i]
            metric = metrics[i]
            if(metric):
                metric_values = sess.run([optimizer] + self.output_variables(metric), feed_dict)[1:]

                if self.current_step % 100 == 0:
                    print("loss " + str(i) + "  "+ loss[0] + " " + self.output_string(metric) % tuple([self.current_step] + metric_values))
            else:
                _ = sess.run(optimizer, feed_dict)

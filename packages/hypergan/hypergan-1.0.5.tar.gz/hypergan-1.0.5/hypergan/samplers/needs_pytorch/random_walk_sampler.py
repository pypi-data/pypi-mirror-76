from hypergan.samplers.base_sampler import BaseSampler
import numpy as np

class RandomWalkSampler(BaseSampler):
    def __init__(self, gan, samples_per_row=8):
        BaseSampler.__init__(self, gan, samples_per_row)
        self.z = None
        self.y = None
        self.x = None
        self.step = 0
        self.steps = 30
        self.target = None

    def _sample(self):
        gan = self.gan
        z_t = gan.latent.sample
        inputs_t = gan.inputs.x

        if self.z is None:
            gan.session.run(gan.set_x)
            self.z = gan.latent.sample.eval()
            self.target = gan.latent.sample.eval()
            self.input = gan.session.run(gan.inputs.x)

        if self.step % self.steps == 0:
            self.z = self.target
            self.target = gan.latent.sample.eval()

        percent = float(self.step % self.steps)/self.steps
        z_interp = self.z*(1.0-percent) + self.target*percent
        self.step+=1
        if self.step % 360 == 0:
            gan.session.run(gan.set_x)
            self.input = gan.session.run(gan.inputs.x)
        output = gan.session.run(gan.generator.sample, feed_dict={z_t: z_interp, inputs_t: self.input})
        g=tf.get_default_graph()
        with g.as_default():
            tf.set_random_seed(1)
            return {
                'generator': output
            }


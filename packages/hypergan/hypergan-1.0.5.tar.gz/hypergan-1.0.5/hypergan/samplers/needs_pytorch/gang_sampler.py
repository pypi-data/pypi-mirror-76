from hypergan.samplers.base_sampler import BaseSampler

from hypergan.samplers.began_sampler import BeganSampler
from hypergan.samplers.batch_sampler import BatchSampler
from hypergan.samplers.static_batch_sampler import StaticBatchSampler
from hypergan.samplers.random_walk_sampler import RandomWalkSampler
from hypergan.samplers.segment_sampler import SegmentSampler
from hypergan.trainers.gang_trainer import GangTrainer
import numpy as np
import hypergan as hg

class GangSampler(BaseSampler):
    def __init__(self, gan, samples_per_row=8):
        BaseSampler.__init__(self, gan, samples_per_row=samples_per_row)
        self.xs = None
        self.samples = 1

    def compatible_with(gan):
        return isinstance(gan.trainer, GangTrainer)

    def sample(self, path, sample_to_file):
        gan = self.gan

        sess = gan.session
        config = gan.config
        if self.xs is None:
            self.xs = [sess.run([gan.inputs.x, gan.latent.sample]) for i in range(self.samples)]

        current_g = sess.run(gan.trainer.all_g_vars)
        
        stacks = []
        def _samples():
            n = 1
            cs = []
            for i in range(self.samples):
                ts = [gan.inputs.x, gan.latent.z]
                vs = self.xs[i]
                feed_dict = {}
                for t,v in zip(ts, vs):
                    feed_dict[t]=v
                cs.append(sess.run(gan.generator.sample,feed_dict))
                #cs.append(sess.run(gan.autoencoded_x,feed_dict))
            return np.vstack(cs)

        stacks.append(_samples())
        for sg in gan.trainer.sgs:
            gan.trainer.assign_g(sg)
            stacks.append(_samples())
        for i in range((gan.trainer.config.nash_memory_size or 10) - len(stacks)+1):
            stacks.append(_samples())

        gan.trainer.assign_g(current_g)

        images = np.vstack([np.hstack(s) for s in stacks])

        self.plot(images, path, sample_to_file)
        return [{'image': path, 'label': 'tiled x sample'}]

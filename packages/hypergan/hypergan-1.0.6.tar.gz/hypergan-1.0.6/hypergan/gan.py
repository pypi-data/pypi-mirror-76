from hypergan.gans.standard_gan import StandardGAN
from hypergan.gan_component import GANComponent

def gan_factory(*args, **kw_args):
    if 'config' in kw_args:
        config = kw_args['config']
    elif len(args) > 0:
        config = args[0]
    else:
        config = None
    if config and 'class' in config:
        return GANComponent.lookup_function(None, config['class'])(*args, **kw_args)
    else:
        return StandardGAN(*args, **kw_args)

GAN=gan_factory

"""
Various layer definitions are defined here. The difference between layers and modules are that layers:
    * Have an input and output size
    * Have a standard interface
    * Use parsed arguments from the configurable component
    * Are attached to a Component
"""
from os.path import dirname, basename, isfile
import glob
modules = glob.glob(dirname(__file__)+"/*.py")
__all__ = [ basename(f)[:-3] for f in modules if isfile(f)]

from .operation import Operation
from .add import Add
from .cat import Cat
from .mul import Mul
from .ez_norm import EzNorm
from .layer import Layer
from .residual import Residual
from .channel_attention import ChannelAttention
from .pixel_shuffle import PixelShuffle
from .upsample import Upsample
from .resizable_stack import ResizableStack
from .multi_head_attention import MultiHeadAttention
from .segment_softmax import SegmentSoftmax

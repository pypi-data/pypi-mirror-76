from . import version
from .op_dict import merge
from .op_dict import remove
from .op_sys import size
from .op_str import find


__version__ = version.VERSION

__all__ = [
    "version",
    "merge",
    "remove",
    "size",
    "find"
]

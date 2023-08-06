# -*- coding: utf-8 -*-

__version__ = "0.0.7"


def version():
    return __version__

from .core import Node
from .identity import NodeID 
from .log import log

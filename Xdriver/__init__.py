from typing import Literal
__dtype__ = Literal['Vision2D']
__task__ = Literal['ObjectDetection']
__format__ = Literal['YOLOv8']

from Xdriver.engine import MongoDB, Plugins
from Xdriver.cfg import Driver

__all__ = "MongoDB", "Plugins", "Driver"

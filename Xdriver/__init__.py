from typing import Literal

__dtype__ = Literal['Vision2D']
__task__ = Literal['ImageClassification', 'ObjectDetection', 'SemanticSegmentation']

from Xdriver.engine import MongoDB, Plugins

__all__ = "MongoDB", "Plugins"
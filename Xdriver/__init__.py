from typing import Literal

__version__ = "0.0"
__dtype__ = Literal['Vision2D']
__task__ = Literal['ImageClassification', 'ObjectDetection', 'SemanticSegmentation']


from Xdriver.engine import MongoDB, Models

__all__ = "MongoDB", "Models"
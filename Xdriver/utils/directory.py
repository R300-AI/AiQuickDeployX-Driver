import os, shutil
from pathlib import Path

class YOLOv8_Builder():
    def __init__(self, user, dtype, task):
        self.dtype = dtype
        self.task = task
        
    def make(self, dir):
        if self.dtype == 'Vision2D':
            if self.task == 'ObjectDetection':
                dir = Path(dir)
                if dir.exists():
                    shutil.rmtree(dir)
                dir.mkdir(parents=True, exist_ok=True)
                for i in ['train', 'valid', 'test']:
                    os.makedirs(os.path.join(dir, i)); os.makedirs(os.path.join(dir, i + "/images")); os.makedirs(os.path.join(dir, i + "/labels"))
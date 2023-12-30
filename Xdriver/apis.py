from roboflow import Roboflow
from pathlib import Path
import os, yaml

class Roboflow_APIs():
    def __init__(self, dtype, task):
        self.dtype = dtype
        self.task = task

    def Download(self, path, user, dataset):
        print(path, user, dataset)
        if self.dtype == 'Vision2D':
            if self.task == 'ObjectDetection':
                rf = Roboflow(api_key="FwJ74nDll40feRx99ICJ")
                project = rf.workspace("itri-1fpyr").project("hard-hat-sample-3ezzq")
                target_path = os.path.join(Path(path + '/data/datasets/' + user), dataset)
                project.version(1).download("yolov8", location=target_path)
                #補足不齊的資訊(這個資料必須包含：names, nc, features, train, test, val六種屬性)
                with open(target_path + '/data.yaml', 'r') as f:
                    data =yaml.safe_load(f)
                with open(target_path + '/data.yaml', 'w') as f:
                    data['features'] = ["class", "x_center", "y_center", "width", "height"]
                    yaml.dump(data, f)
                    
        print('【Roboflow APIs】{dtype}/{task} dataset downloaded to {target_path}.'.format(dtype=self.dtype, task=self.task, target_path=target_path))
        return target_path
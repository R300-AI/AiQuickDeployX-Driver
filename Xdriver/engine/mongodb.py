from Xdriver.apis import Roboflow_APIs
from .uploaders import YOLOv8_Uploader
from .exporters import YOLOv8_Exporter

from pathlib import Path
import numpy as np
import Xdriver, pymongo, gridfs, os, yaml

class MongoDB():
    def __init__(self, hostname, port, user, password):
        self.client = pymongo.MongoClient("mongodb://{hostname}:{port}/".format(hostname=hostname, port=port),
                                          username=user,
                                          password=password)

    def Pull(self, dtype: Xdriver.__dtype__, task: Xdriver.__task__, engine=None, dataset=None, username=None):
        processor = YOLOv8_Exporter(self.client, dtype, task)
        processor.Download(dataset, engine, username)

    def Push(self, dtype: Xdriver.__dtype__, task: Xdriver.__task__, dataset_path=None, retrain_origin = False):
        processor = YOLOv8_Uploader(self.client, dtype, task)
        processor.Upload(dataset_path, retrain_origin)

    def Download_Samples(dtype: Xdriver.__dtype__, task: Xdriver.__task__, path=os.getcwd()) -> str:
        apis = Roboflow_APIs(dtype, task)
        target_path = apis.download(path)
        return target_path
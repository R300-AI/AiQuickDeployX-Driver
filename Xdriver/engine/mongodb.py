from Xdriver.apis import Roboflow_APIs
from Xdriver.cfg.driver import Driver
from .uploaders import YOLOv8_Uploader
from .exporters import YOLOv8_Exporter

from pathlib import Path
import numpy as np
import Xdriver, pymongo, gridfs, os, yaml

class MongoDB(Driver):
    def __init__(self, hostname, port, user, password):
        super().__init__()
        self.client = pymongo.MongoClient("mongodb://{hostname}:{port}/".format(hostname=hostname, port=port),
                                          username=user,
                                          password=password)
        self.__datasets__ = self.search_datasets()

    def search_datasets(self):
        datasets = {}
        print('【MongoDB】Existing Datasets:')
        for dataset in self.client['SystemInfo'].list_collection_names():
            result = self.client['SystemInfo'][dataset].find_one()
            datasets[dataset] = {"dtype": result['dtype'], "task": result['task']}
            print('  -', dataset, '(dtype:', datasets[dataset]['dtype'] ,'/task:', datasets[dataset]['task'], ')')
        return datasets
        
    def Pull(self, dataset=None, metadata=None):
        if dataset in self.__datasets__.keys():
            if self.__datasets__[dataset]['dtype'] == metadata["dtype"] and self.__datasets__[dataset]['task'] == metadata["task"]:
                processor = YOLOv8_Exporter(self.client, metadata["dtype"], metadata["task"])
                processor.Download(dataset, metadata["dataset_dir"], metadata["username"])
            else:
                print('Resources incompatble. Dataset(dtype:', self.__datasets__[dataset]['dtype'], '/task:', self.__datasets__[dataset]['task'], '), Module(dtype:', metadata['dtype'], '/task:', metadata["task"], ')')
        else:
            print('Dataset', dataset, 'does not exist.')

    def Push(self, dtype: Xdriver.__dtype__, task: Xdriver.__task__, dataset_path=None, remain_folder = False):
        processor = YOLOv8_Uploader(self.client, dtype, task)
        processor.Upload(dataset_path, remain_folder)

    def Download_Samples(dtype: Xdriver.__dtype__, task: Xdriver.__task__) -> str:
        apis = Roboflow_APIs(dtype, task)
        target_path = apis.Download(os.getcwd())
        return target_path
from Xdriver.apis import Roboflow_APIs
from Xdriver.cfg.driver import Driver
from .uploaders import YOLOv8_Uploader
from .exporters import YOLOv8_Exporter

from pathlib import Path
import numpy as np
import Xdriver, pymongo, gridfs, os, yaml

class MongoDB(Driver):
    def __init__(self, user):
        super().__init__()
        self.client = pymongo.MongoClient("mongodb://{hostname}:{port}/".format(hostname='localhost', port='27017'),
                                          username='admin',
                                          password='admin')
        self.user = user

    def List_Datasets(self):
        datasets = {}
        print('【MongoDB】Existing Datasets:')
        for dataset in self.client['SystemInfo'].list_collection_names():
            result = self.client['SystemInfo'][dataset].find_one()
            if result['user'] == self.user:
                datasets[dataset] = {"dtype": result['dtype'], "task": result['task']}
                print('  -', dataset, '(dtype:', datasets[dataset]['dtype'] ,'/task:', datasets[dataset]['task'], ')')
        self.__datasets__ = datasets
        return datasets

    def Remove(self, dataset, dtype: Xdriver.__dtype__, task: Xdriver.__task__):
        result = self.client['SystemInfo'][dataset].find_one()
        if result['user'] == self.user and result['dtype'] == dtype and result['task'] == task:
            if dataset + '.files' in self.client['Images'].list_collection_names():
                self.client['Images'][dataset + '.files'].drop(); 
            if dataset + '.chunks' in self.client['Images'].list_collection_names():  
                self.client['Images'][dataset + '.chunks'].drop()
            if dataset in self.client['Labels'].list_collection_names():
                self.client['Labels'][dataset].drop()
            if dataset in self.client['SystemInfo'].list_collection_names():
                self.client['SystemInfo'][dataset].drop()
        return self.List_Datasets()
        
    def Push(self, dataset, dtype: Xdriver.__dtype__, task: Xdriver.__task__):
        dataset_path = self.Download_Samples(dataset=dataset, dtype=dtype, task=task) #TODO: move Dataset to ./Xdriver/data/<user>/<dataset> by WebUI
        processor = YOLOv8_Uploader(self.client, self.user, dtype, task)
        processor.Upload(dataset_path)
        return self.List_Datasets()

    def Pull(self, dataset=None, metadata=None):
        if dataset in self.List_Datasets():
            if self.__datasets__[dataset]['dtype'] == metadata["dtype"] and self.__datasets__[dataset]['task'] == metadata["task"]:
                processor = YOLOv8_Exporter(self.client, metadata["dtype"], metadata["task"])
                processor.Download(dataset, metadata["dataset_dir"], metadata["username"])
            else:
                print('Resources incompatble. Dataset(dtype:', self.__datasets__[dataset]['dtype'], '/task:', self.__datasets__[dataset]['task'], '), Module(dtype:', metadata['dtype'], '/task:', metadata["task"], ')')
        else:
            print('Dataset', dataset, 'does not exist.')

    def Download_Samples(self, dataset, dtype: Xdriver.__dtype__, task: Xdriver.__task__) -> str:
        apis = Roboflow_APIs(dtype, task)
        target_path = apis.Download(os.getcwd(), self.user, dataset)
        return target_path
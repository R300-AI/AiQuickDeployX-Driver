import os, yaml, gridfs
from pathlib import Path
from Xdriver.utils.directory import YOLOv8_Builder

class YOLOv8_Exporter():
    def __init__(self, client, dtype, task):
        self.client, self.dtype, self.task = client, dtype, task
        self.valid_collections = []
        print('【YOLOv8_Exporter】Valid Collections(for {dtype}/{task}):'.format(dtype=self.dtype, task=self.task))
        for collection in self.client['SystemInfo'].list_collection_names():
            if len(list(self.client['SystemInfo'][collection].find({"dtype":self.dtype, "task": self.task}))) > 0:
                self.valid_collections.append(collection)
                print('  -', collection)

        self.engines_path = os.path.dirname(os.path.realpath(__file__)).replace('Xdriver\engine','models/{dtype}/{task}'.format(dtype=self.dtype, task=self.task))
        self.valid_engines = []
        print('【YOLOv8_Exporter】Valid Engines(for {dtype}/{task}):'.format(dtype=self.dtype, task=self.task))
        for framework in os.listdir(self.engines_path):
            for model in os.listdir(os.path.join(Path(self.engines_path), framework)):
                engine = '{framework}/{model}'.format(framework=framework, model=model)
                self.valid_engines.append(engine)
                print('  -', engine)
    
    def Download(self, dataset, engine, username) -> str:
        if dataset in self.valid_collections and engine in self.valid_engines:
            #Build Directory
            target_path = os.path.join(Path(self.engines_path), '{engine}/tmp/datasets/{username}/{dataset}'.format(engine=engine, username=username, dataset=dataset))
            processor = YOLOv8_Builder(self.dtype, self.task)
            processor.make(target_path)
            print(target_path)

            #Write Data
            if self.dtype == 'Vision2D':
                if self.task == 'ImageClassification':
                    print(self.task, 'not supported for YOLOv8_Exporter.Download() yet.')
                    pass

                elif self.task == 'ObjectDetection':
                    with open(target_path + '/data.yaml', 'w') as f:
                        data = self.client['SystemInfo'][dataset].find_one()
                        del data['_id']
                        data['train'], data['vaild'], data['val'] = 'train/images', 'vaild/images', 'val/images'
                        yaml.dump(data, f)
                    for file in self.client['Images'][dataset + '.files'].find():
                        filename, subset = file['filename'], file['subset']
                        with open(target_path + '/{subset}/images/{filename}'.format(subset=subset, filename=filename), 'wb') as f:
                            f.write(gridfs.GridFS(self.client['Images'], collection=dataset).get(file['_id']).read())

                        filename = filename.rstrip(filename.split('.')[-1]) + 'txt'
                        with open(target_path + '/{subset}/labels/{filename}'.format(subset=subset, filename=filename), 'w') as f:
                            labels = self.client['Labels'][dataset].find({"filename":file['filename']})
                            for label in labels:
                                f.write(f"{' '.join([str(label[i]) for i in data['features']])}\n")
                    print('Dataset', dataset, 'has been saved to', target_path)

                elif self.task == 'SemanticSegmentation':
                    print(self.task, 'not supported for YOLOv8_Exporter.Download() yet.')
                    pass
        else:
            target_path = ''
            print("【YOLOv8_Exporter】dataset '{dataset}' or engine '{engine}' isn't exist, lease check your configuration.".format(dataset=dataset, engine=engine))
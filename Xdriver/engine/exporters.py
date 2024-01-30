import os, yaml, gridfs
from pathlib import Path
from Xdriver.utils.directory import YOLOv8_Builder

class YOLOv8_Exporter():
    def __init__(self, client, dtype, task):
        self.client, self.dtype, self.task = client, dtype, task

    def Download(self, dataset, target_path, username) -> str:
        target_path = target_path + '/{dataset}'.format(dataset=dataset)
        print(self.dtype, self.task, username)
        processor = YOLOv8_Builder(self.dtype, self.task)
        processor.make(target_path)
        if self.dtype == 'Vision2D':
            if self.task == 'ObjectDetection':
                with open(target_path + '/data.yaml', 'w') as f:
                    data = self.client['SystemInfo'][dataset].find_one()
                    del data['_id']
                    data['train'], data['vaild'], data['val'] = 'train/images', 'vaild/images', 'val/images'
                    yaml.dump(data, f)
                for file in self.client['Images'][dataset + '.files'].find():
                    filename, subset = file['filename'], file['subset']
                    image_path = target_path + '/{subset}/images/{filename}'.format(subset=subset, filename=filename)
                    with open(image_path, 'wb') as f:
                        f.write(gridfs.GridFS(self.client['Images'], collection=dataset).get(file['_id']).read())
                    filename = filename.rstrip(filename.split('.')[-1]) + 'txt'
                    with open(target_path + '/{subset}/labels/{filename}'.format(subset=subset, filename=filename), 'w') as f:
                        labels = self.client['Labels'][dataset].find({"filename":file['filename']})
                        for label in labels:
                            f.write(f"{' '.join([str(label[i]) for i in data['features']])}\n")
                print('Dataset', dataset, 'has been saved to', target_path)
                return image_path

        else:
            target_path = ''
            print("【YOLOv8_Exporter】dataset '{dataset}' or engine '{engine}' isn't exist, lease check your configuration.".format(dataset=dataset, engine=engine))
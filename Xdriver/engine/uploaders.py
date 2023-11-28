from pathlib import Path
import numpy as np
import gridfs, os, yaml, subprocess, shutil

class YOLOv8_Uploader():
    def __init__(self, client, dtype, task):
        self.client, self.dtype, self.task = client, dtype, task
        pass

    def search_paired_files(self, image_names, label_names):
        paired_file = []
        for image in image_names:
            image_name = image.rstrip(image.split('.')[-1])
            for label in label_names:
                if image_name == label.rstrip(label.split('.')[-1]):
                    paired_file.append([image, label])
        return paired_file

    def Upload(self, dataset_path, retrain_origin):
        if self.dtype == 'Vision2D':
            if self.task == 'ImageClassification':
                print(self.task, 'not supported for YOLOv8_Uploader() yet.')
                pass

            elif self.task == 'ObjectDetection':
                if self.is_yolov8_format(dataset_path):
                    paired_samples = {}
                    flag = True
                    for subset in ['train', 'test', 'valid']:
                        image_path = os.path.join(Path(dataset_path), '{subset}/images'.format(subset=subset))
                        label_path = os.path.join(Path(dataset_path), '{subset}/labels'.format(subset=subset))
                        image_names, label_names = os.listdir(image_path), os.listdir(label_path)
                        paired_samples_temp = self.search_paired_files(image_names, label_names)
                        paired_samples[subset] = [[os.path.join(image_path, i[0]), os.path.join(label_path, i[1])] for i in paired_samples_temp]
                        print("【YOLOv8_Uploader】find ", len(paired_samples[subset]), 'paired {subset} samples.'.format(subset=subset))
                        if len(paired_samples[subset]) == 0:
                            flag = False
                    if flag == True:
                        print('【YOLOv8_Uploader】Samples Uploading...')
                        self.upload_samples(dataset_path, subset, paired_samples)
                        print('【YOLOv8_Uploader】Config SystemInfo...')
                        self.upload_systeminfo(dataset_path)

                        if retrain_origin == False and os.path.exists(dataset_path)==True:
                            shutil.rmtree(dataset_path)
                        print('【YOLOv8_Uploader】Finished.')
                    else:
                        print("【YOLOv8_Uploader】Paired samples insufficient, please varify your dataset.")

            elif self.task == 'SemanticSegmentation':
                print(self.task, 'not supported for Uploader() yet.')
                pass

    def is_yolov8_format(self, dataset_path):
        flag = True
        data_path = os.path.join(Path(dataset_path), 'data.yaml')
        if os.path.exists(data_path) == True:
            with open(dataset_path + '/data.yaml', 'r') as f:
                data =yaml.safe_load(f)
                for info in ['names', 'nc', 'features', 'train', 'test', 'val']:
                    if info not in data.keys():
                        print("【YOLOv8_Uploader】Attribute '", info, "'is not in data.yaml, please varify your dataset.")
                        flag = False
            for subset in ['train', 'test', 'valid']:
                subset_path = os.path.join(Path(dataset_path), '{subset}'.format(subset=subset))
                image_path = os.path.join(Path(dataset_path), '{subset}/images'.format(subset=subset))
                label_path = os.path.join(Path(dataset_path), '{subset}/labels'.format(subset=subset))
                if os.path.exists(subset_path) != True or os.path.exists(image_path) != True or os.path.exists(label_path) != True:
                    print("【YOLOv8_Uploader】Subset '", subset, "' directory is invalid, please varify your dataset.")
                    flag = False
        else:
            print("【YOLOv8_Uploader】data.yaml is not exist (", data_path, "), please varify your dataset.")
            flag = False
        return flag

    def upload_samples(self, dataset_path, subset, samples): 
        with open(os.path.join(Path(dataset_path), 'data.yaml'), 'r') as f:
            data =yaml.safe_load(f)
        dataset = dataset_path.replace('\\', '/').split('/')[-1].replace('/', '')
        
        #remove and initialize corelative collections in Images and Labels database
        if dataset + '.files' in self.client['Images'].list_collection_names():
            self.client['Images'][dataset + '.files'].drop(); 
        if dataset + '.chunks' in self.client['Images'].list_collection_names():  
            self.client['Images'][dataset + '.chunks'].drop()
        if dataset in self.client['Labels'].list_collection_names():
            self.client['Labels'][dataset].drop()
        for subset in samples:
            for image, label in samples[subset]:
                filename = image.replace('\\', '/').split('/')[-1]
                with open(label, 'rb') as labels:
                    for annotation in labels.readlines():
                        annotation = np.array(annotation.decode('utf-8').split(' ')).astype(float)
                        if len(annotation) != len(data['features']):
                            print("【Config_Samples】label's length and features is not competible, please check contents of the", label_path +'/' + label_name)
                            break
                        else:
                            items = {'filename': filename}
                            for i, feature in enumerate(data['features']):
                                items[feature] = annotation[i]
                            items['class'] = int(items['class'])
                            self.client['Labels'][dataset].insert_one(items)
                with open(image, 'rb') as image_file:
                    gridfs.GridFS(self.client['Images'], collection=dataset).put(image_file, filename=filename, subset=subset)
        
    def upload_systeminfo(self, dataset_path):
        with open(os.path.join(Path(dataset_path), 'data.yaml'), 'r') as f:
            data =yaml.safe_load(f)
        dataset = dataset_path.replace('\\', '/').split('/')[-1].replace('/', '')
        if dataset in self.client['SystemInfo'].list_collection_names():
            self.client['SystemInfo'][dataset].drop()
        pass
        info = {"dtype": self.dtype, "task": self.task, "nc": data['nc'], "names": data['names'], "features": data['features']}
        self.client['SystemInfo'][dataset].insert_one(info)

        print('\n【SUMMARY】')
        print('Dataset:', dataset)
        print('- Amount of Samples:',len(list(gridfs.GridFS(self.client['Images'], collection=dataset).find())))
        print('- Amount of Boxes:', self.client['Labels'][dataset].count_documents({}))
        print('finished.')


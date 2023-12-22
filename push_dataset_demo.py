import Xdriver
from Xdriver import MongoDB, Plugins

#下載範例資料集至本機的執行目錄
dataset_path = MongoDB.Download_Samples(dtype='Vision2D', task='ObjectDetection')

#將資料集寫入MongoDB，並以資料夾名稱(dataset_path)來命名資料集。*可於MongoDB中檢視
client = MongoDB('localhost', '27017', 'admin', 'admin')
client.Push(dtype='Vision2D', task='ObjectDetection', dataset_path=dataset_path)
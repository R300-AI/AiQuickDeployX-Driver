import Xdriver
from Xdriver import MongoDB, Models

print('Version:', Xdriver.__version__)
print('Valid dtype:', Xdriver.__dtype__)
print('Valid task:', Xdriver.__task__)

###############################################
# 【從Roboflow取得範例資料集】
# 需提供資料集的規格(dtype, task)與輸出路徑(path)
###############################################
dataset_path = MongoDB.Download_Samples(dtype='Vision2D', task='ObjectDetection', path= './data')

###############################################
# 【將指定的資料集寫入MongoDB】
# 需提供資料集的規格(dtype, task)與指定的資料集路徑(dataset_path)
# 寫入MongoDB後原檔會自動刪除(可用retrain_origin=True保留資料集路徑的原檔)
###############################################
dataset_path = 'data\HardHat'
client = MongoDB('localhost', '27017', 'admin', 'admin')
client.Push(dtype='Vision2D', task='ObjectDetection', dataset_path=dataset_path, retrain_origin = False)

###############################################
# 【從MongoDB取得特定資料集，並置於指定引擎的系統路徑(<engine>/tmp/datasets/...)】
# 需提供資料集的規格(dtype, task)，以及要執行訓練的引擎名稱(engine)與資料集名稱(dataset) 
# [!] dataset名稱需與MondoDB現存的Collection的名稱相符；engine名稱需與modelS現存的模型路徑相同
# 須提供使用者名稱(username)，以為其建構獨立的引擎環境
###############################################
client = MongoDB('localhost', '27017', 'admin', 'admin')
client.Pull(dtype='Vision2D', task='ObjectDetection', dataset='HardHat', engine='Pytorch/YOLOv8n', username='admin')

###############################################
# 【執行引擎環境(需先Pull好所要訓練的資料集)】
# 需提供資料集的規格(dtype, task)，以及欲執行訓練的引擎名稱(engine)
# 提供使用者名稱(username)與資料集名稱(dataset)以啟動環境，引擎的輸出會存放在引擎的暫存路徑output_path中。
###############################################
model = Models(dtype='Vision2D', task='ObjectDetection', engine='Pytorch/YOLOv8n')
output_path = model.run(dataset='HardHat', username='admin')
output_path = './models/Vision2D/ObjectDetection/Pytorch/YOLOv8n/tmp/outputs/admin/HardHat'
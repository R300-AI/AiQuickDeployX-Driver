import requests, json
"""
#取得dtype, task支援的選項
res = requests.post('http://localhost:5000/help').content
print('http://localhost:5000/help', 'OK')


#取得index的資訊
res = requests.post('http://localhost:5000/index').content
print('http://localhost:5000/index', 'OK')


#新增一個HardHat資料集 (直接從Roboflow下載新增)
data = json.dumps({'user': 'Markov', 'dataset': 'HardHat', 'dtype':'Vision2D', 'task':'ObjectDetection'})
res = json.loads(requests.post('http://localhost:5000/push', data=data, headers={'Content-Type': 'application/json'}).content)
print('http://localhost:5000/push', 'OK')


#新增一個HardHat1資料集後再移除
data = json.dumps({'user': 'Markov', 'dataset': 'HardHat1', 'dtype':'Vision2D', 'task':'ObjectDetection'})
res = json.loads(requests.post('http://localhost:5000/push', data=data, headers={'Content-Type': 'application/json'}).content)

data = json.dumps({'user': 'Markov', 'dataset': 'HardHat1', 'dtype':'Vision2D', 'task':'ObjectDetection'})
res = json.loads(requests.post('http://localhost:5000/remove', data=data, headers={'Content-Type': 'application/json'}).content)
print('http://localhost:5000/remove', 'OK')


#取得使用者可存取的資源清單
data = json.dumps({'user': 'Markov'})
res = json.loads(requests.post('http://localhost:5000/info', data=data, headers={'Content-Type': 'application/json'}).content)
print('datasets:', list(res['datasets'].keys()))
print('modules:', list(res['modules'].keys()))


#安裝模組(以URL, tag, local_folder來安裝模組)
data = json.dumps({'url': 'https://github.com/R300-AI/Tensorflow-YOLOv8m_det.git'})
res = json.loads(requests.post('http://localhost:5000/install', data=data, headers={'Content-Type': 'application/json'}).content)
print('http://localhost:5000/install (by url)', 'OK')

data = json.dumps({'tag': 'Pytorch-YOLOv8n_cls'})
res = json.loads(requests.post('http://localhost:5000/install', data=data, headers={'Content-Type': 'application/json'}).content)
print('http://localhost:5000/install (by tag)', 'OK')

data = json.dumps({'local': 'Pytorch-YOLOv8m_det'})
res = json.loads(requests.post('http://localhost:5000/install', data=data, headers={'Content-Type': 'application/json'}).content)
print('http://localhost:5000/install (by local)', 'OK')


#先新增Pytorch-YOLOv8m_det模組再刪除
data = json.dumps({'local': 'Pytorch-YOLOv8m_det'})
res = json.loads(requests.post('http://localhost:5000/install', data=data, headers={'Content-Type': 'application/json'}).content)

data = json.dumps({'module': 'Pytorch/YOLOv8m_det'})
res = json.loads(requests.post('http://localhost:5000/uninstall', data=data, headers={'Content-Type': 'application/json'}).content)
print('http://localhost:5000/uninstall', 'OK')
"""

#執行使用者指定的訓練過程
data = json.dumps({'user': 'Markov', 'dataset': 'HardHat', 'module':'Pytorch/YOLOv8n'})
res = json.loads(requests.post('http://localhost:5000/run', data=data, headers={'Content-Type': 'application/json'}).content)
print('http://localhost:5000/remove', 'OK')

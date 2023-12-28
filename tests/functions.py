import requests, json

#取得dtype, task支援的選項
res = requests.post('http://localhost:5000/help').content
print("Supported_Options: ", json.loads(res)['supported_options'])

#取得index的資訊
res = requests.post('http://localhost:5000/index').content
print("Module Resources: ", json.loads(res))


#上傳資料集(模擬)，dtype, task需依照help提供的選項填寫
data = json.dumps({'user': 'Markov', 'dataset': 'HardHat', 'dtype':'Vision2D', 'task':'ObjectDetection'})
res = json.loads(requests.post('http://localhost:5000/push', data=data, headers={'Content-Type': 'application/json'}).content)
print(res)

#先新增再刪除資料集，dtype, 可透過修改dataset名稱來創建不同資料集(但實際上是同一份資料集)
data = json.dumps({'user': 'Markov', 'dataset': 'HardHat1', 'dtype':'Vision2D', 'task':'ObjectDetection'})
res = json.loads(requests.post('http://localhost:5000/push', data=data, headers={'Content-Type': 'application/json'}).content)
print(res)

data = json.dumps({'user': 'Markov', 'dataset': 'HardHat1', 'dtype':'Vision2D', 'task':'ObjectDetection'})
res = json.loads(requests.post('http://localhost:5000/remove', data=data, headers={'Content-Type': 'application/json'}).content)
print(res)


#取得使用者可存取的資源清單
data = json.dumps({'user': 'Markov'})
res = json.loads(requests.post('http://localhost:5000/info', data=data, headers={'Content-Type': 'application/json'}).content)
print('datasets:', list(res['datasets'].keys()))
print('modules:', list(res['modules'].keys()))


#安裝模組(以URL, tag, local_folder來安裝模組)
data = json.dumps({'url': 'https://github.com/R300-AI/Tensorflow-YOLOv8m_det.git'})
res = json.loads(requests.post('http://localhost:5000/install', data=data, headers={'Content-Type': 'application/json'}).content)
print(list(res.keys()))

data = json.dumps({'tag': 'Pytorch-YOLOv8n_cls'})
res = json.loads(requests.post('http://localhost:5000/install', data=data, headers={'Content-Type': 'application/json'}).content)
print(list(res.keys()))

data = json.dumps({'local': 'Pytorch-YOLOv8m_det'})
res = json.loads(requests.post('http://localhost:5000/install', data=data, headers={'Content-Type': 'application/json'}).content)
print(list(res.keys()))


#先新增再刪除模組
data = json.dumps({'local': 'Pytorch-YOLOv8m_det'})
res = json.loads(requests.post('http://localhost:5000/install', data=data, headers={'Content-Type': 'application/json'}).content)
print(list(res.keys()))

data = json.dumps({'module': 'Pytorch/YOLOv8m_det'})
res = json.loads(requests.post('http://localhost:5000/uninstall', data=data, headers={'Content-Type': 'application/json'}).content)
print(list(res.keys()))


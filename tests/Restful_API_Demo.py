import requests, json, time, threading

"""
print("[測試系統資訊]")
res = requests.post('http://localhost:5000/help').content
print(res)
print('http://localhost:5000/help', 'OK\n')

res = requests.post('http://localhost:5000/index').content
print(res)
print('http://localhost:5000/index', 'OK\n')

data = json.dumps({'user': 'admin'})
res = json.loads(requests.post('http://localhost:5000/info', data=data, headers={'Content-Type': 'application/json'}).content)
print(res)
print('http://localhost:5000/info', 'OK\n')

print("[新增預設資料集]")
user = 'admin'
dataset_name = 'HardHat'
data = json.dumps({'user': user, 'dataset': dataset_name, 'dtype':'Vision2D', 'task':'ObjectDetection'})
res = json.loads(requests.post('http://localhost:5000/push', data=data, headers={'Content-Type': 'application/json'}).content)
print(res)
print('http://localhost:5000/push', 'OK\n')

print("[測試新增/刪除資料集]")
user = 'user'
dataset_name = 'HardHat'
data = json.dumps({'user': user, 'dataset': dataset_name, 'dtype':'Vision2D', 'task':'ObjectDetection'})
res = json.loads(requests.post('http://localhost:5000/push', data=data, headers={'Content-Type': 'application/json'}).content)
print("before:", res)
data = json.dumps({'user': user, 'dataset': dataset_name, 'dtype':'Vision2D', 'task':'ObjectDetection'})
res = json.loads(requests.post('http://localhost:5000/remove', data=data, headers={'Content-Type': 'application/json'}).content)
print("after:", res)
print('http://localhost:5000/remove', 'OK')
"""

"""
print("[測試模組安裝/刪除]")
res = requests.post('http://localhost:5000/index').content
index = json.loads(res.decode("utf-8"))
print(index)
for tag in ["Pytorch/YOLOv8n", "Pytorch/YOLOv8n_cls", "Tensorflow/YOLOv8m_det"]:
    data = json.dumps({'url': index[tag]})
    res = json.loads(requests.post('http://localhost:5000/install', data=data, headers={'Content-Type': 'application/json'}).content)
    print('http://localhost:5000/install', tag, '(by url)', 'OK')

    #data = json.dumps({'module': tag})
    #res = json.loads(requests.post('http://localhost:5000/uninstall', data=data, headers={'Content-Type': 'application/json'}).content)
    #print('http://localhost:5000/uninstall', tag, 'OK')

    data = json.dumps({'tag': tag})
    res = json.loads(requests.post('http://localhost:5000/install', data=data, headers={'Content-Type': 'application/json'}).content)
    print('http://localhost:5000/install', tag, ' (by tag)', 'OK')

    data = json.dumps({'module': tag})
    res = json.loads(requests.post('http://localhost:5000/uninstall', data=data, headers={'Content-Type': 'application/json'}).content)
    print('http://localhost:5000/uninstall', tag, 'OK')
"""

global flag
flag = True
def running():
    global flag
    flag = True
    data = json.dumps({'user': 'admin', 'dataset': 'HardHat', 'module':'Pytorch/YOLOv8n'})
    res = json.loads(requests.post('http://localhost:5000/run', data=data, headers={'Content-Type': 'application/json'}).content)
    print('http://localhost:5000/run', 'OK')
    flag = False

data = json.dumps({'tag': "Pytorch/YOLOv8n"})
res = json.loads(requests.post('http://localhost:5000/install', data=data, headers={'Content-Type': 'application/json'}).content)
t = threading.Thread(target = running)
t.start()
"""
while flag:
    data = json.dumps({'user': 'admin', 'dataset': 'HardHat', 'module':'Pytorch/YOLOv8n'})
    res = json.loads(requests.post('http://localhost:5000/logging', data=data, headers={'Content-Type': 'application/json'}).content)
    print("lines in logs:", res)
    time.sleep(1)
print('http://localhost:5000/logging', 'OK')
"""

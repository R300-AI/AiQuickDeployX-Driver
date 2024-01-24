from flask import Flask, request, json
from typing import get_args
from flask_cors import CORS
import os
app = Flask(__name__)
CORS(app)
global running
running = {}
@app.route('/help', methods=['POST']) #params:[] / outputs:[dtype, task, format]
def help():
    """
    【範例】
    POST: None
    RESPONSE: {'dtype': ['Vision2D'], 'task': ['ObjectDetection'], 'format': ['YOLOv8']}
    """
    import Xdriver
    return {'dtype': list(get_args(Xdriver.__dtype__)), 'task': list(get_args(Xdriver.__task__)), 'format': list(get_args(Xdriver.__format__))}

@app.route('/index', methods=['POST']) #params:[] / outputs:[module_names]
def index():
    """
    【範例】
    POST: None
    RESPONSE: {'Pytorch/YOLOv8n': 'https://github.com/R300-AI/Pytorch-YOLOv8n.git', ...}
    """
    from Xdriver import Plugins
    return json.load(open(Plugins().xdriver_dir + "/index.json"))

@app.route('/info', methods=['POST']) #params:[user] / outputs:[datasets, modules]
def info():
    from Xdriver import MongoDB, Plugins
    """
    【範例】
    POST: {'user': 'admin'}
    RESPONSE: {'datasets': ['HardHat'], 'modules': ['Pytorch/YOLOv8n']}
    """
    dialog = request.get_json()
    user = dialog['user']
    return {"datasets": MongoDB(user).List_Datasets(), "modules": Plugins().List_Modules()}

@app.route('/push', methods=['POST']) #params:[user, dataset, dtype, task] / outputs:[datasets]
def push():
    """
    【範例】
    POST: {'user': 'admin', 'dataset': 'HardHat'}
    RESPONSE: {'datasets': ['HardHat']}
    """
    from Xdriver import MongoDB
    dialog = request.get_json()
    user, dataset, dtype, task = dialog['user'], dialog['dataset'], 'Vision2D', 'ObjectDetection'

    client = MongoDB(user)
    datasets_list = client.Push(dataset, dtype, task)
    return {"datasets": datasets_list}

@app.route('/remove', methods=['POST']) #params:[user, dataset, dtype, task] / outputs:[datasets]
def remove():
    """
    【範例】
    POST: {'user': 'admin', 'dataset': 'HardHat'}
    RESPONSE: {'datasets': ['HardHat']}
    """
    from Xdriver import MongoDB
    dialog = request.get_json()
    user, dataset, dtype, task = dialog['user'], dialog['dataset'], 'Vision2D', 'ObjectDetection'
    
    client = MongoDB(user)
    datasets_list = client.Remove(dataset, dtype, task)
    return {"datasets": datasets_list}

@app.route('/install', methods=['POST'])
def install(): #params:[url, tag, local] / outputs:[modules]
    """
    【範例】
    POST: 
        -  {'url': 'https://github.com/R300-AI/Tensorflow-YOLOv8m_det.git'}
        -  {'tag': 'Pytorch-YOLOv8n_cls'}
    RESPONSE: {'Pytorch/YOLOv8m_det': '(module info)', ...}
    """
    from Xdriver import Plugins
    dialog, params = request.get_json(), {}
    for source in ['url', 'tag', 'local']:
        try:
            params[source] = dialog[source]
        except:
            print('Source {} not found'.format(source))
    module, source = Plugins(), list(params.keys())[0]
    if source == 'url':
        module.Install(url=params[source])
    elif source == 'tag':
        module.Install(tag=params[source])
    elif source == 'local':
        module.Install(local_name=params[source])
    return Plugins().List_Modules()

@app.route('/uninstall', methods=['POST'])
def uninstall(): #params:[module] / outputs:[modules]
    """
    【範例】
    POST: {'module': 'Pytorch/YOLOv8m_det'}
    RESPONSE: {'Pytorch/YOLOv8m_det': '(module info)', ...}
    """
    from Xdriver import Plugins
    dialog = request.get_json()
    module_name = dialog['module']
    module = Plugins()
    module.Uninstall(module_name)
    return Plugins().List_Modules()

@app.route('/run', methods=['POST']) #params:[user, dataset, module] / outputs:[outputs]
def run(): 
    """
    【範例】
    POST: {'user': 'admin', 'dataset': 'HardHat', 'module':'Pytorch/YOLOv8n'}
    RESPONSE: {'Pytorch/YOLOv8m_det': '(module info)', ...}
    """
    from Xdriver import MongoDB, Plugins
    dialog = request.get_json()
    user, dataset, module = dialog['user'], dialog['dataset'], dialog['module']
    
    plugin, client = Plugins(), MongoDB(user)
    client.Pull(dataset=dataset, metadata=plugin.Load(module, username=user))
    global running
    running[user+dataset+module] = True
    plugin.Run(dataset=dataset)
    del running[user+dataset+module]
    return {'outputs': 'OK'}

@app.route('/logging', methods=['POST']) #params:[user, dataset, module] / outputs:[outputs]
def logging(): 
    """
    【範例】
    POST: {'user': 'admin', 'dataset': 'HardHat', 'module':'Pytorch/YOLOv8n'}
    RESPONSE: {outputs: ["logs line1", "logs line2", ...]}
    """
    from Xdriver import Plugins
    dialog = request.get_json()
    user, dataset, module = dialog['user'], dialog['dataset'], dialog['module']
    plugin = Plugins()
    if user+dataset+module in running.keys():
        lines = ["docker image building..."]
    else:
        lines = []
    log_path = plugin.__modules__[module]['module_dir']
    log_path += '/tmp/logs/{user}/{dataset}.log'.format(user=user, dataset=dataset)
    if os.path.isfile(log_path):
        file = open(log_path, 'r')
        lines += file.read().splitlines()
    return {'outputs': lines}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

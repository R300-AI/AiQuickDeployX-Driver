from flask import Flask, request, json, send_from_directory
from typing import get_args
from flask_cors import CORS
import os, time, base64
app = Flask(__name__)
CORS(app)
global stack
stack = {}

@app.route('/help', methods=['POST']) #params:[] / outputs:[dtype, task, format]
def help():
    """
    【Example】
    POST: None
    RESPONSE: {'dtype': ['Vision2D'], 'task': ['ObjectDetection'], 'format': ['YOLOv8']}
    """
    import Xdriver
    return {'dtype': list(get_args(Xdriver.__dtype__)), 'task': list(get_args(Xdriver.__task__)), 'format': list(get_args(Xdriver.__format__))}

@app.route('/index', methods=['POST']) #params:[] / outputs:[module_names]
def index():
    """
    【Example】
    POST: None
    RESPONSE: {'Pytorch/YOLOv8n': 'https://github.com/R300-AI/Pytorch-YOLOv8n.git', ...}
    """
    from Xdriver import Plugins
    return json.load(open(Plugins().xdriver_dir + "/index.json"))

@app.route('/info', methods=['POST']) #params:[user] / outputs:[datasets, modules]
def info():
    from Xdriver import MongoDB, Plugins
    """
    【Example】
    POST: {'user': 'admin'}
    RESPONSE: {'datasets': ['HardHat'], 'modules': ['Pytorch/YOLOv8n']}
    """
    dialog = request.get_json()
    user = dialog['user']
    return {"datasets": MongoDB(user).List_Datasets(), "modules": Plugins().List_Modules(username=user)}

@app.route('/cache', methods=['POST']) #params:[user] / outputs:[dataset(base64_image)]
def cache():
    """
    【Example】
    POST: {'user': 'admin'}
    RESPONSE: {'HardHat': 'bytes_image', ...}
    """
    dialog = request.get_json()
    return json.load(open('./cache.json'))[dialog['user']]

@app.route('/push', methods=['POST']) #params:[user, dataset, dtype, task] / outputs:[datasets]
def push():
    """
    【Example】
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
    【Example】
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
    【Example】
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
    retry = 0
    while retry < 5:
        time.sleep(3)
        if source == 'url':
            module.Install(url=params[source])
            break
        elif source == 'tag':
            module.Install(tag=params[source])
            break
        elif source == 'local':
            module.Install(local_name=params[source])
            break
        retry += 1
    return Plugins().List_Modules()

@app.route('/uninstall', methods=['POST'])
def uninstall(): #params:[module] / outputs:[modules]
    """
    【Example】
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
    【Example】
    POST: {'user': 'admin', 'dataset': 'HardHat', 'module':'Pytorch/YOLOv8n'}
    RESPONSE: {'Pytorch/YOLOv8m_det': '(module info)', ...}
    """
    from Xdriver import MongoDB, Plugins
    dialog = request.get_json()
    user, dataset, module = dialog['user'], dialog['dataset'], dialog['module']
    
    plugin, client = Plugins(), MongoDB(user)
    image_path = client.Pull(dataset=dataset, metadata=plugin.Load(module, username=user))
    with open(image_path, 'rb') as f:
        image_bytes = base64.b64encode(f.read()).decode('ascii')

    cache = json.load(open('./cache.json'))
    user_cache = cache.get(user, {})
    dataset_cache = user_cache.get(dataset, {})
    module_cache = dataset_cache.get(module, {"benchmarks": {}, "img": "image_bytes..."})#image_bytes
    dataset_cache[module] = module_cache
    user_cache[dataset] = dataset_cache
    cache[user] = user_cache
    with open('./cache.json', "w") as f: 
        json.dump(cache, f)

    global stack
    stack[user+dataset+module] = {}
    benchmarks = plugin.Run(dataset=dataset)
    stack[user+dataset+module] = benchmarks

    cache = json.load(open('./cache.json'))
    cache[user][dataset][module]["benchmarks"] = benchmarks
    with open('./cache.json', "w") as f: 
        json.dump(cache, f)
    return benchmarks

@app.route('/logging', methods=['POST']) #params:[user, dataset, module] / outputs:[benchmarks, outputs]
def logging(): 
    """
    【Example】
    POST: {'user': 'admin', 'dataset': 'HardHat', 'module':'Pytorch/YOLOv8n'}
    RESPONSE: {outputs: ["logs line1", "logs line2", ...]}
    """
    from Xdriver import Plugins
    dialog = request.get_json()
    user, dataset, module = dialog['user'], dialog['dataset'], dialog['module']
    plugin, lines = Plugins(), []
    log_path = plugin.__modules__[module]['module_dir'] + '/tmp/logs/{user}/{dataset}.log'.format(user=user, dataset=dataset)
    benchmarks = {}
    if user+dataset+module in stack.keys():
        lines.append("docker image building...")
        if os.path.isfile(log_path):
            file = open(log_path, 'r')
            lines += file.read().splitlines()
            benchmarks = stack[user+dataset+module]
    return {'benchmarks': benchmarks, 'logs': lines}

@app.route('/download', methods=['POST'])  #params:[user, dataset, module, benchmark] / outputs: FILE
def download(): 
    """
    【Example】
    POST: {'user': 'admin', 'dataset': 'HardHat', 'module':'Pytorch/YOLOv8n', 'benchmark': 'INT8_quant.tflite'}
    RESPONSE: FILE
    """
    dialog = request.get_json()
    user, dataset, module, benchmark = dialog['user'], dialog['dataset'], dialog['module'], dialog['benchmark']
    path = json.load(open('./cache.json'))[user][dataset][module]["benchmarks"][benchmark]
    print(path)
    return send_from_directory(path, benchmark, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
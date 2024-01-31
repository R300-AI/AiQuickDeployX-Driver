from flask import Flask, request, json, send_from_directory, send_file
from typing import get_args
from flask_cors import CORS
import os, time, base64
from io import BytesIO

app = Flask(__name__)
CORS(app)
global stack
stack = {}

@app.route('/help', methods=['POST']) #params:[] / outputs:[dtype, task, format]
def help():
    import Xdriver
    print('receive a /help post...')
    return {'dtype': list(get_args(Xdriver.__dtype__)), 'task': list(get_args(Xdriver.__task__)), 'format': list(get_args(Xdriver.__format__))}

@app.route('/index', methods=['POST']) #params:[] / outputs:[module_names]
def index():
    print('receive a /index post...')
    from Xdriver import Plugins
    return json.load(open(Plugins().xdriver_dir + "/index.json"))

@app.route('/info', methods=['POST']) #params:[user] / outputs:[datasets, modules]
def info():
    from Xdriver import MongoDB, Plugins
    dialog = request.get_json()
    print('receive a /info post with dialog:', dialog)
    user = dialog['user']
    return {"datasets": MongoDB(user).List_Datasets(), "modules": Plugins().List_Modules(username=user)}

@app.route('/push', methods=['POST']) #params:[user, dataset, dtype, task] / outputs:[datasets]
def push():
    from Xdriver import MongoDB
    dialog = request.get_json()
    print('receive a /push post with dialog:', dialog)
    user, dataset, dtype, task = dialog['user'], dialog['dataset'], 'Vision2D', 'ObjectDetection'

    client = MongoDB(user)
    datasets_list = client.Push(dataset, dtype, task)
    return {"datasets": datasets_list}

@app.route('/remove', methods=['POST']) #params:[user, dataset, dtype, task] / outputs:[datasets]
def remove():
    from Xdriver import MongoDB
    dialog = request.get_json()
    print('receive a /remove post with dialog:', dialog)
    user, dataset, dtype, task = dialog['user'], dialog['dataset'], 'Vision2D', 'ObjectDetection'
    
    client = MongoDB(user)
    datasets_list = client.Remove(dataset, dtype, task)
    return {"datasets": datasets_list}

@app.route('/install', methods=['POST'])
def install(): #params:[url, tag, local] / outputs:[modules]
    from Xdriver import Plugins
    dialog, params = request.get_json(), {}
    print('receive a /install post with dialog:', dialog)
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
    from Xdriver import Plugins
    dialog = request.get_json()
    print('receive a /uninstall post with dialog:', dialog)
    module_name = dialog['module']
    module = Plugins()
    module.Uninstall(module_name)
    return Plugins().List_Modules()

@app.route('/run', methods=['POST']) #params:[user, dataset, module] / outputs:[outputs]
def run(): 
    from Xdriver import MongoDB, Plugins
    dialog = request.get_json()
    print('receive a /run post with dialog:', dialog)
    user, dataset, module = dialog['user'], dialog['dataset'], dialog['module']
    
    plugin, client = Plugins(), MongoDB(user)
    image_path = client.Pull(dataset=dataset, metadata=plugin.Load(module, username=user))
    with open(image_path, 'rb') as f:
        image_bytes = base64.b64encode(f.read()).decode('ascii')

    cache = json.load(open('./cache.json'))
    user_cache = cache.get(user, {})
    dataset_cache = user_cache.get(dataset, {})
    module_cache = dataset_cache.get(module, {"benchmarks": {}, "img": image_bytes})
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
    from Xdriver import Plugins
    dialog = request.get_json()
    print('receive a /logging post with dialog:', dialog)
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

@app.route('/cache', methods=['POST']) #params:[user] / outputs:[dataset(base64_image)]
def cache():
    dialog = request.get_json()
    print('receive a /cache post with dialog:', dialog)
    return json.load(open('./cache.json'))[dialog['user']]

"""
@app.route('/download', methods=['POST'])  #params:[user, dataset, module, benchmark] / outputs: FILE
def download(): 
    dialog = request.get_json()
    print('receive a /download post with dialog:', dialog)
    user, dataset, module, benchmark = dialog['user'], dialog['dataset'], dialog['module'], dialog['benchmark']
    #path = json.load(open('./cache.json'))[user][dataset][module]["benchmarks"][benchmark]
    path = 
    return send_file(path, as_attachment=True)
    #return send_from_directory(path, benchmark, as_attachment=True)
"""
@app.route('/download/<dialog>', methods=['GET'])#params:[<user>_<dataset>_<module>_<benchmark>]
def download(dialog): 
    print(dialog)
    user, dataset, module, benchmark = dialog.split('_')
    return send_file('./test.log', as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

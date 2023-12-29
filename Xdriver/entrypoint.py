from flask import Flask, request, json
from typing import get_args
app = Flask(__name__)

@app.route('/help', methods=['POST']) #params:[] / outputs:[supported_options(dtype, task)]
def help():
    import Xdriver
    return {"supported_options": {'dtype': list(get_args(Xdriver.__dtype__)), 'task': list(get_args(Xdriver.__task__))}}

@app.route('/index', methods=['POST']) #params:[] / outputs:[supported_options(dtype, task)]
def index():
    from Xdriver import Plugins
    return json.load(open(Plugins().xdriver_dir + "/index.json"))

@app.route('/info', methods=['POST']) #params:[user] / outputs:[datasets, modules]
def info():
    from Xdriver import MongoDB, Plugins
    dialog = request.get_json()
    user = dialog['user']

    return {"datasets": MongoDB(user).List_Datasets(), "modules": Plugins().List_Modules()}

@app.route('/push', methods=['POST']) #params:[user, dataset, dtype, task] / outputs:[datasets]
def push():
    from Xdriver import MongoDB
    dialog = request.get_json()
    user, dataset, dtype, task = dialog['user'], dialog['dataset'], dialog['dtype'], dialog['task']

    client = MongoDB(user)
    datasets_list = client.Push(dataset, dtype, task)
    return {"datasets": datasets_list}

@app.route('/remove', methods=['POST']) #params:[user, dataset, dtype, task] / outputs:[datasets]
def remove():
    from Xdriver import MongoDB
    dialog = request.get_json()
    user, dataset, dtype, task = dialog['user'], dialog['dataset'], dialog['dtype'], dialog['task']
    
    client = MongoDB(user)
    datasets_list = client.Remove(dataset, dtype, task)
    return {"datasets": datasets_list}

@app.route('/install', methods=['POST'])
def install(): #params:[url, tag, local] / outputs:[modules]
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
    from Xdriver import Plugins
    dialog = request.get_json()
    module_name = dialog['module']

    module = Plugins()
    module.Uninstall(module_name)
    return Plugins().List_Modules()

#@app.route('/run', methods=['POST']) #params:[user, dataset, module]

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
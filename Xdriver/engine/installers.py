from git import Repo
from pathlib import Path
from datetime import datetime
import os, shutil, json, stat

class Module_Installer():
    def __init__(self, xdriver_dir):
        self.xdriver_dir = xdriver_dir
    
    def install_from_url(self, url):
        tag = url.replace('.git', '').split('/')[-1]
        local_path = "{dir}/data/models/{tag}".format(dir=self.xdriver_dir, tag=tag.replace("/", "-"))
        spec_path = "{local_path}/spec.json".format(local_path=local_path)
        self.chmod(local_path)
        if Path(local_path).exists():
            shutil.rmtree(local_path)
        Repo.clone_from(url, local_path)
        spec = json.load(open(spec_path))
        dtype, task =  spec['dtype'], spec['task']
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        spec["date"] = date
        with open(spec_path, "w") as f: 
            json.dump(spec, f)
        framework, model = tag.split('-')
        target_path = "{xdriver_dir}/plugins/{dtype}/{task}/{framework}/{model}".format(xdriver_dir=self.xdriver_dir, dtype=dtype, task=task, framework=framework, model=model)
        self.chmod(target_path)
        if Path(target_path).exists():
            shutil.rmtree(target_path)
        shutil.move(local_path, target_path)

    def install_from_local(self, local_path):
        tag = local_path.split('/')[-1]
        spec_path = "{local_path}/spec.json".format(local_path=local_path)
        spec = json.load(open(spec_path))
        dtype, task =  spec['dtype'], spec['task']
        framework, model = tag.split('-')
        target_path = "{xdriver_dir}/plugins/{dtype}/{task}/{framework}/{model}".format(xdriver_dir=self.xdriver_dir, dtype=dtype, task=task, framework=framework, model=model)
        if Path(target_path).exists():
            shutil.rmtree(target_path)
        self.chmod(local_path)
        shutil.copytree(local_path, target_path)

    def install_from_tag(self, tag):
        index = json.load(open("{xdriver_dir}/index.json".format(xdriver_dir=self.xdriver_dir)))
        if  tag in index.keys():
            self.install_from_url(index[tag])
        else:
            print("module not found")

    def chmod(self, path):
        for root, dirs, files in os.walk(path):
            for dir in dirs:
                os.chmod(os.path.join(root, dir), stat.S_IRWXU)
            for file in files:
                os.chmod(os.path.join(root, file), stat.S_IRWXU)
import Xdriver, os, subprocess, shutil, json, stat
from Xdriver.cfg.driver import Driver
from pathlib import Path
from git import Repo

class Plugins(Driver):
    def __init__(self):
        super().__init__()
        self.__modules__ = self.search_modules()

    def Install(self, url=None, local_path=None):
        if url != None:
            module_name = url.replace('.git', '').split('/')[-1]
            local_path = "{dir}/plugins/temp".format(dir=self.xdriver_dir)
            spec_path = "{local_path}/spec.json".format(local_path=local_path)
            self.chmod(local_path)
            if Path(local_path).exists():
                shutil.rmtree(local_path)
            Repo.clone_from(url, local_path)
            spec = json.load(open(spec_path))
            dtype, task =  spec['dtype'], spec['task']
            framework, model = module_name.split('-')
            target_path = "{xdriver_dir}/plugins/{dtype}/{task}/{framework}/{model}".format(xdriver_dir=self.xdriver_dir, dtype=dtype, task=task, framework=framework, model=model)
            if Path(target_path).exists():
                shutil.rmtree(target_path)
            shutil.move(local_path, target_path)
            
        elif local_path != None:
            module_name = local_path.split('/')[-1]
            spec_path = "{local_path}/spec.json".format(local_path=local_path)
            spec = json.load(open(spec_path))
            dtype, task =  spec['dtype'], spec['task']
            framework, model = module_name.split('-')
            target_path = "{xdriver_dir}/plugins/{dtype}/{task}/{framework}/{model}".format(xdriver_dir=self.xdriver_dir, dtype=dtype, task=task, framework=framework, model=model)
            if Path(target_path).exists():
                shutil.rmtree(target_path)
            self.chmod(local_path)
            shutil.copy(local_path, target_path)
        
    def Load(self, module, username):
        if module in self.__modules__.keys():
            self.dtype, self.task, self.username = self.__modules__[module]["dtype"], self.__modules__[module]["task"], username
            self.module_dir = self.__modules__[module]["module_dir"]
            self.dataset_dir = self.module_dir + '/tmp/datasets/' + username
            self.log_dir = self.module_dir + '/tmp/logs/' + username
            self.output_dir = self.module_dir + '/tmp/outputs/' + username
            return {"dataset_dir": self.dataset_dir, "dtype": self.dtype, "task": self.task, "username": self.username}
        else:
            print('engine not found, please check your configuration.')

    def Run(self, dataset=None):
        entrypoint, dataset, output, log = self.tmp_config(self.username, dataset, True)
        subprocess.run(["bash ", entrypoint, '-u', self.username, '-d', dataset, '-l', log, '-o', output])
        shutil.rmtree(dataset)
        print('finish')

    def chmod(self, path):
        for root, dirs, files in os.walk(path):  
            for dir in dirs:
                os.chmod(os.path.join(root, dir), stat.S_IRWXU)
            for file in files:
                os.chmod(os.path.join(root, file), stat.S_IRWXU)

    def search_modules(self):
        print('【Plugins】Existing Modules:')
        modules = {}
        modules_dir = self.xdriver_dir + '/plugins'
        for dtype in [f for f in os.listdir(modules_dir) if os.path.isdir(os.path.join(modules_dir, f))]:
            dtype_dir = modules_dir + '/' + dtype
            for task in [f for f in os.listdir(dtype_dir) if os.path.isdir(os.path.join(dtype_dir, f))]:
                task_dir = dtype_dir + '/' + task 
                for framework in [f for f in os.listdir(task_dir) if os.path.isdir(os.path.join(task_dir, f))]:
                    framework_dir = task_dir + '/' + framework
                    for model in [f for f in os.listdir(framework_dir) if os.path.isdir(os.path.join(framework_dir, f))]:
                        model_dir = framework_dir + '/' + model
                        module = framework + '/' + model
                        modules[module] = {"dtype": dtype, "task": task, "module_dir": model_dir}
                        print('  -', module, '(dtype:', dtype ,'/task:', task, ')')
        return  modules

    def tmp_config(self, username, dataset, initialize = True):
        self.entrypoint =  os.path.relpath('./' + self.module_dir + '/run.sh', os.getcwd()).replace('\\', '/')
        self.dataset =  (self.dataset_dir + '/' + dataset).replace('\\', '/')
        self.output =  (self.output_dir + '/' + dataset).replace('\\', '/')
        self.log =  (self.log_dir + '/' + dataset + '.log').replace('\\', '/')

        print('【Plugins】Runtime Config:')
        print('   - Entrypoint:', os.path.relpath(self.entrypoint, os.getcwd()))
        print('   - Dataset folder:', os.path.relpath(self.dataset, os.getcwd()))
        print('   - Output folder:', os.path.relpath(self.output, os.getcwd()))
        print('   - Log file:', os.path.relpath(self.log, os.getcwd()))
        print('---------------------------')
        if initialize == True:
            Path(self.dataset_dir).mkdir(parents=True, exist_ok=True)
            Path(self.log_dir).mkdir(parents=True, exist_ok=True)
            Path(self.output_dir).mkdir(parents=True, exist_ok=True)
            if Path(self.output).exists():
                shutil.rmtree(self.output)
            if Path(self.log).exists():
                os.remove(self.log)
            Path(self.log).touch()
            os.makedirs(self.output)
        return self.entrypoint, self.dataset, self.output, self.log
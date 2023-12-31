import Xdriver, os, subprocess, shutil
from Xdriver.cfg.driver import Driver
from .installers import Module_Installer
from pathlib import Path

class Plugins(Driver):
    def __init__(self):
        super().__init__()
        self.__modules__ = self.List_Modules()

    def List_Modules(self):
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
        self.__modules__ = modules
        return  modules

    def Uninstall(self, module):
        modules = self.List_Modules()
        module_path = modules[module]['module_dir']
        if Path(module_path).exists():
            shutil.rmtree(module_path)

    def Install(self, url=None, tag=None, local_name=None):
        processor = Module_Installer(self.xdriver_dir)
        if url != None:
            processor.install_from_url(url)
        elif tag != None:
            processor.install_from_tag(tag)
        elif local_name != None:
            local_path = self.xdriver_dir + '/data/models/' + local_name
            processor.install_from_local(local_path)

    def Run(self, dataset=None):
        entrypoint, dataset, output, log = self.tmp_config(self.username, dataset, True)
        subprocess.run(['./Xdriver/dos2unix.exe', entrypoint.replace(self.xdriver_dir, '.')])
        subprocess.run(["bash", entrypoint, '-u', self.username, '-d', dataset, '-l', log, '-o', output])
        shutil.rmtree(dataset)
        
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

    def tmp_config(self, username, dataset, initialize = True):
        self.entrypoint =  os.path.relpath('./' + self.module_dir + '/run.sh', os.getcwd()).replace('\\', '/')
        self.entrypoint = self.entrypoint.replace(os.getcwd()[1:], os.getcwd())
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

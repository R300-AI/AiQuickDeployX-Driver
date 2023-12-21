import Xdriver, os, subprocess, shutil
from Xdriver.cfg.driver import Driver
from pathlib import Path

class Plugins(Driver):
    def __init__(self):
        super().__init__()
        self.__modules__ = self.search_modules()

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

    def make_tmp(self, username):
        self.dataset_dir = self.module_dir + '/tmp/datasets/' + username
        self.log_dir = self.module_dir + '/tmp/logs/' + username
        self.output_dir = self.module_dir + '/tmp/outputs/' + username
        Path(self.dataset_dir).mkdir(parents=True, exist_ok=True)
        Path(self.log_dir).mkdir(parents=True, exist_ok=True)
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)


    def Load(self, module, username):
        if module in self.__modules__.keys():
            self.dtype, self.task, self.username = self.__modules__[module]["dtype"], self.__modules__[module]["task"], username
            self.module_dir = self.__modules__[module]["module_dir"]
            self.make_tmp(self.username)
            return {"dataset_dir": self.dataset_dir, "dtype": self.dtype, "task": self.task, "username": self.username}
        else:
            print('engine not found, please check your configuration.')

    def Run(self, dataset=None):
        entrypoint =  os.path.relpath('./' + self.module_dir + '/run.sh', os.getcwd()).replace('\\', '/')
        dataset_dir =  (self.dataset_dir + '/' + dataset).replace('\\', '/')
        output_dir =  (self.output_dir + '/' + dataset).replace('\\', '/')
        log_path =  (self.log_dir + '/' + dataset + '.log').replace('\\', '/')

        if Path(output_dir).exists():
            shutil.rmtree(output_dir)
        if Path(log_path).exists():
            os.remove(log_path)
        Path(log_path).touch()
        os.makedirs(output_dir)
        print('【Plugins】Runtime Config:')
        print('   - Dataset folder:', os.path.relpath(dataset_dir, os.getcwd()))
        print('   - Output folder:', os.path.relpath(output_dir, os.getcwd()))
        print('   - Log file:', os.path.relpath(log_path, os.getcwd()))
        print('---------------------------')
        subprocess.run(["bash ", entrypoint, '-u', self.username, '-d', dataset_dir, '-l', log_path, '-o', output_dir])
        print('finish.')
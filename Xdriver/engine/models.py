import Xdriver, os, subprocess

class Models():
    def __init__(self, dtype: Xdriver.__dtype__, task: Xdriver.__task__, engine=None):
        self.dtype = dtype
        self.task = task
        self.engine = engine

    def run(self, dataset=None, username=None):
        root_path = os.path.dirname(os.path.realpath(__file__))
        engine_path = '/models/{dtype}/{task}/{engine}/run.sh'.format(dtype=self.dtype, task=self.task, engine=self.engine)
        path = '.' + root_path.replace('\Xdriver\engine', engine_path).split('AiQuickDeployX-Driver')[-1]
        output_path = path.replace('run.sh', 'tmp/outputs/{username}/{dataset}'.format(username=username, dataset=dataset))
        if os.path.exists(output_path) == False:
            os.makedirs(output_path)
        subprocess.run(["bash", path,  '-u', username , '-d', dataset])
        print('Outputs saved to:', output_path)
        return output_path
        
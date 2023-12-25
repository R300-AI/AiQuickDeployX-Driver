import os
class Driver():
    def __init__(self):
        self.xdriver_dir = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
        self.xdriver_dir = self.xdriver_dir.split('/Xdriver/cfg')[0]

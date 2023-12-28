import os
class Driver():
    def __init__(self):
        self.xdriver_dir = os.path.dirname(os.path.realpath(__file__)).replace('/Xdriver/cfg', '')
        print(self.xdriver_dir)
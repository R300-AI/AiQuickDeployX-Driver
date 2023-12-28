from Xdriver import Plugins
import os

module = Plugins()
module.Install(url='https://github.com/R300-AI/Tensorflow-YOLOv8m_det.git')
module.Install(module_name='Pytorch-YOLOv8n_cls')
module.Install(local_path=os.path.dirname(os.path.realpath(__file__)) + '/data/Pytorch-YOLOv8m_det')

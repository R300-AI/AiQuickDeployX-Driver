from Xdriver import MongoDB, Plugins

#載入模組+資料集，並為特定使用者建立工作路徑
module = Plugins()
client = MongoDB('localhost', '27017', 'admin', 'admin')

client.Pull(dataset='HardHat', metadata=module.Load('Pytorch/YOLOv8n', username='markov'))
module.Run(dataset='HardHat')
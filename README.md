### 開發環境
1. Bash Shell ([安裝](https://itsfoss.com/install-bash-on-windows/))
2. Github Agent ([安裝](https://desktop.github.com/))
3. Python Compiler>=3.8, PIP & Library ([安裝](https://github.com/R300-AI/AiQuickDeployX-Driver/blob/main/docs/Python%20Installation.md))
4. Docker Engine ([安裝](https://docs.docker.com/engine/install/))
5. MongoDB Container ([安裝](https://github.com/R300-AI/AiQuickDeployX-Driver/blob/main/docs/MongoDB%20installation.md))
    
### 目錄結構
```
AiQuickDeployX-Driver
    ├─ plugins            # 放置已安裝的訓練引擎，由X-driver.plugins模組統一管理
          ... ...         (它們皆會依照<dtype>/<task>/<framwork>/<model>_<tag>的資料夾路徑來進行分類)
    ├─ Xdriver           # Python模組的主體，使用範例請參考demo.py
    ├─ tests             # 測試功能用的程式碼
    ├─ docs              # 放置說明文件
    └─ index.json        # 訓練引擎的安裝來源與資訊
```

### 使用說明
![Usage](https://github.com/R300-AI/AiQuickDeployX-Driver/assets/140595764/908df835-d7a9-44ab-96ce-ff49c58c4851)


#### 快速開始
* 從線上取得HardHat範例資料集寫入MongoDB。以Vision2D/ObjectDetection任務類型為例。
    ```python
    from Xdriver import MongoDB, Plugins
    
    #下載範例資料集至本機的執行目錄
    dataset_path = MongoDB.Download_Samples(dtype='Vision2D', task='ObjectDetection')
    
    #將資料集寫入MongoDB，並以資料夾名稱(dataset_path)來命名資料集。*可於MongoDB中檢視
    client = MongoDB('localhost', '27017', 'admin', 'admin')
    client.Push(dtype='Vision2D', task='ObjectDetection', dataset_path=dataset_path)
    ```
* 為使用者建立訓練模組，並從MongoDB拉取資料集來進行訓練。
    ```python
    from Xdriver import MongoDB, Plugins
    
    #載入模組+資料集，並為特定使用者建立工作路徑
    module = Plugins()
    client = MongoDB('localhost', '27017', 'admin', 'admin')
    client.Pull(dataset='HardHat', metadata=module.Load('Pytorch/YOLOv8n', username='markov'))

    #執行訓練
    module.Run(dataset='HardHat')
    ```
    
### 附錄文件
* [ITRI LOGO附件](https://github.com/R300-AI/AiQuickDeployX-Driver/tree/main/docs/logo/LOGO)

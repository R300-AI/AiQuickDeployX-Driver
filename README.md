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
![image](https://github.com/R300-AI/AiQuickDeployX-Driver/assets/140595764/d23941da-69d5-47ce-8f22-bf5475213a6b)

#### 快速開始
##### MongoDB
* 從Roboflow取得範例資料集(HardHat)
    ```python
    import Xdriver
    from Xdriver import MongoDB, Plugins
    
    #下載範例資料集至本機的執行目錄
    dataset_path = MongoDB.Download_Samples(dtype='Vision2D', task='ObjectDetection')
    
    #將資料集寫入MongoDB，並以資料夾名稱(dataset_path)來命名資料集。*可於MongoDB中檢視
    client = MongoDB('localhost', '27017', 'admin', 'admin')
    client.Push(dtype='Vision2D', task='ObjectDetection', dataset_path=dataset_path)
    ```
* 將指定的資料集寫入MongoDB(需先整理成YOLOv8資料夾格式)，以HardHat範例資料集作為為例
    ```python
    from Xdriver import MongoDB, Models
    
    dataset_path = 'data\HardHat'
    client = MongoDB('localhost', '27017', 'admin', 'admin')
    client.Push(dtype='Vision2D', task='ObjectDetection', dataset_path=dataset_path, retrain_origin = False)
    ```
* 從MongoDB拉取指定資料集，並置於指定的引擎系統(<engine>/tmp/datasets/...)
    ```python
    from Xdriver import MongoDB, Models
    
    client = MongoDB('localhost', '27017', 'admin', 'admin')
    client.Pull(dtype='Vision2D', task='ObjectDetection', dataset='HardHat', engine='Pytorch/YOLOv8n', username='admin')
    ```
* 執行指定的引擎環境(需先透過前個步驟Pull好所要訓練的資料集)，並回傳輸出檔案的存放路徑
    ```python
    from Xdriver import MongoDB, Models
    
    model = Models(dtype='Vision2D', task='ObjectDetection', engine='Pytorch/YOLOv8n')
    output_path = model.run(dataset='HardHat', username='admin')
    ```
    
### 開發文件
* [[2] How to Access Database for Training and Orginize Engine Plugins?]()
* [ITRI LOGO附件](https://github.com/R300-AI/AiQuickDeployX-Driver/tree/main/docs/logo/LOGO)

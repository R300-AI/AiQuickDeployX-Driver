### 環境需求
1. WSL or Linux OS    **避免路徑規則的錯誤*
2. Python & Bash Compiler    **執行Scripts所需的工具*
3. Docker Engine ([安裝](https://docs.docker.com/engine/install/))

### 系統說明
![image](https://github.com/R300-AI/AiQuickDeployX-Driver/assets/140595764/ba2f144e-8392-495f-b155-76399b8646ef)




#### 安裝
* 安裝並啟動MongoDB Client的Docker容器
```bash
bash ./build/install_mongodb.sh
```
* 安裝Xdriver的Python相依套件於本機環境
```bash
bash ./build/install_mongodb.sh
```
#### 快速開始
* 啟動Xdriver伺服器(監聽 5000port)
```bash
bash ./auto_up.sh
```
* 測試APIs功能是否正常
```bash
python ./tests/Restful_API_Demo.py
```

### 附錄文件
* [ITRI LOGO附件](https://github.com/R300-AI/AiQuickDeployX-Driver/tree/main/docs/logo/LOGO)
  
### What's Next?
* [Kubernete](https://learn.microsoft.com/zh-tw/azure/aks/intro-kubernetes)

  ![Usage](https://github.com/R300-AI/AiQuickDeployX-Driver/assets/140595764/908df835-d7a9-44ab-96ce-ff49c58c4851)

### 目錄結構
```
AiQuickDeployX-Driver
    ├─ Xdriver            # Xdriver的系統核心
    ├─ build              # MongoDB和Xdriver的Docker安裝指令
    ├─ docker             # Xdriver系統環境的源碼
    ├─ docs               # 文件資源
    └─ data               # Web API功能測試的Python執行檔
```

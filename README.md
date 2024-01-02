### 後端環境需求
1. WSL or Linux OS    **避免路徑規則的錯誤*
2. Python & Bash Compiler    **執行Scripts所需的工具*
3. Docker Engine ([安裝](https://docs.docker.com/engine/install/))

### 系統架構
![image](https://github.com/R300-AI/AiQuickDeployX-Driver/assets/140595764/ba2f144e-8392-495f-b155-76399b8646ef)

#### 快速開始
* 安裝MongoDB-docker
```bash
bash ./build/install_mongodb.sh
```
* 啟動Xdriver伺服器
```bash
bash ./activate.sh
```
若有必要可以透過`python ./tests/Restful_API_Demo.py`測試RestfulAPI的功能是否正常


### 附錄文件
* [ITRI LOGO](https://github.com/R300-AI/AiQuickDeployX-Driver/tree/main/docs/logo/LOGO)
* [開發者手冊](https://github.com/R300-AI/AiQuickDeployX-Driver/blob/main/docs/White_Paper.md)
  
### What's Next?
* [透過Kubernete分散化系統模組+規範模組開發方式](https://learn.microsoft.com/zh-tw/azure/aks/intro-kubernetes)


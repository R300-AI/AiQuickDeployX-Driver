# APIs
|  Routes   | Post(JSON)  | Response  | 註解  |
|  ----   | ----  | ----  | ----  |
| /help   | - | `dtype:str`, `task:str`, `format:str`  | 目前系統支援的任務類型與資料集格式 |
| /index  | - | `module:str(url)`| 所有開源模組的rul安裝連結 |
| /info  | `user:str` |  `datasets:list(str)`, `modules:list(str)` | 取得特定使用者可存取的資料集、訓練模組名稱 |
| /push  | `user:str`, `dataset:str(*assign a name)`, `dtype:str(Vision2D)`, `task:str(ObjectDetection)` | `datasets:list` | 新增資料集(模擬)，回傳該使用者可存取的資料集列表 |
| /remove  | 单元格 | ----  | ----  |
| /install  | 单元格 | ----  | ----  |
| /uninstall  | 单元格 | ----  | ----  |
| /run  | 单元格 | ----  | ----  |

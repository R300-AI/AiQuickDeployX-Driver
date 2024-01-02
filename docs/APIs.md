# APIs
### 基本資訊
|  Routes   | Post(JSON)  | Response  | 註解  |
|  ----   | ----  | ----  | ----  |
| /help   | - | `dtype:str`, `task:str`, `format:str`  | 回傳目前系統支援的任務類型與資料集格式 |
| /index  | - | `module:str(url)`| 所有開源模組的rul安裝連結 |
| /info  | `user:str` |  `datasets:list(str)`, `modules:list(str)` | 取得特定使用者可存取的資料集、訓練模組名稱 |

### 資料集管理
|  Routes   | Post(JSON)  | Response  | 註解  |
|  ----   | ----  | ----  | ----  |
| /push  | `user:str`, `dataset:str(*assign a name)` | `datasets:list` | 新增資料集(模擬)，回傳該使用者可存取的資料集列表 |
| /remove  | `user:str`, `dataset:str(*assign a name)` | `datasets:list` | 刪除資料集(模擬)，回傳該使用者可存取的資料集列表 |

### 訓練模組
|  Routes   | Post(JSON)  | Response  | 註解  |
|  ----   | ----  | ----  | ----  |
| /install  | `url:str`, `tag:str`, `local:str` | `modules:dict(metadata)`  | 新增模組，選用其一種來源即可。完成後回傳該使用者可存取的訓練模組 |
| /uninstall  | `module:str` | `modules:list(str)`  | 透過名稱刪除模組。完成後回傳現存的訓練模組 |
| /run  | `user:str`, `dataset:str`, `module:str` | `outputs:None`  | 執行模組。輸出(Logs、模型檔)再依檔案產出、下載方式決定 |

# AI News 2.0 - 重構版本

這是一個自動抓取、翻譯和朗讀 arXiv AI 論文摘要的網站專案，現已完全重構為更模組化、可維護的架構。

## 🆕 架構重構亮點

### 🏗️ 全新的專案結構

```
AI_news2/
├── 📁 src/                           # 核心源代碼
│   ├── 📁 core/                      # 核心模組
│   │   ├── config.py                 # 統一配置管理
│   │   ├── models.py                 # Pydantic 資料模型
│   │   └── exceptions.py             # 自定義異常
│   ├── 📁 services/                  # 服務層（業務邏輯）
│   │   ├── arxiv_service.py          # arXiv 論文抓取
│   │   ├── translation_service.py    # Gemini 翻譯服務
│   │   ├── audio_service.py          # 語音生成服務
│   │   └── storage_service.py        # 資料儲存服務
│   ├── 📁 utils/                     # 工具函式
│   │   ├── logging_utils.py          # 日誌管理
│   │   ├── file_utils.py             # 檔案操作
│   │   └── date_utils.py             # 日期處理
│   └── 📁 cli/                       # 命令列介面
│       └── main.py                   # 新的主執行腳本
├── 📁 web/                           # 前端資源
│   ├── index.html                    # 主頁面
│   ├── index.css                     # 樣式檔案
│   └── index.js                      # JavaScript
├── 📁 data/                          # 資料目錄
│   ├── news.jsonl                    # 新聞資料
│   ├── processed_ids.txt             # 已處理ID
│   └── 📁 audios/                    # 音訊檔案
└── Makefile                          # 便利指令
```

### 🔧 主要改進

1. **模組化設計**: 將功能拆分為獨立的服務類別
2. **配置管理**: 統一的配置管理系統
3. **錯誤處理**: 完整的異常處理機制
4. **日誌系統**: 結構化的日誌記錄
5. **型別提示**: 完整的 Python 型別提示
6. **測試友好**: 易於測試的架構設計

## 🚀 快速開始

### 環境設置

1. **克隆專案**

   ```bash
   git clone https://github.com/your-username/AI_news2.git
   cd AI_news2
   ```

2. **建立虛擬環境**

   ```bash
   make venv
   .venv\Scripts\activate  # Windows
   ```

3. **安裝依賴**

   ```bash
   make install
   ```

4. **設置環境變數**
   ```bash
   # 設置 GEMINI_API_KEY
   set GEMINI_API_KEY=your_api_key_here
   ```

### 使用方法

1. **更新新聞資料**

   ```bash
   make update-news
   ```

2. **啟動本地伺服器**

   ```bash
   make serve
   ```

3. **檢查配置**
   ```bash
   make check-config
   ```

## 📋 可用指令

使用 `make help` 查看所有可用指令：

```bash
make help              # 顯示幫助資訊
make install           # 安裝專案依賴
make update-news       # 更新新聞資料
make serve             # 啟動本地開發伺服器
make test              # 執行測試
make clean             # 清理暫存檔案
make backup            # 備份資料檔案
make lint              # 程式碼檢查
make format            # 格式化程式碼
```

## 🔧 服務架構

### 核心服務

1. **ArxivService**: 負責從 arXiv 抓取論文
2. **TranslationService**: 使用 Gemini API 進行翻譯
3. **AudioService**: 生成中文語音檔案
4. **StorageService**: 管理資料的儲存和讀取

### 配置管理

所有配置都集中在 `src/core/config.py` 中：

```python
class Config:
    # API 配置
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # 檔案路徑
    DATA_DIR = BASE_DIR / "data"
    AUDIO_DIR = DATA_DIR / "audios"

    # arXiv 設定
    ARXIV_QUERIES = ["AI", "Foundation Model", "Diffusion Model"]
    MAX_RESULTS_PER_QUERY = 50

    # Gemini 設定
    GEMINI_MODEL = "gemini-2.0-flash-001"
    TEMPERATURE = 0.7
```

## 🎯 資料模型

使用 Pydantic 定義結構化的資料模型：

```python
class Paper(BaseModel):
    query: str
    id: str
    title: str
    summary: str
    authors: List[str]
    # ... 其他欄位

class PaperTranslation(BaseModel):
    title_zh: str
    summary_zh: str
    applications: List[str]
    pitch: str
```

## 📊 錯誤處理

完整的異常處理系統：

```python
class AINewsException(Exception): ...
class TranslationError(AINewsException): ...
class AudioGenerationError(AINewsException): ...
class ArxivFetchError(AINewsException): ...
```

## 🔍 日誌系統

結構化的日誌記錄：

```python
from src.utils.logging_utils import get_logger

logger = get_logger(__name__)
logger.info("處理開始")
logger.error("處理失敗", exc_info=True)
```

## 🧪 測試

執行測試：

```bash
make test
```

## 📈 監控和統計

新版本提供詳細的處理統計：

- 總抓取論文數
- 成功翻譯數
- 翻譯失敗數
- 音訊生成數
- 成功率計算

## 🚀 部署

### GitHub Actions

專案包含自動化的 GitHub Actions 工作流程：

- 每小時自動更新新聞
- 自動部署到 GitHub Pages
- 持續整合和測試

### 手動部署

```bash
make deploy
```

## 🔧 開發指南

### 新增功能

1. 在對應的服務類別中新增方法
2. 更新資料模型（如需要）
3. 新增測試
4. 更新文檔

### 程式碼風格

```bash
make lint    # 檢查程式碼
make format  # 格式化程式碼
```

## 📝 更新日誌

### v2.0 - 架構重構版本

- 🔄 完全重構為服務導向架構
- 📊 統一的配置管理系統
- 🛡️ 完整的錯誤處理機制
- 📋 結構化的日誌系統
- 🧪 測試友好的設計
- 📁 重新組織的檔案結構
- 🔧 Makefile 便利指令

## 🤝 貢獻

歡迎提交 Pull Request 和 Issue！

## 📄 授權

MIT License

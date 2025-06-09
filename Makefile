# AI News 專案 Makefile
# 提供常用的開發和部署指令

.PHONY: help install test clean update-news serve deploy

# 預設目標
help:
	@echo "AI News 專案可用指令："
	@echo "  install      - 安裝專案依賴"
	@echo "  test         - 執行測試"
	@echo "  clean        - 清理暫存檔案"
	@echo "  update-news  - 更新新聞資料"
	@echo "  serve        - 啟動本地開發伺服器"
	@echo "  deploy       - 部署到 GitHub Pages"
	@echo "  backup       - 備份資料檔案"
	@echo "  lint         - 程式碼檢查"

# 安裝依賴
install:
	@echo "安裝 Python 依賴..."
	pip install -r requirements.txt
	@echo "依賴安裝完成！"

# 執行測試
test:
	@echo "執行測試..."
	python -m pytest tests/ -v
	@echo "測試完成！"

# 清理暫存檔案
clean:
	@echo "清理暫存檔案..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	@echo "清理完成！"

# 更新新聞資料
update-news:
	@echo "更新新聞資料..."
	python src/cli/main.py
	@echo "新聞更新完成！"

# 啟動本地開發伺服器
serve:
	@echo "啟動本地開發伺服器..."
	cd web && python -m http.server 8000
	@echo "伺服器已啟動在 http://localhost:8000"

# 備份資料檔案
backup:
	@echo "備份資料檔案..."
	python -c "from src.services.storage_service import StorageService; StorageService().backup_data()"
	@echo "備份完成！"

# 程式碼檢查
lint:
	@echo "執行程式碼檢查..."
	python -m flake8 src/ --max-line-length=100
	python -m mypy src/
	@echo "程式碼檢查完成！"

# 安裝開發依賴
install-dev:
	@echo "安裝開發依賴..."
	pip install -r requirements.txt
	pip install pytest flake8 mypy black
	@echo "開發依賴安裝完成！"

# 格式化程式碼
format:
	@echo "格式化程式碼..."
	python -m black src/ tests/
	@echo "程式碼格式化完成！"

# 檢查配置
check-config:
	@echo "檢查專案配置..."
	python -c "from src.core.config import Config; Config().validate(); print('配置檢查通過！')"

# 建立新的虛擬環境
venv:
	@echo "建立虛擬環境..."
	python -m venv .venv
	@echo "虛擬環境建立完成！請執行: .venv\Scripts\activate" 
"""
配置管理模組

統一管理專案中的所有配置項目，包括API金鑰、檔案路徑、搜尋參數等。
"""

import os
from typing import List, Optional
from pathlib import Path


class Config:
    """專案配置類別"""
    
    # API 配置
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    
    # 檔案路徑配置
    BASE_DIR = Path(__file__).parent.parent.parent
    DATA_DIR = BASE_DIR / "docs" / "data"
    AUDIO_DIR = DATA_DIR / "audios"
    WEB_DIR = BASE_DIR / "web"
    
    NEWS_FILE = DATA_DIR / "news.jsonl"
    PROCESSED_IDS_FILE = DATA_DIR / "processed_ids.txt"
    
    # arXiv 搜尋配置
    ARXIV_QUERIES: List[str] = ["AI", "Foundation Model", "Diffusion Model"]
    MAX_RESULTS_PER_QUERY: int = 50
    
    # Gemini 配置
    GEMINI_MODEL: str = "gemini-2.0-flash-001"
    TEMPERATURE: float = 0.7
    MAX_OUTPUT_TOKENS: int = 2000
    
    # 語音合成配置
    TTS_LANGUAGE: str = "zh-tw"
    GEMINI_TTS_MODEL: str = "gemini-2.5-flash-preview-tts"
    GEMINI_TTS_VOICE: str = "Kore"  # 可選的語音名稱
    TTS_SAMPLE_RATE: int = 24000
    TTS_CHANNELS: int = 1
    TTS_SAMPLE_WIDTH: int = 2
    
    # 網站配置
    SITE_TITLE: str = "最新 arXiv AI 論文"
    SITE_DESCRIPTION: str = "每小時更新的 arXiv AI 論文中文摘要，支援文字和語音閱讀。"
    UPDATE_INTERVAL_HOURS: int = 1
    
    @classmethod
    def validate(cls) -> None:
        """驗證配置的有效性"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY 環境變數未設定")
        
        # 確保必要目錄存在
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.AUDIO_DIR.mkdir(exist_ok=True)
    
    @classmethod
    def get_audio_path(cls, paper_id: str) -> Path:
        """取得音訊檔案路徑"""
        return cls.AUDIO_DIR / f"{paper_id}.wav" 
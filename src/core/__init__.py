"""
AI News 核心模組

這個模組包含了專案的核心元件，包括配置管理、資料模型和自定義異常。
"""

__version__ = "2.0.0"
__author__ = "AI News Team"

from .config import Config
from .models import Paper, PaperTranslation
from .exceptions import AINewsException, TranslationError, AudioGenerationError

__all__ = [
    "Config",
    "Paper", 
    "PaperTranslation",
    "AINewsException",
    "TranslationError", 
    "AudioGenerationError"
] 
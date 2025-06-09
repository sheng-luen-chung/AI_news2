"""
日誌管理工具

提供統一的日誌配置和管理功能。
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
    format_string: Optional[str] = None
) -> None:
    """
    設置日誌系統
    
    Args:
        level: 日誌等級
        log_file: 日誌檔案路徑
        format_string: 日誌格式字串
    """
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # 設置根日誌器
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # 清除現有的處理器
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # 建立格式器
    formatter = logging.Formatter(format_string)
    
    # 控制台處理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # 檔案處理器（如果指定）
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """
    取得日誌器
    
    Args:
        name: 日誌器名稱
        
    Returns:
        配置好的日誌器
    """
    return logging.getLogger(name)


class LoggerMixin:
    """日誌器混合類別"""
    
    @property
    def logger(self) -> logging.Logger:
        """取得當前類別的日誌器"""
        return get_logger(self.__class__.__name__) 
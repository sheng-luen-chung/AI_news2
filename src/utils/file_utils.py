"""
檔案操作工具

提供安全的檔案操作功能。
"""

import os
import json
from pathlib import Path
from typing import Any, Dict

from .logging_utils import get_logger

logger = get_logger(__name__)


def ensure_dir_exists(dir_path: Path) -> None:
    """
    確保目錄存在
    
    Args:
        dir_path: 目錄路徑
    """
    try:
        dir_path.mkdir(parents=True, exist_ok=True)
        logger.debug(f"目錄已確保存在: {dir_path}")
    except Exception as e:
        logger.error(f"建立目錄失敗: {dir_path} - {str(e)}")
        raise


def safe_write_file(file_path: Path, content: str, encoding: str = "utf-8") -> None:
    """
    安全地寫入檔案
    
    Args:
        file_path: 檔案路徑
        content: 檔案內容
        encoding: 編碼格式
    """
    try:
        # 確保父目錄存在
        ensure_dir_exists(file_path.parent)
        
        # 寫入檔案
        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)
        
        logger.debug(f"檔案寫入成功: {file_path}")
        
    except Exception as e:
        logger.error(f"檔案寫入失敗: {file_path} - {str(e)}")
        raise


def safe_read_file(file_path: Path, encoding: str = "utf-8") -> str:
    """
    安全地讀取檔案
    
    Args:
        file_path: 檔案路徑
        encoding: 編碼格式
        
    Returns:
        檔案內容
    """
    try:
        with open(file_path, "r", encoding=encoding) as f:
            content = f.read()
        
        logger.debug(f"檔案讀取成功: {file_path}")
        return content
        
    except Exception as e:
        logger.error(f"檔案讀取失敗: {file_path} - {str(e)}")
        raise


def safe_write_json(file_path: Path, data: Dict[str, Any]) -> None:
    """
    安全地寫入JSON檔案
    
    Args:
        file_path: 檔案路徑
        data: 要寫入的資料
    """
    try:
        ensure_dir_exists(file_path.parent)
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.debug(f"JSON檔案寫入成功: {file_path}")
        
    except Exception as e:
        logger.error(f"JSON檔案寫入失敗: {file_path} - {str(e)}")
        raise


def safe_read_json(file_path: Path) -> Dict[str, Any]:
    """
    安全地讀取JSON檔案
    
    Args:
        file_path: 檔案路徑
        
    Returns:
        解析後的資料
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        logger.debug(f"JSON檔案讀取成功: {file_path}")
        return data
        
    except Exception as e:
        logger.error(f"JSON檔案讀取失敗: {file_path} - {str(e)}")
        raise


def get_file_size(file_path: Path) -> int:
    """
    取得檔案大小
    
    Args:
        file_path: 檔案路徑
        
    Returns:
        檔案大小（位元組）
    """
    try:
        return file_path.stat().st_size
    except Exception as e:
        logger.error(f"取得檔案大小失敗: {file_path} - {str(e)}")
        return 0


def is_file_empty(file_path: Path) -> bool:
    """
    檢查檔案是否為空
    
    Args:
        file_path: 檔案路徑
        
    Returns:
        檔案是否為空
    """
    return not file_path.exists() or get_file_size(file_path) == 0 
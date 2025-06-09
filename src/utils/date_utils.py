"""
日期處理工具

提供日期和時間相關的工具函式。
"""

from datetime import datetime, timezone
from typing import Optional


def format_timestamp(dt: Optional[datetime] = None, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    格式化時間戳
    
    Args:
        dt: 日期時間物件，預設為當前時間
        format_str: 格式字串
        
    Returns:
        格式化後的時間字串
    """
    if dt is None:
        dt = datetime.now()
    
    return dt.strftime(format_str)


def parse_date(date_str: str, format_str: str = "%Y-%m-%d") -> datetime:
    """
    解析日期字串
    
    Args:
        date_str: 日期字串
        format_str: 格式字串
        
    Returns:
        日期時間物件
    """
    return datetime.strptime(date_str, format_str)


def get_current_timestamp() -> str:
    """
    取得當前時間戳（ISO格式）
    
    Returns:
        ISO格式的時間戳
    """
    return datetime.now().isoformat()


def get_utc_timestamp() -> str:
    """
    取得UTC時間戳（ISO格式）
    
    Returns:
        UTC時間戳
    """
    return datetime.now(timezone.utc).isoformat()


def days_ago(days: int) -> datetime:
    """
    取得幾天前的日期
    
    Args:
        days: 天數
        
    Returns:
        幾天前的日期時間
    """
    from datetime import timedelta
    return datetime.now() - timedelta(days=days)


def is_recent(dt: datetime, hours: int = 24) -> bool:
    """
    檢查日期是否在指定小時內
    
    Args:
        dt: 要檢查的日期時間
        hours: 小時數
        
    Returns:
        是否在指定時間內
    """
    from datetime import timedelta
    return datetime.now() - dt < timedelta(hours=hours)


def format_duration(seconds: float) -> str:
    """
    格式化持續時間
    
    Args:
        seconds: 秒數
        
    Returns:
        格式化後的持續時間字串
    """
    if seconds < 60:
        return f"{seconds:.1f} 秒"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} 分鐘"
    else:
        hours = seconds / 3600
        return f"{hours:.1f} 小時" 
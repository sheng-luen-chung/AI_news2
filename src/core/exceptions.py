"""
自定義異常類別

定義專案中使用的所有自定義異常，提供更好的錯誤處理和除錯資訊。
"""


class AINewsException(Exception):
    """AI News 專案的基礎異常類別"""
    
    def __init__(self, message: str, details: str = None):
        self.message = message
        self.details = details
        super().__init__(self.message)
    
    def __str__(self):
        if self.details:
            return f"{self.message} - 詳細資訊: {self.details}"
        return self.message


class TranslationError(AINewsException):
    """翻譯相關異常"""
    
    def __init__(self, message: str = "翻譯處理失敗", details: str = None):
        super().__init__(message, details)


class AudioGenerationError(AINewsException):
    """音訊生成相關異常"""
    
    def __init__(self, message: str = "音訊生成失敗", details: str = None):
        super().__init__(message, details)


class ArxivFetchError(AINewsException):
    """arXiv 論文抓取相關異常"""
    
    def __init__(self, message: str = "論文抓取失敗", details: str = None):
        super().__init__(message, details)


class StorageError(AINewsException):
    """資料儲存相關異常"""
    
    def __init__(self, message: str = "資料儲存失敗", details: str = None):
        super().__init__(message, details)


class ConfigurationError(AINewsException):
    """配置相關異常"""
    
    def __init__(self, message: str = "配置錯誤", details: str = None):
        super().__init__(message, details) 
"""
配置模組測試

測試配置管理功能。
"""

import os
import sys
from pathlib import Path

# 將 src 加入 Python 路徑
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from src.core.config import Config
from src.core.exceptions import ConfigurationError


class TestConfig:
    """配置類別測試"""
    
    def test_config_paths(self):
        """測試路徑配置"""
        config = Config()
        
        assert config.BASE_DIR.exists()
        assert config.DATA_DIR.name == "data"
        assert config.AUDIO_DIR.name == "audios"
        assert config.WEB_DIR.name == "web"
    
    def test_config_queries(self):
        """測試查詢配置"""
        config = Config()
        
        assert isinstance(config.ARXIV_QUERIES, list)
        assert len(config.ARXIV_QUERIES) > 0
        assert "AI" in config.ARXIV_QUERIES
    
    def test_config_gemini_settings(self):
        """測試 Gemini 配置"""
        config = Config()
        
        assert config.GEMINI_MODEL == "gemini-2.0-flash-001"
        assert 0 <= config.TEMPERATURE <= 1
        assert config.MAX_OUTPUT_TOKENS > 0
    
    def test_get_audio_path(self):
        """測試音訊路徑生成"""
        config = Config()
        
        audio_path = config.get_audio_path("test123")
        assert audio_path.suffix == ".mp3"
        assert "test123" in str(audio_path)
    
    def test_validate_without_api_key(self):
        """測試沒有 API 金鑰時的驗證"""
        original_key = os.environ.get("GEMINI_API_KEY")
        
        # 暫時移除環境變數
        if "GEMINI_API_KEY" in os.environ:
            del os.environ["GEMINI_API_KEY"]
        
        try:
            # 重新建立配置物件
            config = Config()
            config.GEMINI_API_KEY = None
            
            with pytest.raises(ValueError):
                config.validate()
        finally:
            # 恢復環境變數
            if original_key:
                os.environ["GEMINI_API_KEY"] = original_key


if __name__ == "__main__":
    pytest.main([__file__]) 
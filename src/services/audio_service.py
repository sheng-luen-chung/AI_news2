"""
音訊生成服務

使用 Google Text-to-Speech 生成中文語音檔案。
"""

from gtts import gTTS
from pathlib import Path

from ..core.config import Config
from ..core.exceptions import AudioGenerationError
from ..utils.logging_utils import get_logger

logger = get_logger(__name__)


class AudioService:
    """音訊生成服務"""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
    
    def generate_audio(self, text: str, output_path: Path) -> None:
        """
        生成音訊檔案
        
        Args:
            text: 要轉換的文字
            output_path: 輸出檔案路徑
            
        Raises:
            AudioGenerationError: 音訊生成失敗時拋出
        """
        try:
            logger.info(f"正在生成音訊檔案: {output_path.name}")
            
            # 確保輸出目錄存在
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 生成語音
            tts = gTTS(text, lang=self.config.TTS_LANGUAGE)
            tts.save(str(output_path))
            
            logger.info(f"音訊檔案生成成功: {output_path}")
            
        except Exception as e:
            error_msg = f"生成音訊檔案失敗: {str(e)}"
            logger.error(error_msg)
            raise AudioGenerationError(error_msg, str(e))
    
    def validate_audio_file(self, file_path: Path) -> bool:
        """
        驗證音訊檔案是否有效
        
        Args:
            file_path: 音訊檔案路徑
            
        Returns:
            檔案是否有效
        """
        if not file_path.exists():
            return False
        
        if file_path.stat().st_size < 1000:  # 檔案過小
            logger.warning(f"音訊檔案過小: {file_path}")
            return False
        
        return True
    
    def batch_generate_audio(self, text_file_pairs: list) -> list:
        """
        批次生成音訊檔案
        
        Args:
            text_file_pairs: (文字, 檔案路徑) 配對列表
            
        Returns:
            成功生成的檔案路徑列表
        """
        successful_files = []
        
        for text, file_path in text_file_pairs:
            try:
                self.generate_audio(text, file_path)
                successful_files.append(file_path)
            except AudioGenerationError as e:
                logger.error(f"批次生成音訊失敗: {file_path} - {str(e)}")
                continue
        
        return successful_files 
"""
音訊生成服務

使用 Gemini Text-to-Speech 生成中文語音檔案。
"""

from google import genai
from google.genai import types
import wave
import os
from pathlib import Path

from ..core.config import Config
from ..core.exceptions import AudioGenerationError
from ..utils.logging_utils import get_logger

logger = get_logger(__name__)


class AudioService:
    """音訊生成服務"""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        
        # 初始化 Gemini 客戶端
        if not self.config.GEMINI_API_KEY:
            raise AudioGenerationError("GEMINI_API_KEY 環境變數未設定")
        
        self.client = genai.Client(api_key=self.config.GEMINI_API_KEY)
    
    def _save_wave_file(self, filename: str, pcm_data: bytes, channels: int = None, 
                       rate: int = None, sample_width: int = None) -> None:
        """
        儲存 PCM 資料為 WAV 檔案
        
        Args:
            filename: 輸出檔案名稱
            pcm_data: PCM 音訊資料
            channels: 聲道數
            rate: 取樣率
            sample_width: 取樣寬度（位元組）
        """
        # 使用配置中的預設值
        channels = channels or self.config.TTS_CHANNELS
        rate = rate or self.config.TTS_SAMPLE_RATE
        sample_width = sample_width or self.config.TTS_SAMPLE_WIDTH
        
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            wf.writeframes(pcm_data)
    
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
            logger.info(f"正在使用 Gemini TTS 生成音訊檔案: {output_path.name}")
            
            # 確保輸出目錄存在
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 使用 Gemini TTS 生成語音
            response = self.client.models.generate_content(
                model=self.config.GEMINI_TTS_MODEL,
                contents=text,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name=self.config.GEMINI_TTS_VOICE,
                            )
                        )
                    ),
                )
            )
            
            # 提取音訊資料
            if (response.candidates and 
                response.candidates[0].content and 
                response.candidates[0].content.parts and
                response.candidates[0].content.parts[0].inline_data):
                
                pcm_data = response.candidates[0].content.parts[0].inline_data.data
                
                # 儲存為 WAV 檔案
                self._save_wave_file(str(output_path), pcm_data)
                
                logger.info(f"音訊檔案生成成功: {output_path}")
            else:
                raise AudioGenerationError("無法從 Gemini API 回應中提取音訊資料")
            
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
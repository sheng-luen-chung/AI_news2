"""
Gemini 翻譯服務

使用 Google Gemini API 進行論文翻譯，支援結構化輸出和錯誤重試機制。
"""

import time
from google import genai
from google.genai import types

from ..core.config import Config
from ..core.models import PaperTranslation
from ..core.exceptions import TranslationError, ConfigurationError
from ..utils.logging_utils import get_logger

logger = get_logger(__name__)


class TranslationService:
    """Gemini 翻譯服務"""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self._validate_config()
        self.client = genai.Client(api_key=self.config.GEMINI_API_KEY)
    
    def _validate_config(self):
        """驗證配置"""
        if not self.config.GEMINI_API_KEY:
            raise ConfigurationError("GEMINI_API_KEY 未設定")
    
    def translate_paper(self, title: str, summary: str, max_retries: int = 3) -> PaperTranslation:
        """
        翻譯論文標題和摘要
        
        Args:
            title: 英文標題
            summary: 英文摘要
            max_retries: 最大重試次數
            
        Returns:
            翻譯結果
            
        Raises:
            TranslationError: 翻譯失敗時拋出
        """
        prompt = self._build_translation_prompt(title, summary)
        
        for attempt in range(max_retries):
            try:
                logger.info(f"正在翻譯論文: {title[:50]}...")
                
                response = self.client.models.generate_content(
                    model=self.config.GEMINI_MODEL,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type='application/json',
                        response_schema=PaperTranslation,
                        temperature=self.config.TEMPERATURE,
                        max_output_tokens=self.config.MAX_OUTPUT_TOKENS,
                    ),
                )
                
                translation = response.parsed
                self._validate_translation(translation)
                
                logger.info(f"翻譯成功: {translation.title_zh}")
                return translation
                
            except Exception as e:
                logger.warning(f"翻譯嘗試 {attempt + 1} 失敗: {str(e)}")
                
                if attempt < max_retries - 1:
                    # 延遲重試
                    time.sleep(2 ** attempt)
                    continue
                else:
                    # 最後一次嘗試失敗，返回回退結果
                    logger.error(f"翻譯最終失敗: {str(e)}")
                    return self._create_fallback_translation(title, summary, str(e))
    
    def _build_translation_prompt(self, title: str, summary: str) -> str:
        """建構翻譯提示詞"""
        return (
            f"請將以下arXiv論文標題與摘要翻譯成繁體中文，並完成以下任務：\n"
            f"1. 將摘要濃縮成適合收聽且簡明扼要的中文摘要（約100-150字）。\n"
            f"2. 設想3個「生活化的應用場景」，用簡單易懂的口語描述，讓一般人能理解這項技術的價值。\n"
            f"3. 以「向創投或天使基金推銷」的角度，說明這項技術的重要性與潛在商業價值，盡量發揮創意、大膽預測未來可能性。\n\n"
            f"英文標題：{title}\n"
            f"英文摘要：{summary}\n"
        )
    
    def _validate_translation(self, translation: PaperTranslation) -> None:
        """驗證翻譯結果"""
        if not translation.title_zh or len(translation.title_zh.strip()) < 5:
            raise TranslationError("翻譯標題過短或為空")
        
        if not translation.summary_zh or len(translation.summary_zh.strip()) < 50:
            raise TranslationError("翻譯摘要過短或為空")
        
        if not translation.applications or len(translation.applications) != 3:
            raise TranslationError("應用場景必須恰好有3個")
        
        if not translation.pitch or len(translation.pitch.strip()) < 20:
            raise TranslationError("推銷內容過短或為空")
    
    def _create_fallback_translation(self, title: str, summary: str, error: str) -> PaperTranslation:
        """建立回退翻譯結果"""
        return PaperTranslation(
            title_zh=f"[翻譯失敗] {title}",
            summary_zh=f"摘要翻譯失敗：{error}",
            applications=[
                "應用場景1：翻譯失敗，請參考原文",
                "應用場景2：翻譯失敗，請參考原文", 
                "應用場景3：翻譯失敗，請參考原文"
            ],
            pitch=f"推銷內容翻譯失敗：{error}"
        )
    
    def batch_translate(self, papers: list) -> list:
        """
        批次翻譯多篇論文
        
        Args:
            papers: 論文列表
            
        Returns:
            翻譯結果列表
        """
        results = []
        
        for i, paper in enumerate(papers):
            logger.info(f"正在處理第 {i+1}/{len(papers)} 篇論文")
            
            try:
                translation = self.translate_paper(paper.title, paper.summary)
                results.append((paper, translation, None))
            except Exception as e:
                logger.error(f"翻譯論文 {paper.id} 失敗: {str(e)}")
                results.append((paper, None, str(e)))
        
        return results 
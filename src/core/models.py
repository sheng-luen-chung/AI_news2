"""
資料模型

定義專案中使用的所有資料結構，包括論文資訊和翻譯結果。
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class Paper(BaseModel):
    """arXiv 論文資料模型"""
    
    query: str = Field(description="搜尋關鍵字")
    id: str = Field(description="論文ID")
    url: str = Field(description="論文URL")
    title: str = Field(description="英文標題")
    summary: str = Field(description="英文摘要")
    authors: List[str] = Field(description="作者列表")
    published_date: str = Field(description="發布日期")
    timestamp: Optional[str] = Field(default=None, description="處理時間戳")
    
    # 翻譯結果
    title_zh: Optional[str] = Field(default=None, description="中文標題")
    summary_zh: Optional[str] = Field(default=None, description="中文摘要")
    applications: Optional[List[str]] = Field(default=None, description="應用場景")
    pitch: Optional[str] = Field(default=None, description="推銷內容")
    audio: Optional[str] = Field(default=None, description="音訊檔案路徑")
    
    def add_translation(self, translation: 'PaperTranslation', audio_path: str) -> None:
        """新增翻譯結果到論文物件"""
        self.title_zh = translation.title_zh
        self.summary_zh = translation.summary_zh
        self.applications = translation.applications
        self.pitch = translation.pitch
        self.audio = audio_path
        self.timestamp = datetime.now().isoformat()
    
    @property
    def is_translated(self) -> bool:
        """檢查是否已翻譯"""
        return self.title_zh is not None


class PaperTranslation(BaseModel):
    """論文翻譯結果的結構化模型"""
    
    title_zh: str = Field(description="論文的繁體中文標題")
    summary_zh: str = Field(description="適合收聽的簡明中文摘要")
    applications: List[str] = Field(
        description="三個生活化應用場景的描述",
        min_items=3,
        max_items=3
    )
    pitch: str = Field(description="向創投或天使基金推銷的內容")
    
    def get_audio_content(self) -> str:
        """產生完整的音訊內容"""
        return (
            f"{self.title_zh}\n\n"
            f"{self.summary_zh}\n\n"
            f"這項技術有三個生活化的應用場景：\n"
            f"第一，{self.applications[0]}\n"
            f"第二，{self.applications[1]}\n" 
            f"第三，{self.applications[2]}\n\n"
            f"如果向創投或天使基金推銷，可以這樣說：\n{self.pitch}"
        )


class NewsUpdate(BaseModel):
    """新聞更新統計模型"""
    
    total_fetched: int = Field(description="總共抓取的論文數量")
    successfully_translated: int = Field(description="成功翻譯的論文數量")
    failed_translations: int = Field(description="翻譯失敗的論文數量")
    audio_generated: int = Field(description="成功生成音訊的論文數量")
    update_time: str = Field(description="更新時間")
    
    @property
    def success_rate(self) -> float:
        """計算成功率"""
        if self.total_fetched == 0:
            return 0.0
        return self.successfully_translated / self.total_fetched 
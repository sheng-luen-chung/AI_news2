"""
AI News 主執行腳本

重構後的主程式入口，使用新的服務導向架構。
"""

import sys
from datetime import datetime
from pathlib import Path

# 將 src 加入 Python 路徑
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.config import Config
from src.core.models import NewsUpdate
from src.services.arxiv_service import ArxivService
from src.services.translation_service import TranslationService
from src.services.audio_service import AudioService
from src.services.storage_service import StorageService
from src.utils.logging_utils import setup_logging, get_logger


def main():
    """主執行函式"""
    # 設置日誌
    setup_logging()
    logger = get_logger(__name__)
    
    logger.info("=== AI News 更新開始 ===")
    start_time = datetime.now()
    
    try:
        # 初始化配置
        config = Config()
        config.validate()
        
        # 初始化服務
        arxiv_service = ArxivService(config)
        translation_service = TranslationService(config)
        audio_service = AudioService(config) 
        storage_service = StorageService(config)
        
        # 載入已處理的論文ID
        processed_ids = storage_service.load_processed_ids()
        logger.info(f"已載入 {len(processed_ids)} 個已處理的論文ID")
        
        # 抓取新論文
        papers = arxiv_service.fetch_papers(processed_ids)
        
        if not papers:
            logger.info("沒有新論文，結束更新")
            return
        
        # 初始化統計
        stats = NewsUpdate(
            total_fetched=len(papers),
            successfully_translated=0,
            failed_translations=0,
            audio_generated=0,
            update_time=datetime.now().isoformat()
        )
        
        # 處理每篇論文
        for i, paper in enumerate(papers, 1):
            logger.info(f"處理第 {i}/{len(papers)} 篇論文: {paper.title[:50]}...")
            
            try:
                # 翻譯論文
                translation = translation_service.translate_paper(paper.title, paper.summary)
                stats.successfully_translated += 1
                
                # 生成音訊
                audio_path = config.get_audio_path(paper.id)
                audio_service.generate_audio(translation.get_audio_content(), audio_path)
                stats.audio_generated += 1
                
                # 更新論文物件
                # 確保路徑使用正斜線，避免 JavaScript 處理問題
                relative_path = audio_path.relative_to(config.BASE_DIR)
                web_friendly_path = str(relative_path).replace("\\", "/")
                paper.add_translation(translation, web_friendly_path)
                
                # 儲存論文資料
                storage_service.save_paper(paper)
                
                # 更新已處理ID
                processed_ids.add(paper.id)
                
                logger.info(f"成功處理論文: {paper.title_zh}")
                
            except Exception as e:
                logger.error(f"處理論文 {paper.id} 失敗: {str(e)}")
                stats.failed_translations += 1
                continue
        
        # 儲存更新的已處理ID
        storage_service.save_processed_ids(processed_ids)
        
        # 輸出統計
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        logger.info("=== 更新統計 ===")
        logger.info(f"總抓取論文數: {stats.total_fetched}")
        logger.info(f"成功翻譯數: {stats.successfully_translated}")
        logger.info(f"翻譯失敗數: {stats.failed_translations}")
        logger.info(f"音訊生成數: {stats.audio_generated}")
        logger.info(f"成功率: {stats.success_rate:.2%}")
        logger.info(f"處理時間: {duration:.1f} 秒")
        logger.info("=== AI News 更新完成 ===")
        
    except Exception as e:
        logger.error(f"程式執行失敗: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main() 
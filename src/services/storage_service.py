"""
資料儲存服務

負責處理論文資料的讀取、儲存和管理。
"""

import json
from typing import Set, List, Optional
from pathlib import Path

from ..core.config import Config
from ..core.models import Paper
from ..core.exceptions import StorageError
from ..utils.logging_utils import get_logger

logger = get_logger(__name__)


class StorageService:
    """資料儲存服務"""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
    
    def load_processed_ids(self) -> Set[str]:
        """
        載入已處理的論文ID
        
        Returns:
            已處理的論文ID集合
        """
        try:
            if not self.config.PROCESSED_IDS_FILE.exists():
                logger.info("已處理ID檔案不存在，返回空集合")
                return set()
            
            with open(self.config.PROCESSED_IDS_FILE, "r", encoding="utf-8") as f:
                ids = set(line.strip() for line in f.readlines() if line.strip())
            
            logger.info(f"載入 {len(ids)} 個已處理的論文ID")
            return ids
            
        except Exception as e:
            logger.error(f"載入已處理ID失敗: {str(e)}")
            return set()
    
    def save_processed_ids(self, ids: Set[str]) -> None:
        """
        儲存已處理的論文ID
        
        Args:
            ids: 論文ID集合
            
        Raises:
            StorageError: 儲存失敗時拋出
        """
        try:
            # 確保目錄存在
            self.config.PROCESSED_IDS_FILE.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config.PROCESSED_IDS_FILE, "w", encoding="utf-8") as f:
                f.write("\n".join(sorted(ids)))
            
            logger.info(f"已儲存 {len(ids)} 個論文ID")
            
        except Exception as e:
            error_msg = f"儲存已處理ID失敗: {str(e)}"
            logger.error(error_msg)
            raise StorageError(error_msg, str(e))
    
    def save_paper(self, paper: Paper) -> None:
        """
        儲存論文資料到JSONL檔案
        
        Args:
            paper: 論文物件
            
        Raises:
            StorageError: 儲存失敗時拋出
        """
        try:
            # 確保目錄存在
            self.config.NEWS_FILE.parent.mkdir(parents=True, exist_ok=True)
            
            # 將論文資料附加到檔案末尾
            with open(self.config.NEWS_FILE, "a", encoding="utf-8") as f:
                paper_data = paper.model_dump()
                f.write(json.dumps(paper_data, ensure_ascii=False) + "\n")
            
            logger.debug(f"論文資料已儲存: {paper.id}")
            
        except Exception as e:
            error_msg = f"儲存論文資料失敗: {str(e)}"
            logger.error(error_msg)
            raise StorageError(error_msg, str(e))
    
    def load_papers(self, limit: Optional[int] = None) -> List[Paper]:
        """
        載入論文資料
        
        Args:
            limit: 限制載入的論文數量
            
        Returns:
            論文列表
        """
        papers = []
        
        try:
            if not self.config.NEWS_FILE.exists():
                logger.info("新聞檔案不存在，返回空列表")
                return papers
            
            with open(self.config.NEWS_FILE, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    if limit and len(papers) >= limit:
                        break
                    
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        paper_data = json.loads(line)
                        paper = Paper(**paper_data)
                        papers.append(paper)
                    except json.JSONDecodeError as e:
                        logger.warning(f"解析第 {line_num} 行失敗: {str(e)}")
                        continue
                    except Exception as e:
                        logger.warning(f"建立論文物件失敗 (第 {line_num} 行): {str(e)}")
                        continue
            
            logger.info(f"載入 {len(papers)} 篇論文")
            return papers
            
        except Exception as e:
            logger.error(f"載入論文資料失敗: {str(e)}")
            return papers
    
    def get_paper_by_id(self, paper_id: str) -> Optional[Paper]:
        """
        根據ID取得特定論文
        
        Args:
            paper_id: 論文ID
            
        Returns:
            論文物件或None
        """
        papers = self.load_papers()
        
        for paper in papers:
            if paper.id == paper_id:
                return paper
        
        return None
    
    def backup_data(self, backup_path: Optional[Path] = None) -> Path:
        """
        備份資料檔案
        
        Args:
            backup_path: 備份檔案路徑
            
        Returns:
            備份檔案路徑
        """
        import shutil
        from datetime import datetime
        
        if backup_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.config.DATA_DIR / f"backup_{timestamp}.jsonl"
        
        try:
            shutil.copy2(self.config.NEWS_FILE, backup_path)
            logger.info(f"資料已備份到: {backup_path}")
            return backup_path
            
        except Exception as e:
            error_msg = f"資料備份失敗: {str(e)}"
            logger.error(error_msg)
            raise StorageError(error_msg, str(e)) 
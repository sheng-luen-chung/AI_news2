"""
arXiv 論文抓取服務

負責從 arXiv 抓取最新的 AI 論文，並過濾已處理的論文。
"""

import arxiv
from typing import List, Set
from datetime import datetime

from ..core.config import Config
from ..core.models import Paper
from ..core.exceptions import ArxivFetchError
from ..utils.logging_utils import get_logger

logger = get_logger(__name__)


class ArxivService:
    """arXiv 論文抓取服務"""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.client = arxiv.Client()
    
    def fetch_papers(self, processed_ids: Set[str]) -> List[Paper]:
        """
        抓取新論文
        
        Args:
            processed_ids: 已處理的論文ID集合
            
        Returns:
            新論文列表
            
        Raises:
            ArxivFetchError: 抓取失敗時拋出
        """
        papers = []
        
        try:
            for query in self.config.ARXIV_QUERIES:
                logger.info(f"正在抓取 {query} 相關論文...")
                query_papers = self._fetch_papers_by_query(query, processed_ids)
                papers.extend(query_papers)
                
                if query_papers:
                    logger.info(f"從 {query} 抓取到 {len(query_papers)} 篇新論文")
                
        except Exception as e:
            raise ArxivFetchError(f"抓取論文時發生錯誤", str(e))
        
        logger.info(f"總共抓取到 {len(papers)} 篇新論文")
        return papers
    
    def _fetch_papers_by_query(self, query: str, processed_ids: Set[str]) -> List[Paper]:
        """
        根據查詢字串抓取論文
        
        Args:
            query: 搜尋關鍵字
            processed_ids: 已處理的論文ID集合
            
        Returns:
            論文列表
        """
        papers = []
        
        search = arxiv.Search(
            query=f'"{query}"',
            max_results=self.config.MAX_RESULTS_PER_QUERY,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        for result in self.client.results(search):
            paper_id = result.get_short_id()
            
            # 跳過已處理的論文
            if paper_id in processed_ids:
                continue
            
            paper = Paper(
                query=query,
                id=paper_id,
                url=result.entry_id,
                title=result.title,
                summary=result.summary,
                authors=[author.name for author in result.authors],
                published_date=result.published.strftime("%Y-%m-%d")
            )
            
            papers.append(paper)
            processed_ids.add(paper_id)
            
            # 每個查詢只抓取一篇新論文
            break
        
        return papers
    
    def validate_paper(self, paper: Paper) -> bool:
        """
        驗證論文資料的完整性
        
        Args:
            paper: 論文物件
            
        Returns:
            驗證是否通過
        """
        required_fields = ['id', 'title', 'summary', 'authors']
        
        for field in required_fields:
            if not getattr(paper, field, None):
                logger.warning(f"論文 {paper.id} 缺少必要欄位: {field}")
                return False
        
        if len(paper.summary) < 50:
            logger.warning(f"論文 {paper.id} 摘要過短")
            return False
        
        return True 
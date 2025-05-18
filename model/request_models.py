"""The base request models for the API"""

from pydantic import BaseModel, Field
from typing import Optional


class ArticleSearchRequest(BaseModel):
    """Article search request Model"""
    keyword: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    domain: Optional[str] = None
    country: Optional[str] = None
    language: Optional[str] = None
    maxrecords: Optional[int] = 100

class TimelineRequest(ArticleSearchRequest):
    """Timeline search request Model"""
    mode: str

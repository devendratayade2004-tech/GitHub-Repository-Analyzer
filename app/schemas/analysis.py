from pydantic import BaseModel, HttpUrl
from typing import Dict, Optional, List, Any
from datetime import datetime

class AnalysisBase(BaseModel):
    repo_url: str

class AnalysisCreate(AnalysisBase):
    pass

class AnalysisResponse(AnalysisBase):
    id: int
    repo_name: str
    owner: str
    stars: int
    forks: int
    open_issues: int
    contributors_count: int
    top_contributors: Optional[List[Dict[str, Any]]] = None
    health_score: float
    languages: Dict[str, float]
    created_at: datetime

    class Config:
        from_attributes = True

class RepoURLInput(BaseModel):
    url: str

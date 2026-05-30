from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from datetime import datetime
from app.db.session import Base

class AnalysisHistory(Base):
    __tablename__ = "analysis_history"

    id = Column(Integer, primary_key=True, index=True)
    repo_url = Column(String, index=True)
    repo_name = Column(String)
    owner = Column(String)
    stars = Column(Integer)
    forks = Column(Integer)
    open_issues = Column(Integer)
    contributors_count = Column(Integer)
    top_contributors = Column(JSON) # Store list of contributor dicts
    health_score = Column(Float)
    languages = Column(JSON)  # Store as a dictionary
    created_at = Column(DateTime, default=datetime.utcnow)

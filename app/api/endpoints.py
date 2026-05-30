from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.analysis import AnalysisHistory
from app.schemas.analysis import AnalysisResponse, RepoURLInput
from app.services.analysis_service import analysis_service
from app.services.export_service import export_service

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_repository(input_data: RepoURLInput, db: Session = Depends(get_db)):
    try:
        # Analyze the repo
        analysis_data = await analysis_service.analyze_repo(input_data.url)
        
        # Save to database
        db_analysis = AnalysisHistory(
            repo_url=analysis_data["repo_url"],
            repo_name=analysis_data["repo_name"],
            owner=analysis_data["owner"],
            stars=analysis_data["stars"],
            forks=analysis_data["forks"],
            open_issues=analysis_data["open_issues"],
            contributors_count=analysis_data["contributors_count"],
            top_contributors=analysis_data["top_contributors"],
            health_score=analysis_data["health_score"],
            languages=analysis_data["languages"]
        )
        db.add(db_analysis)
        db.commit()
        db.refresh(db_analysis)
        
        return db_analysis
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/history", response_model=List[AnalysisResponse])
def get_history(db: Session = Depends(get_db)):
    return db.query(AnalysisHistory).order_by(AnalysisHistory.created_at.desc()).limit(10).all()

@router.get("/export/{analysis_id}")
async def export_to_pdf(analysis_id: int, db: Session = Depends(get_db)):
    analysis = db.query(AnalysisHistory).filter(AnalysisHistory.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    pdf_buffer = export_service.generate_repo_pdf(analysis)
    
    headers = {
        'Content-Disposition': f'attachment; filename="{analysis.owner}_{analysis.repo_name}_report.pdf"'
    }
    return Response(content=pdf_buffer.getvalue(), media_type="application/pdf", headers=headers)

import pandas as pd
from typing import Dict, Any
from app.services.github_service import github_service

class AnalysisService:
    @staticmethod
    def calculate_health_score(repo_data: Dict[str, Any], contributors_count: int, recent_commits: int) -> float:
        """
        Calculate health score based on:
        - Popularity: Stars, Forks (40%)
        - Activity: Recent commits, Contributors (40%)
        - Maintenance: Open issues (20%) - fewer issues relative to stars is better
        """
        stars = repo_data.get("stargazers_count", 0)
        forks = repo_data.get("forks_count", 0)
        open_issues = repo_data.get("open_issues_count", 0)
        
        # Normalize scores (0-100)
        # These are arbitrary weights for demonstration
        popularity_score = min(100, (stars * 0.5 + forks * 2) / 10)
        activity_score = min(100, (contributors_count * 5 + recent_commits * 10))
        
        # Issue score: Higher is better (meaning fewer issues per star)
        if stars > 0:
            issue_ratio = open_issues / stars
            maintenance_score = max(0, 100 - (issue_ratio * 1000))
        else:
            maintenance_score = 50 # Neutral
            
        health_score = (popularity_score * 0.4) + (activity_score * 0.4) + (maintenance_score * 0.2)
        return round(min(100, health_score), 2)

    async def analyze_repo(self, repo_url: str) -> Dict[str, Any]:
        # Parse URL
        # Expected format: https://github.com/owner/repo
        parts = repo_url.strip("/").split("/")
        if len(parts) < 2:
            raise ValueError("Invalid GitHub URL")
        
        owner, repo = parts[-2], parts[-1]
        
        # Fetch data
        repo_data = await github_service.get_repo_details(owner, repo)
        languages = await github_service.get_languages(owner, repo)
        contributors_count = await github_service.get_contributors_count(owner, repo)
        top_contributors_data = await github_service.get_top_contributors(owner, repo)
        recent_commits = await github_service.get_recent_commits_count(owner, repo)
        
        # Format top contributors
        top_contributors = [
            {
                "login": c["login"],
                "contributions": c["contributions"],
                "avatar_url": c["avatar_url"],
                "html_url": c["html_url"]
            }
            for c in top_contributors_data
        ]
        
        # Calculate health score
        health_score = self.calculate_health_score(repo_data, contributors_count, recent_commits)
        
        # Use Pandas for language distribution (optional but requested)
        df_langs = pd.Series(languages)
        lang_distribution = {}
        if not df_langs.empty:
            total_bytes = df_langs.sum()
            lang_distribution = (df_langs / total_bytes * 100).round(2).to_dict()

        return {
            "repo_url": repo_url,
            "repo_name": repo,
            "owner": owner,
            "stars": repo_data.get("stargazers_count", 0),
            "forks": repo_data.get("forks_count", 0),
            "open_issues": repo_data.get("open_issues_count", 0),
            "contributors_count": contributors_count,
            "top_contributors": top_contributors,
            "health_score": health_score,
            "languages": lang_distribution,
            "description": repo_data.get("description", ""),
        }

analysis_service = AnalysisService()

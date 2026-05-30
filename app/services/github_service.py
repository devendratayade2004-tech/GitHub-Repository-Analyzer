import httpx
from typing import Dict, Any, List
from app.core.config import settings

class GitHubService:
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        if settings.GITHUB_TOKEN:
            self.headers["Authorization"] = f"token {settings.GITHUB_TOKEN}"

    async def get_repo_details(self, owner: str, repo: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def get_languages(self, owner: str, repo: str) -> Dict[str, int]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}/languages",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def get_contributors_count(self, owner: str, repo: str) -> int:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}/contributors?per_page=1",
                headers=self.headers
            )
            if response.status_code == 200:
                if "Link" in response.headers:
                    links = response.headers["Link"]
                    if 'rel="last"' in links:
                        last_link = [l for l in links.split(",") if 'rel="last"' in l][0]
                        count = int(last_link.split("page=")[-1].split(">")[0])
                        return count
                return len(response.json())
            return 0

    async def get_top_contributors(self, owner: str, repo: str, limit: int = 10) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}/contributors?per_page={limit}",
                headers=self.headers
            )
            if response.status_code == 200:
                return response.json()
            return []

    async def get_recent_commits_count(self, owner: str, repo: str) -> int:
        # Fetching commits from the last 30 days
        import datetime
        since = (datetime.datetime.now() - datetime.timedelta(days=30)).isoformat()
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}/commits?since={since}&per_page=1",
                headers=self.headers
            )
            if response.status_code == 200:
                if "Link" in response.headers:
                    links = response.headers["Link"]
                    if 'rel="last"' in links:
                        last_link = [l for l in links.split(",") if 'rel="last"' in l][0]
                        count = int(last_link.split("page=")[-1].split(">")[0])
                        return count
                return len(response.json())
            return 0

github_service = GitHubService()

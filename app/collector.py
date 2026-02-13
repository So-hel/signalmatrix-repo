import requests
import os
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

load_dotenv()

class GitHubCollector:
    def __init__(self, token: str = None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        } if self.token else {
            "Accept": "application/vnd.github.v3+json"
        }

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 403 and "X-RateLimit-Remaining" in response.headers:
            if response.headers["X-RateLimit-Remaining"] == "0":
                raise Exception("GitHub API rate limit exceeded.")
        
        response.raise_for_status()
        return response.json()

    def get_user(self, username: str) -> Dict:
        return self._get(f"users/{username}")

    def get_repos(self, username: str) -> List[Dict]:
        return self._get(f"users/{username}/repos", params={"sort": "updated", "per_page": 100})

    def get_languages(self, owner: str, repo: str) -> Dict:
        return self._get(f"repos/{owner}/{repo}/languages")

    def get_contents(self, owner: str, repo: str, path: str = "") -> List[Dict]:
        try:
            return self._get(f"repos/{owner}/{repo}/contents/{path}")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return []
            raise

    def get_commits(self, owner: str, repo: str) -> List[Dict]:
        return self._get(f"repos/{owner}/{repo}/commits", params={"per_page": 30})

    def get_pulls(self, owner: str, repo: str) -> List[Dict]:
        return self._get(f"repos/{owner}/{repo}/pulls", params={"state": "all", "per_page": 30})

    def get_issues(self, owner: str, repo: str) -> List[Dict]:
        return self._get(f"repos/{owner}/{repo}/issues", params={"state": "all", "per_page": 30})

    def get_releases(self, owner: str, repo: str) -> List[Dict]:
        return self._get(f"repos/{owner}/{repo}/releases")

    def get_workflow_files(self, owner: str, repo: str) -> List[Dict]:
        return self.get_contents(owner, repo, ".github/workflows")

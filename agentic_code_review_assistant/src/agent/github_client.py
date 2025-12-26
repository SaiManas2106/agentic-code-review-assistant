import os, requests
from typing import Dict, Any, List

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

class GitHubClient:
    def __init__(self, token: str = None):
        self.token = token or GITHUB_TOKEN
        if not self.token:
            raise ValueError('GitHub token required. Provide via GITHUB_TOKEN env var.')

    def _headers(self):
        return {'Authorization': f'token {self.token}', 'Accept': 'application/vnd.github.v3+json'}

    def get_pr_files(self, repo_full_name: str, pr_number: int) -> List[Dict[str, Any]]:
        url = f'https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}/files'
        resp = requests.get(url, headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_pr_comments(self, repo_full_name: str, pr_number: int):
        url = f'https://api.github.com/repos/{repo_full_name}/issues/{pr_number}/comments'
        resp = requests.get(url, headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()

from .github_client import GitHubClient
from .summarizer import Summarizer
from .storage import Storage
from langchain.embeddings import OpenAIEmbeddings
import os
from typing import List, Dict

EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'text-embedding-3-small')

class AgentCore:
    def __init__(self, github_token=None):
        self.gh = GitHubClient(github_token)
        self.summarizer = Summarizer()
        self.storage = Storage()
        self.embedder = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    def _embed_texts(self, texts: List[str]):
        # returns list of vectors
        return self.embedder.embed_documents(texts)

    def analyze_pr(self, repo_full_name: str, pr_number: int) -> Dict:
        files = self.gh.get_pr_files(repo_full_name, pr_number)
        # prepare textual contents to embed (file path + patch)
        docs = []
        for f in files:
            content = f.get('patch') or f.get('contents_url') or f.get('filename')
            docs.append(f"FILE: {f.get('filename')}\n{content}")

        # just-in-time retrieval: embed current PR and search similar docs
        vectors = self._embed_texts(docs)
        # store vectors for future sessions (simple upsert)
        try:
            self.storage.upsert(vectors)
        except Exception as e:
            # if Qdrant not available, continue gracefully
            print('Storage upsert failed:', e)

        # Summarize for post-session memory
        summary = self.summarizer.summarize_changes(docs)

        # Build a short report
        report = {
            'num_files': len(files),
            'summary': summary,
            'files': [f.get('filename') for f in files]
        }
        return report

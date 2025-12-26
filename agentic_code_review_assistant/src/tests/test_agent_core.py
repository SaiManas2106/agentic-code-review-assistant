import pytest
from agent.agent_core import AgentCore
from unittest.mock import patch, MagicMock

class DummyGitHub:
    def __init__(self):
        pass
    def get_pr_files(self, repo_full_name, pr_number):
        return [{'filename': 'a.py', 'patch': 'def foo(): pass'}, {'filename': 'b.py', 'patch': 'def bar(): pass'}]

class DummyEmbed:
    def __init__(self):
        pass
    def embed_documents(self, texts):
        return [[0.1]*1536 for _ in texts]

@patch('agent.agent_core.GitHubClient', autospec=True)
@patch('agent.agent_core.OpenAIEmbeddings', autospec=True)
@patch('agent.agent_core.Storage', autospec=True)
@patch('agent.agent_core.Summarizer', autospec=True)
def test_analyze_pr(mock_summarizer, mock_storage, mock_embeddings, mock_gh):
    mock_gh.return_value = DummyGitHub()
    mock_embeddings.return_value = DummyEmbed()
    mock_storage.return_value = MagicMock()
    mock_summarizer.return_value = MagicMock(summarize_changes=lambda files: 'short summary')
    agent = AgentCore(github_token='dummy')
    report = agent.analyze_pr('owner/repo', 1)
    assert report['num_files'] == 2
    assert 'summary' in report

# Agentic Code Review Assistant with Memory Persistence

This project implements an agent that analyzes GitHub pull requests across sessions while maintaining context about project conventions and historical review patterns.
It demonstrates a hybrid context strategy combining pre-loaded style guides with just-in-time (JIT) retrieval via Qdrant, plus post-session summary generation for memory persistence.

## Features
- Connect to GitHub to fetch PR files and metadata
- Use embeddings and Qdrant for semantic retrieval (JIT)
- Maintain compressed session summaries for future initialization
- Simple FastAPI server to trigger analysis on-demand
- PyTest tests and GitHub Actions CI

## Requirements
- Python 3.10+
- Docker & docker-compose (for running Qdrant locally)
- GitHub token with `repo` read access
- OpenAI API key (or any LLM compatible with LangChain)

See `.env.example` for environment variables and `docker-compose.yml` to start Qdrant locally.

## Quickstart (local)
1. Copy `.env.example` -> `.env` and fill in keys.
2. Start Qdrant:
   ```bash
   docker-compose up -d
   ```
3. Create virtualenv and install deps:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
   python -m src.app
   ```
5. Use `/analyze_pr` endpoint (see README for details).



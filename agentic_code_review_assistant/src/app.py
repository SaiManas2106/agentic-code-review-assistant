from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from agent.agent_core import AgentCore

load_dotenv()

app = FastAPI(title='Agentic Code Review Assistant')

class PRRequest(BaseModel):
    repo_full_name: str
    pr_number: int

agent = AgentCore()

@app.post('/analyze_pr')
async def analyze_pr(req: PRRequest):
    try:
        result = agent.analyze_pr(req.repo_full_name, req.pr_number)
        return {'status': 'ok', 'result': result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('src.app:app', host='0.0.0.0', port=8000, reload=True)

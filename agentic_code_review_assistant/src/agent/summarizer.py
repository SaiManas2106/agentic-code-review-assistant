from typing import List, Dict
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

LLM_MODEL = os.getenv('LLM_MODEL', 'gpt-4o-mini')

class Summarizer:
    def __init__(self):
        self.llm = ChatOpenAI(model=LLM_MODEL, temperature=0.0)

    def summarize_changes(self, files: List[Dict]) -> str:
        # Create a compact summary of changed files for persistence
        prompt = PromptTemplate(
            input_variables=['files'],
            template='''You are an assistant that summarizes code changes for future agent initialization.
Given the following file diffs or contents: {files}
Produce a concise summary (3-6 lines) of recurring patterns, conventions, and potential tech-debt points.''')
        chain = LLMChain(llm=self.llm, prompt=prompt)
        return chain.run({'files': files})

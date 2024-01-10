from langchain_community.llms import Together
import os
from api.scraper.environment import setup_environment

setup_environment()


def setup_language_model():
    llm = Together(
        model=os.getenv("LLM_PROVIDER_MODEL"),
        temperature=0.5,
        max_tokens=3000,
        top_k=1,
        together_api_key=os.getenv("LLM_PROVIDER_API_KEY"),
    )
    return llm

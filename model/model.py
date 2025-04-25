from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from action.set_api_key import get_api_key, set_api_key

load_dotenv()

def model():
    openai_api_key = get_api_key() or os.getenv("OPENAI_API_KEY")
    if not openai_api_key or not openai_api_key.startswith("sk-"):
        raise ValueError("OPENAI_API_KEY environment variable not set or invalid")
    return ChatOpenAI(model="gpt-4o", api_key=openai_api_key)
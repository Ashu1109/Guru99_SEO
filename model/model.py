from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from action.set_api_key import get_api_key, set_api_key

load_dotenv()

def model():
    # First try to get key from memory
    openai_api_key = get_api_key()
    
    # If not in memory, try environment variable
    if not openai_api_key:
        openai_api_key = os.getenv("OPENAI_API_KEY")
    
    # If still not found, try fetching from database
    if not openai_api_key:
        from action.fetch_api_key import fetch_api_key
        openai_api_key = fetch_api_key()
        # If found in database, set it in memory and environment
        if openai_api_key:
            set_api_key(openai_api_key)
    
    # Final check before using
    if not openai_api_key or not openai_api_key.startswith("sk-"):
        raise ValueError("OPENAI_API_KEY environment variable not set or invalid")
    
    return ChatOpenAI(model="gpt-4o", api_key=openai_api_key)
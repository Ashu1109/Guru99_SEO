import os

api_key = ""

def set_api_key(key):
    global api_key
    api_key = key if key is not None else ""
    if key is not None:
        os.environ["OPENAI_API_KEY"] = key
    elif "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]
    
def get_api_key():
    return api_key if api_key else None


def clear_api_key():
    global api_key
    api_key = None
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]
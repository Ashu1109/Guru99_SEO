import requests
from action.get_processed_array import access_token
def get_filtered_links(back_url):
    access_token_ = access_token()
    site_url = 'https://www.guru99.com/'  # Use the exact property URL
    api_url = f'https://www.googleapis.com/webmasters/v3/sites/{requests.utils.quote(site_url, safe="")}/searchAnalytics/query'

    body = {
        "startDate": "2025-04-01",
        "endDate": "2025-04-29",
        "dimensions": ["page"],
        "dimensionFilterGroups": [{
            "filters": [{
                "dimension": "page",
                "operator": "contains",
                "expression": back_url
            }]
        }],
        "rowLimit": 1000
    }

    headers = {
        'Authorization': f'Bearer {access_token_}',
        'Content-Type': 'application/json'
    }

    response = requests.post(api_url, json=body, headers=headers)
    return response.json()


from deep_translator import GoogleTranslator

def translate_text(text, target_language='en'):
    """
    Translate text to the target language with automatic source language detection.
    
    Args:
        text (str): Text to translate
        target_language (str): Target language code (default: 'en' for English)
        show_detection (bool): Whether to show detected language (default: False)
        
    Returns:
        str: Translated text
    """
    try:
        # Skip translation if text is empty
        if not text or text.strip() == "":
            return text
        translator = GoogleTranslator(source='auto', target=target_language)
        translation = translator.translate(text)
        return translation
        
    except Exception as e:
        print(f"Error during translation: {e}")
        return text  # Return original text in case of error

# Example usage
if __name__ == "__main__":
    # Test with multiple languages
    test_phrases = [
        ("Bonjour le monde", "French"),
        ("Hola mundo", "Spanish"),
        ("Ciao mondo", "Italian"),
        ("Hallo Welt", "German"),
        ("你好世界", "Chinese"),
        ("こんにちは世界", "Japanese"),
        ("안녕하세요 세계", "Korean"),
        ("Привет, мир", "Russian"),
        ("مرحبا بالعالم", "Arabic"),
        ("नमस्ते दुनिया", "Hindi"),
        ("Hello world", "English")  # Test with English to see if it detects no translation needed
    ]
    
    # Test translation to English
    print("\n" + "="*80)
    print("TESTING TRANSLATIONS TO ENGLISH:")
    print("="*80)
    
    for phrase, language in test_phrases:
        print("\n" + "-"*50)
        print(f"Testing {language}: \"{phrase}\"")
        translated_text = translate_text(phrase, target_language='en')
        print(f"Translated: \"{translated_text}\"")
        
    # Test translation to other target languages
    print("\n\n" + "="*80)
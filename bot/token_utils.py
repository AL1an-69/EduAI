import tiktoken

def count_tokens(messages, model="claude-3-haiku"):
    """Подсчет токенов для текстовых и мультимодальных сообщений"""
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = 0
    
    for msg in messages:
        content = msg.get("content", "")
        
        # Если content — строка (обычное сообщение)
        if isinstance(content, str):
            tokens += len(encoding.encode(content))
        
        # Если content — список (мультимодальное сообщение с фото)
        elif isinstance(content, list):
            for item in content:
                if item.get("type") == "text":
                    text = item.get("text", "")
                    tokens += len(encoding.encode(text))
                elif item.get("type") == "image_url":
                    # Изображения занимают примерно 85-200 токенов
                    tokens += 85
    
    return tokens

MAX_TOKENS = 40000  # максимальное количество токенов в истории
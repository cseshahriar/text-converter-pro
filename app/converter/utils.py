import secrets


def generate_api_key():
    return secrets.token_urlsafe(32)


def convert_text(text: str, operation: str) -> str:
    'Text conversion utility function'
    if operation == "camel":
        return ''.join(word.capitalize() if i > 0 else word for i, word in enumerate(text.split()))
    elif operation == "pascal":
        return ''.join(word.capitalize() for word in text.split())
    elif operation == "snake":
        return '_'.join(text.lower().split())
    elif operation == "kebab":
        return '-'.join(text.lower().split())
    elif operation == "upper":
        return text.upper()
    elif operation == "lower":
        return text.lower()
    else:
        raise ValueError("Unsupported case type")

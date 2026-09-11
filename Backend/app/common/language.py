from typing import Optional


ERROR_MESSAGES = {
    "Permission denied": {"en": "Permission denied", "kr": "권한이 거부되었습니다"},
    "Resource not found": {"en": "Resource not found", "kr": "리소스를 찾을 수 없습니다"},
    "API exception": {"en": "API exception", "kr": "API 예외"},
    "Internal server error": {
        "en": "Internal server error",
        "kr": "내부 서버 오류",
    },
    "Operation failed": {"en": "Operation failed", "kr": "작업 실패"},
}


def get_message(message: str, language: Optional[str] = None) -> str:
    if not language or language.lower() not in ["en", "kr"]:
        language = "en"
    if message in ERROR_MESSAGES:
        return ERROR_MESSAGES[message].get(language.lower(), ERROR_MESSAGES[message]["en"])
    return message

from typing import Any, Optional

from fastapi import HTTPException

from app.common.language import get_message


class APIException(HTTPException):
    def __init__(
        self,
        code: int = 10000,
        message: str = "API exception",
        status_code: int = 400,
        data: Any = None,
        language: Optional[str] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=get_message(message, language))
        self.code = code
        self.data = data


class ValidationError(APIException):
    def __init__(self, message: str = "Validation error", data: Any = None):
        super().__init__(code=1001, message=message, status_code=400, data=data)


class AuthenticationError(APIException):
    def __init__(self, message: str = "Authentication failed", data: Any = None):
        super().__init__(code=1002, message=message, status_code=401, data=data)


class AuthorizationError(APIException):
    def __init__(self, message: str = "Permission denied", data: Any = None):
        super().__init__(code=1003, message=message, status_code=403, data=data)


class NotFoundError(APIException):
    def __init__(self, message: str = "Resource not found", data: Any = None):
        super().__init__(code=1004, message=message, status_code=404, data=data)


class ServerError(APIException):
    def __init__(self, message: str = "Internal server error", data: Any = None):
        super().__init__(code=1005, message=message, status_code=500, data=data)


class BudgetExceededError(APIException):
    def __init__(self, message: str = "Daily LLM token budget exceeded", data: Any = None, language: Optional[str] = None):
        super().__init__(code=1007, message=message, status_code=429, data=data, language=language)


class LLMServiceError(APIException):
    def __init__(self, message: str = "LLM service unavailable", data: Any = None, language: Optional[str] = None):
        super().__init__(code=1008, message=message, status_code=503, data=data, language=language)


class InputTooLongError(APIException):
    def __init__(self, message: str = "Input exceeds maximum length", data: Any = None, language: Optional[str] = None):
        super().__init__(code=1009, message=message, status_code=400, data=data, language=language)


class ContentReviewError(APIException):
    def __init__(self, message: str = "Generated content failed review", data: Any = None, language: Optional[str] = None):
        super().__init__(code=1010, message=message, status_code=503, data=data, language=language)

from fastapi import HTTPException


class CustomError(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class NotFoundError(CustomError):
    def __init__(self, item: str):
        super().__init__(status_code=404, detail=f"{item} not found.")


class ValidationError(CustomError):
    def __init__(self, field: str, message: str):
        super().__init__(
            status_code=400, detail=f"Validation error on {field}: {message}"
        )


class InternalServiceError(CustomError):
    def __init__(self, message: str = "An internal server error occurred."):
        super().__init__(status_code=500, detail=message)

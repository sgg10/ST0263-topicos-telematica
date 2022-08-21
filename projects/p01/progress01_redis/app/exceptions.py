class HTTPAppException(Exception):
    def __init__(self, message: str, status_code: int, *args, **kwargs) -> None:
        self.message = message
        self.status_code = status_code
    def __str__(self):
        return f"Error {self.status_code} | {self.message}"
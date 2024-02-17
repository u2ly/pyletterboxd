class TitleNotFound(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(f"Title not found: {message}")

class RequestException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(f"Request issue: {message}")
"""Custom exceptions for Gas Station Spain API."""


class GasStationServerUnavailableException(Exception):
    """Exception raised when the gas station server is unavailable or returns an error."""

    def __init__(self, status_code: int, message: str = None):
        self.status_code = status_code
        self.message = message or f"Server returned status code {status_code}"
        super().__init__(self.message)

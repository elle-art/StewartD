class FileProcessingError(Exception):
    """Base exception for file processing errors."""
    def __init__(self, filename, message):
        self.filename = filename
        super().__init__(f"{message} (file: {filename})")

class InvalidDataError(FileProcessingError):
    """Raised when data validation fails."""
    def __init__(self, filename, detail):
        super().__init__(filename, f"Invalid data: {detail}")

class MissingFieldError(FileProcessingError):
    """Raised when a required field is missing."""
    def __init__(self, filename, field):
        super().__init__(filename, f"Missing required field: {field}")

class FileProcessingError(Exception):
    """Base exception for file processing errors."""
    def __init__(self, filename, message):
        self.filename = filename
        super().__init__(f"{message} (file: {filename})")

class InvalidDataError(FileProcessingError):
    """Raised when data validation fails."""
    def __init__(self, detail):
        super(Exception, self).__init__(f"Error INVALID_DATA: {detail}")

class MissingFieldError(FileProcessingError):
    """Raised when a required field is missing."""
    def __init__(self, field):
        super(Exception, self).__init__(f"Error MISSING_FIELD: {field}")

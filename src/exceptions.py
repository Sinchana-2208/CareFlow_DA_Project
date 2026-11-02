class CareFlowException(Exception):
    """Base exception class for all custom CareFlow pipeline errors."""
    pass

class DataValidationError(CareFlowException):
    """Raised when clinical event log data fails structural or hygiene validation checks."""
    def __init__(self, message: str, missing_columns: list = None):
        super().__init__(message)
        self.missing_columns = missing_columns or []

class PipelineExecutionError(CareFlowException):
    """Raised when an unrecoverable failure occurs during stage orchestration."""
    pass
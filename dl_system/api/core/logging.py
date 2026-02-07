import logging
import sys
import json
from datetime import datetime, timezone
from typing import Any, Dict

class JSONFormatter(logging.Formatter):
    """
    Formatter that outputs JSON strings after parsing the LogRecord.
    """
    def format(self, record: logging.LogRecord) -> str:
        log_obj: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add correlation ID if present in thread local storage or record
        if hasattr(record, "request_id"):
            log_obj["request_id"] = record.request_id # type: ignore
        
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_obj)

def setup_logging() -> None:
    """
    Configure root logger to use JSON formatting.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)
    
    # Adjust levels for noisy libraries
    logging.getLogger("uvicorn.access").disabled = True  # Disable default access log to avoid duplication if we add middleware
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    
    # Suppress TensorFlow/Keras warnings
    import os
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2" # FATAL
    os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
    
    logging.getLogger("tensorflow").setLevel(logging.ERROR)
    logging.getLogger("absl").setLevel(logging.ERROR)
    # Filter out specific deprecated warning if needed, though setting level to ERROR should cover it


from utils.audit_logger import AuditLogger
import functools

def robust_skill_execution(fallback_return_value=None, skill_name="Unknown Skill"):
    """
    A decorator to provide error recovery and graceful degradation for skill functions.
    It catches exceptions, logs them, and returns a specified fallback value.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_message = f"Error in {skill_name}.{func.__name__}: {e}"
                print(f"[ERROR HANDLER]: {error_message}")
                AuditLogger.log(
                    event_type="SKILL_ERROR",
                    agent="ErrorHandler",
                    description=error_message,
                    details={"skill": skill_name, "function": func.__name__, "args": args, "kwargs": kwargs}
                )
                return fallback_return_value
        return wrapper
    return decorator

def robust_watcher_process(fallback_action_description="Process skipped due to error"):
    """
    A decorator for watcher processing functions (like process_pending_file)
    to log errors and prevent a single file's issue from stopping the watcher.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_message = f"Error processing file in {func.__name__}: {e}"
                print(f"[ERROR HANDLER]: {error_message}")
                AuditLogger.log(
                    event_type="WATCHER_PROCESSING_ERROR",
                    agent="ErrorHandler",
                    description=error_message,
                    details={"function": func.__name__, "args": args, "kwargs": kwargs}
                )
                # This could also implement moving the file to an error folder
                # or marking it to be re-attempted. For now, it just logs and continues.
        return wrapper
    return decorator

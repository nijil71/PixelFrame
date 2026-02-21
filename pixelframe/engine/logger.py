from rich.console import Console
from rich.logging import RichHandler
import logging

console = Console()

def setup_logger():
    """Set up the PixelFrame logger with Rich handler. Idempotent — safe to call multiple times."""
    logger = logging.getLogger("pixelframe")

    # Avoid adding duplicate handlers on repeated calls
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    handler = RichHandler(rich_tracebacks=True, console=console)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)

    # Prevent log propagation to root logger (avoids duplicate output)
    logger.propagate = False

    return logger
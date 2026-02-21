from rich.console import Console
from rich.logging import RichHandler
import logging

console = Console()

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True)]
    )
    return logging.getLogger("pixelframe")
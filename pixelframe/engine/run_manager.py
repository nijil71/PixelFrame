from pathlib import Path
from datetime import datetime

def create_run_directory(base_output: str) -> Path:
    base_path = Path(base_output)
    base_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    run_path = base_path / f"run-{timestamp}"
    
    (run_path / "screenshots").mkdir(parents=True, exist_ok=True)
    (run_path / "composite").mkdir(parents=True, exist_ok=True)
    (run_path / "report").mkdir(parents=True, exist_ok=True)

    return run_path
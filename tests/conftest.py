import sys
from pathlib import Path
import pytest

# Project root directory resolution
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Ensure scripts and local packages are discoverable
scripts_dir = PROJECT_ROOT / "scripts"
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

from run_pm4py_discovery import load_events  # noqa: E402


@pytest.fixture(scope="session")
def project_root() -> Path:
    """Returns the absolute path to the project root directory."""
    return PROJECT_ROOT


@pytest.fixture(scope="session")
def careflow_data_dir(project_root: Path) -> Path:
    """Returns the path to the careflow data directory."""
    return project_root / "careflow_data"


@pytest.fixture(scope="session")
def event_log_path(careflow_data_dir: Path) -> Path:
    """Points to the clean synthetic event log CSV file."""
    return careflow_data_dir / "clean_event_log.csv"


@pytest.fixture(scope="session")
def loaded_events(event_log_path: Path):
    """Loads and caches parsed events once for the entire test session."""
    if not event_log_path.is_file():
        pytest.skip(f"Event log file not found at: {event_log_path}")
    return load_events(event_log_path)


@pytest.fixture(scope="session")
def dbt_directory(project_root: Path) -> Path:
    """Returns the root path of the dbt subproject."""
    return project_root / "careflow_dbt"
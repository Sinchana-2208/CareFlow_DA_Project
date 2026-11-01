import os
import yaml
from pathlib import Path
from typing import Dict, Any

def load_project_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """
    Load project configuration from YAML and allow environment variable overrides.
    Enables seamless switching between local SQLite development databases and 
    production analytical instances without direct code modifications.
    """
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found at: {path.absolute()}")

    with open(path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}

    # Allow environment variable overrides for critical paths
    if "CAREFLOW_DB_PATH" in os.environ:
        if "database" not in config:
            config["database"] = {}
        config["database"]["path"] = os.environ["CAREFLOW_DB_PATH"]

    if "CAREFLOW_DATA_DIR" in os.environ:
        if "paths" not in config:
            config["paths"] = {}
        config["paths"]["data_dir"] = os.environ["CAREFLOW_DATA_DIR"]

    return configimport os
import yaml
from pathlib import Path
from typing import Dict, Any

def load_project_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """
    Load project configuration from YAML and allow environment variable overrides.
    Enables seamless switching between local SQLite development databases and 
    production analytical instances without direct code modifications.
    """
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found at: {path.absolute()}")

    with open(path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}

    # Allow environment variable overrides for critical paths
    if "CAREFLOW_DB_PATH" in os.environ:
        if "database" not in config:
            config["database"] = {}
        config["database"]["path"] = os.environ["CAREFLOW_DB_PATH"]

    if "CAREFLOW_DATA_DIR" in os.environ:
        if "paths" not in config:
            config["paths"] = {}
        config["paths"]["data_dir"] = os.environ["CAREFLOW_DATA_DIR"]

    return configimport os
import yaml
from pathlib import Path
from typing import Dict, Any

def load_project_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """
    Load project configuration from YAML and allow environment variable overrides.
    Enables seamless switching between local SQLite development databases and 
    production analytical instances without direct code modifications.
    """
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found at: {path.absolute()}")

    with open(path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}

    # Allow environment variable overrides for critical paths
    if "CAREFLOW_DB_PATH" in os.environ:
        if "database" not in config:
            config["database"] = {}
        config["database"]["path"] = os.environ["CAREFLOW_DB_PATH"]

    if "CAREFLOW_DATA_DIR" in os.environ:
        if "paths" not in config:
            config["paths"] = {}
        config["paths"]["data_dir"] = os.environ["CAREFLOW_DATA_DIR"]

    return config
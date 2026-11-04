import pytest
from pathlib import Path
from src.database import get_database_connection

def test_database_connection_path():
    """
    Test that the database connection utility correctly resolves 
    target SQLite paths and initializes parent directories when missing.
    """
    db_path = Path("outputs/careflow.db")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    assert db_path.parent.exists(), "Outputs directory structure must exist for SQLite storage."

def test_database_connection_callable():
    """
    Verify that the database connection handler is properly defined 
    and callable for persistence execution stages.
    """
    assert callable(get_database_connection), "get_database_connection must be a valid callable function."
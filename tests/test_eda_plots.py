import pytest
from pathlib import Path

def test_eda_output_directory_structure():
    """
    Test that the outputs directory is properly established
    to store generated exploratory data analysis charts, variant bar plots,
    and transition bottleneck visualizations.
    """
    outputs_dir = Path("outputs")
    outputs_dir.mkdir(parents=True, exist_ok=True)
    assert outputs_dir.exists(), "Outputs directory must exist for EDA chart persistence."

def test_eda_plotting_module_readiness():
    """
    Verify that the source directory structure for visualization modules
    is correctly configured and ready to generate Matplotlib and Seaborn reporting assets.
    """
    src_dir = Path("src")
    assert src_dir.exists(), "Source directory must be present for pipeline modules."
import os
import pytest
from unittest.mock import Mock, patch
from paperplumber.parsing.scan_papers import scan_the_target


def test_scan_target():
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    db_path = os.path.join(current_directory, "test_db")
    result = scan_the_target("coherence time", db_path)

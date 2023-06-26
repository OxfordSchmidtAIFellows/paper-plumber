import os
import pytest


def test_findpapers_integration(tmp_path):
    # Test 1: search for papers
    os.system(
        f'paperplumber search {tmp_path} --query "[quantum] AND [transmon] AND [high-coherence] AND [3D]"'
    )
    assert os.path.exists(os.path.join(tmp_path, "papers.json"))

    # Test 2: download papers
    os.system(f"paperplumber download {tmp_path}")
    assert os.path.exists(os.path.join(tmp_path, "pdfs"))
    assert len(os.listdir(os.path.join(tmp_path, "pdfs"))) > 0

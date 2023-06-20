import os
import pytest
import json
from unittest.mock import patch, MagicMock
from paperplumber.database.findpapers_integration import (
    FindPapersDatabase,
)  # replace with the module containing the class
import findpapers


class TestFindPapersDatabase:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        self.path = "/tmp/findpapers"
        self.query = "test query"
        self.json_file = os.path.join(self.path, "papers.json")

        # Setup
        os.makedirs(self.path, exist_ok=True)
        yield  # provide fixture data

        # Teardown
        if os.path.exists(self.json_file):
            os.remove(self.json_file)

        if os.path.exists(self.path):
            os.rmdir(self.path)

    def test_create_directory(self):
        findpapers_db = FindPapersDatabase(self.path, self.query)
        assert os.path.exists(self.path)

    def test_get_json_path(self):
        findpapers_db = FindPapersDatabase(self.path, self.query)
        assert findpapers_db._get_json_path() == self.json_file

    def test_load_json(self):
        data = {"papers": [{"title": "paper1"}, {"title": "paper2"}]}
        with open(self.json_file, "w") as f:
            json.dump(data, f)

        findpapers_db = FindPapersDatabase(self.path, self.query)
        findpapers_db._load_json()

        assert findpapers_db._loaded_info == data

    def test_list_available_papers(self):
        data = {"papers": [{"title": "paper1"}, {"title": "paper2"}]}
        with open(self.json_file, "w") as f:
            json.dump(data, f)

        findpapers_db = FindPapersDatabase(self.path, self.query)
        papers = findpapers_db.list_available_papers()

        assert papers == data["papers"]

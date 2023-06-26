""" A wrapper module for the findpapers (https://github.com/jonatasgrosman/findpapers) package"""

import os
import json
from typing import Any, Dict, List
import functools
import findpapers
from paperplumber.logger import get_logger

logger = get_logger(__name__)


class FindPapersDatabase:
    """
    A wrapper class for the findpapers
    """

    def __init__(self, path: str) -> None:
        """
        Initializer for the FindPapersDatabase class.

        Args:
            path (str): The path to the directory containing the database files.

        """

        # Create wrapper functions for the findpapers package
        @functools.wraps(findpapers.search)
        def search(**kwargs) -> List[Dict[str, Any]]:
            json_path = self._get_json_path()
            if "outputpath" in kwargs:
                logger.warning(
                    "Findpapers search wrapper:"
                    " The outputpath argument %s will be overwritten by %s.",
                    kwargs["outputpath"],
                    json_path,
                )
            kwargs["outputpath"] = json_path
            return findpapers.search(**kwargs)

        @functools.wraps(findpapers.refine)
        def refine(**kwargs) -> List[Dict[str, Any]]:
            json_path = self._get_json_path()
            if "search_path" in kwargs:
                logger.warning(
                    "Findpapers refine wrapper:"
                    " The search_path argument %s will be overwritten by %s.",
                    kwargs["search_path"],
                    json_path,
                )
            kwargs["search_path"] = json_path
            return findpapers.refine(**kwargs)

        @functools.wraps(findpapers.download)
        def download(**kwargs) -> List[Dict[str, Any]]:
            json_path = self._get_json_path()
            output_directory = os.path.join(self.path, "pdfs")
            if "search_path" in kwargs:
                logger.warning(
                    "Findpapers download wrapper:"
                    " The search_path argument %s will be overwritten by %s.",
                    kwargs["search_path"],
                    json_path,
                )
            if "output_directory" in kwargs:
                logger.warning(
                    "Findpapers download wrapper:"
                    " The search_path argument %s will be overwritten by %s.",
                    kwargs["output_directory"],
                    output_directory,
                )
            kwargs["search_path"] = json_path
            kwargs["output_directory"] = output_directory
            return findpapers.download(**kwargs)

        self.search = search
        self.refine = refine
        self.download = download

        self._loaded_info = None

        # Check if the path is valid
        self.path = path

        # Make dir to that directory
        self._create_directory()

    def _get_json_path(self) -> str:
        """
        Returns the path to the JSON file containing the database information.

        Returns:
            str: The path to the JSON file.
        """
        return os.path.join(self.path, "papers.json")

    def _create_directory(self) -> None:
        """
        Creates a new directory at the specified path if it does not already exist.
        """
        os.makedirs(self.path, exist_ok=True)

    def _load_json(self) -> None:
        """
        Loads a JSON file from the specified path and saves it to the _loaded_info attribute.
        """
        if self._loaded_info is not None:
            return

        with open(
            os.path.join(self.path, "papers.json"), "r", encoding="utf-8"
        ) as file:
            self._loaded_info = json.load(file)

    def list_available_papers(self) -> List[Dict[str, Any]]:
        """
        Returns a list of available papers in the database.

        Returns:
            List[Dict[str, Any]]: The list of papers.
        """
        self._load_json()

        papers = self._loaded_info["papers"]
        return papers

    def list_downloaded_papers(self) -> List[Dict[str, Any]]:
        """
        Returns a list of downloaded papers in the database.

        Returns:
            List[Dict[str, Any]]: The list of papers.
        """
        self._load_json()

        pdf_path = os.path.join(self.path, "pdfs")

        if not os.path.exists(pdf_path):
            logger.error(
                "No downloaded papers find. Please run `paperplumber download [path]` to download them first."
            )

        pdfs = [x for x in os.listdir(pdf_path) if x.endswith(".pdf")]

        return pdfs

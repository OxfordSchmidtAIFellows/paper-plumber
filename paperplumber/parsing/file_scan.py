"""This module implements the embedding search of a pdf file"""
import os
from typing import List
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings

from paperplumber.logger import get_logger
from paperplumber.parsing.llmreader import LLMReader
from paperplumber.parsing.pdf_parser import PDFParser


logger = get_logger(__name__)


class FileScanner(PDFParser):
    """A class used to scan a PDF file for data using
    the LLMReader functionality."""

    def __init__(self, pdf_path: str):
        super().__init__(pdf_path)

    @classmethod
    def from_pages(cls, pages: List):
        """Creates a FileScanner object from a list of pages.

        Args:
            pages (List): A list of pages to be scanned.

        Returns:
            FileScanner: A FileScanner object with the specified pages."""

        scanner = cls.__new__(cls)
        scanner._pages = pages
        return scanner

    def scan(self, target: str) -> List[str]:
        """Scans the pages of a document for a specified target using the LLMReader.

        This function scans each page of the document and retrieves values related to 
        the target, discarding any 'NA' values. If multiple unique values are found for 
        the target, a warning is logged.

        Args:
            target (str): The target to be scanned within the document pages.

        Returns:
            List[str]: A list of unique values found for the target in the document pages, 
                    excluding 'NA'. If no value is found, returns an empty list.

        Raises:
            Warning: If more than one unique value is found for the target."""

        reader = LLMReader(target)
        values = [reader.read(page.page_content) for page in self._pages]

        # Remove NAs
        clean_values = set([value for value in values if value is not 'NA'])

        # Warn if multiple values are found
        if len(clean_values) > 1:
            logger.warning(f"Found multiple values for {target}.")

        return list(clean_values)
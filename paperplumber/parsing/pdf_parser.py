"""Abstract base class to parse PDFs."""

import os

from langchain.document_loaders import PyPDFium2Loader

from paperplumber.logger import get_logger


logger = get_logger(__name__)


class PDFParser:

    _backend = "pdfium2"

    def __init__(self, pdf_path: str):

        self._pdf_path = pdf_path
        
        # Check if the pdf exists
        if not os.path.exists(self._pdf_path):
            logger.error("File % does not exist", str(self._pdf_path))

        # Load and split the pdf into pages
        self._loader = self._get_loader(self._backend)(pdf_path)
        self._pages = self._loader.load_and_split()

    def _get_loader(self, backend: str):
        if backend == "pdfium2":
            return PyPDFium2Loader
        else:
            raise ValueError("Invalid backend")
        
    @property
    def pages(self):
        """
        Returns the split pages of the pdf file.
        """
        return self._pages
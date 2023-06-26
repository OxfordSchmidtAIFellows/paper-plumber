"""This module implements the embedding search of a pdf file"""
import os
from typing import List
from langchain.document_loaders import PyPDFium2Loader
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings

from paperplumber.logger import get_logger

logger = get_logger(__name__)



class DocEmbeddings:
    """
    A class used to represent Document Embeddings for a specific PDF document.

    ...

    Attributes
    ----------
    _pdf_path : str
        The path to the PDF document.
    _loader : PyPDFium2Loader
        The object responsible for loading and splitting the PDF document into pages.
    _pages : List[str]
        The list of pages from the loaded PDF document.
    _faiss_index : FAISS
        FAISS index built from the document pages.

    Methods
    -------
    similarity_search(question: str, k: int = 2):
        Returns top k similar documents for a given question using similarity search in the FAISS index.
    """

    def __init__(self, pdf_path: str):
        """
        Constructs all necessary attributes for the DocEmbeddings object.

        Parameters
        ----------
            pdf_path : str
                The path to the PDF document.
        """

        self._pdf_path = pdf_path

        # Check if the pdf exists
        if not os.path.exists(self._pdf_path):
            logger.error("File % does not exist",str(self._pdf_path))

        # Load and split the pdf into pages
        self._loader = PyPDFium2Loader(pdf_path)
        self._pages = self._loader.load_and_split()

        # Build a FAISS index from the document pages
        self._faiss_index = FAISS.from_documents(self._pages, OpenAIEmbeddings())

    def similarity_search(self, question: str, k: int = 2) -> List[str]:
        """
        Performs a similarity search in the FAISS index for a given question.

        Parameters
        ----------
            question : str
                The question for which to find similar documents.
            k : int, optional
                The number of similar documents to find (default is 2).

        Returns
        -------
        List[str]
            A list of top k similar documents.
        """

        docs = self._faiss_index.similarity_search(question, k=k)
        return docs

    @property
    def pages(self):
        """
        Returns the split pages of the pdf file.
        """
        return self._pages

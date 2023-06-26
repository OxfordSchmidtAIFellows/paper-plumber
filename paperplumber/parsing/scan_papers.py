"""
This module scans the existing downloaded papers and ask question for each of them.
"""
import os
from typing import Dict, List, Optional
from paperplumber.database.findpapers_integration import FindPapersDatabase
from paperplumber.parsing.embedding_search import DocEmbeddings
from paperplumber.parsing.llmreader import OpenAIReader


def scan_the_target(
        target: str, path: str, filter_with_embedding_search: bool = True
) -> Dict[str, List[Optional[str]]]:
    """
    This function scans a target quantity from a set of papers within a specified directory.

    Parameters
    ----------
    target : str
        The target quantity that we are trying to extract from the papers.

    path : str
        The path of the directory containing the papers.

    filter_with_embedding_search : bool, optional
        If True, the function will only scan those pages that are returned by a similarity search
        with the target quantity (default is True).

    Returns
    -------
    Dict[str, List[Optional[str]]]
        A dictionary mapping each paper's path to a list of the extracted values from that paper.

    """

    # Instantiate a database to list all available pdfs in the specified path
    database = FindPapersDatabase(path=path)
    downloaded_papers = database.list_downloaded_papers()

    # Instantiate a reader to read the target quantity from the papers
    reader = OpenAIReader(target=target)

    values_dict = {}

    # Iterate over all papers
    for paper_path in downloaded_papers:
        values = []

        # Create document embeddings for the current paper
        doc = DocEmbeddings(os.path.join(path, "pdfs", paper_path))

        # If filter_with_embedding_search is True, filter pages based on similarity to target
        if filter_with_embedding_search:
            pages = doc.similarity_search(target)
        else:
            # If filter_with_embedding_search is False, consider all pages
            pages = doc.pages

        # Extract target quantity from each page
        for page in pages:
            value = reader.read(page)

            # If the reader found a value, append it to the values list
            if value is not None:
                values.append(value)

        # Map the paper path to the list of found values
        values_dict[paper_path] = values

    return values_dict

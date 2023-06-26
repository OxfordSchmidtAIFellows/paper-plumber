""" The entrance file of the CLI application is paperplumber/main.py.
It wrapps the findpapers package and adds some # additional functionality.
"""

import os
import json
from typing import List
from datetime import datetime
import typer
from rich.console import Console
from rich.table import Table

import paperplumber
from paperplumber.database.findpapers_integration import FindPapersDatabase
from paperplumber.parsing.embedding_search import EmbeddingSearcher
from paperplumber.parsing.file_scan import FileScanner

app = typer.Typer()

logger = paperplumber.get_logger(__name__)


@app.command("search")
def search(
    path: str = typer.Argument(
        ..., help="A valid database path where the search result will be placed"
    ),
    query: str = typer.Option(
        None,
        "-q",
        "--query",
        show_default=True,
        help="A query string that will be used to perform the papers search (If not provided it will be loaded from the environment variable FINDPAPERS_QUERY). E.g. [term A] AND ([term B] OR [term C]) AND NOT [term D]",
    ),
    query_filepath: str = typer.Option(
        None,
        "-f",
        "--query-file",
        show_default=True,
        help="A file path that contains the query string that will be used to perform the papers search",
    ),
    since: datetime = typer.Option(
        None,
        "-s",
        "--since",
        show_default=True,
        help="A lower bound (inclusive) date that will be used to filter the search results. Following the pattern YYYY-MM-DD. E.g. 2020-12-31",
        formats=["%Y-%m-%d"],
    ),
    until: datetime = typer.Option(
        None,
        "-u",
        "--until",
        show_default=True,
        help="A upper bound (inclusive) date that will be used to filter the search results. Following the pattern YYYY-MM-DD. E.g. 2020-12-31",
        formats=["%Y-%m-%d"],
    ),
    limit: int = typer.Option(
        None,
        "-l",
        "--limit",
        show_default=True,
        help="The max number of papers to collect",
    ),
    limit_per_database: int = typer.Option(
        None,
        "-ld",
        "--limit-db",
        show_default=True,
        help="The max number of papers to collect per each database",
    ),
    databases: str = typer.Option(
        None,
        "-d",
        "--databases",
        show_default=True,
        help="A comma-separated list of databases where the search should be performed, if not specified all databases will be used (this parameter is case insensitive)",
    ),
    publication_types: str = typer.Option(
        None,
        "-p",
        "--publication-types",
        show_default=True,
        help="A comma-separated list of publication types to filter when searching, if not specified all the"
        " publication types will be collected (this parameter is case insensitive). The available publication"
        " types are: journal, conference proceedings, book, other",
    ),
    scopus_api_token: str = typer.Option(
        None,
        "-ts",
        "--token-scopus",
        show_default=True,
        help="A API token used to fetch data from Scopus database. If you don't have one go to"
        " https://dev.elsevier.com and get it. (If not provided it will be loaded from the environment"
        " variable FINDPAPERS_SCOPUS_API_TOKEN)",
    ),
    ieee_api_token: str = typer.Option(
        None,
        "-ti",
        "--token-ieee",
        show_default=True,
        help="A API token used to fetch data from IEEE database. If you don't have one go to https://developer.ieee.org and get it. (If not provided it will be loaded from the environment variable FINDPAPERS_IEEE_API_TOKEN)",
    ),
    proxy: str = typer.Option(
        None,
        "-x",
        "--proxy",
        show_default=True,
        help="proxy URL that can be used during requests",
    ),
    verbose: bool = typer.Option(
        False,
        "-v",
        "--verbose",
        show_default=True,
        help="If you wanna a verbose mode logging",
    ),
):
    # pylint disable=line-too-long
    """
    Search for papers metadata using a query.

    When you have a query and needs to get papers using it, this is the command that you'll need to call.
    This command will find papers from some databases based on the provided query.

    All the query terms need to be enclosed by square brackets and can be associated using boolean operators,
    and grouped using parentheses. The available boolean operators are "AND", "OR". "NOT".
    All boolean operators needs to be uppercased. The boolean operator "NOT" must be preceded by an "AND" operator.

    E.g.: [term A] AND ([term B] OR [term C]) AND NOT [term D]

    You can use some wildcards in the query too. Use ? to replace a single character or * to replace any number of characters.

    E.g.: 'son?' -> will match song, sons, ...

    E.g.: 'son*' -> will match song, sons, sonar, songwriting, ...

    Nowadays, we search for papers on ACM, arXiv, IEEE, PubMed, and Scopus database.
    The searching on IEEE and Scopus requires an API token, that must to be provided
    by the user using the -ts (or --scopus_api_token) and -te (or --ieee_api_token) arguments.
    If these tokens are not provided the search on these databases will be skipped.

    You can constraint the search by date using the -s (or --since) and -u (or --until) arguments
    following the pattern YYYY-MM-DD (E.g. 2020-12-31).

    You can restrict the max number of retrieved papers by using -l (or --limit).
    And, restrict the max number of retrieved papers by database using -ld (or --limit_per_database) argument.

    You can control which databases you would like to use in your search by the -d (or --databases) option. This parameter
    accepts a comma-separated list of database names, and is case-insensitive. Nowadays the available databases are
    ACM, arXiv, IEEE, PubMed, Scopus

    E.g.:
    --databases "scopus,arxiv,acm"
    --databases "ieee,ACM,PubMed"

    You can control which publication types you would like to fetch in your search by the -p (or --publication-types) option. This parameter
    accepts a comma-separated list of database names, and is case-insensitive. Nowadays the available publication types are
    journal, conference proceedings, book, other.
    When a particular publication does not fit into any of the other types it is classified as "other", e.g., magazines, newsletters, unpublished manuscripts.

    E.g.:
    --publication-types "journal,conference proceedings,BOOK,other"
    --publication-types "Journal,book"

    You can control the command logging verbosity by the -v (or --verbose) argument.
    """

    logger.info("Calling findpapers to search your papers...")
    try:
        since = since.date() if since is not None else None
        until = until.date() if until is not None else None
        databases = (
            [x.strip() for x in databases.split(",")] if databases is not None else None
        )
        publication_types = (
            [x.strip() for x in publication_types.split(",")]
            if publication_types is not None
            else None
        )

        if query is None and query_filepath is not None:
            with open(query_filepath, "r", encoding="utf-8") as file:
                query = file.read().strip()

        database = paperplumber.FindPapersDatabase(path=path)
        database.search(
            query=query,
            since=since,
            until=until,
            limit=limit,
            limit_per_database=limit_per_database,
            databases=databases,
            publication_types=publication_types,
            scopus_api_token=scopus_api_token,
            ieee_api_token=ieee_api_token,
            proxy=proxy,
            verbose=verbose,
        )
    except Exception as error:
        if verbose:
            logger.debug(error, exc_info=True)
        else:
            typer.echo(error)
        raise typer.Exit(code=1)


@app.command("refine")
def refine(
    path: str = typer.Argument(
        ..., help="A valid file path for the search result file"
    ),
    categories: List[str] = typer.Option(
        [],
        "-c",
        "--categories",
        show_default=True,
        help="A comma-separated list of categories to assign to the papers with their facet following the pattern: <facet>:<term_b>,<term_c>,...",
    ),
    highlights: str = typer.Option(
        None,
        "-h",
        "--highlights",
        show_default=True,
        help="A comma-separated list of terms to be highlighted on the abstract",
    ),
    show_abstract: bool = typer.Option(
        False,
        "-a",
        "--abstract",
        show_default=True,
        help="A flag to indicate if the paper's abstract should be shown or not",
    ),
    show_extra_info: bool = typer.Option(
        False,
        "-e",
        "--extra-info",
        show_default=True,
        help="A flag to indicate if the paper's extra info should be shown or not",
    ),
    only_selected_papers: bool = typer.Option(
        False,
        "-s",
        "--selected",
        show_default=True,
        help="If only the selected papers will be refined",
    ),
    only_removed_papers: bool = typer.Option(
        False,
        "-r",
        "--removed",
        show_default=True,
        help="If only the removed papers will be refined",
    ),
    read_only: bool = typer.Option(
        False,
        "-l",
        "--list",
        show_default=True,
        help="If this flag is present, this function call will only list the papers",
    ),
    verbose: bool = typer.Option(
        False,
        "-v",
        "--verbose",
        show_default=True,
        help="If you wanna a verbose mode logging",
    ),
):
    # pylint disable=line-too-long
    """
    Refine the search results by selecting/classifying the papers.

    When you have a search result and wanna refine it, this is the command that you'll need to call.
    This command will iterate through all the papers showing their collected data,
    then asking if you wanna select a particular paper or not

    You can show or hide the paper abstract by using the -a (or --abstract) flag.

    If a comma-separated list of categories is provided by the -c (or --categories) argument,
    you can assign a category to the paper. You need to define these categories following the pattern: <facet>:<term_b>,<term_c>,...

    E.g.:
    --categories "Contribution:Metric,Tool,Model,Method"
    --categories "Research Type:Validation Research,Evaluation Research,Solution Proposal,Philosophical,Opinion,Experience"

    The -c parameter can be defined several times, so you can define as many facets as you want
    The -c parameter is case-sensitive.

    And to help you on the refinement, this command can also highlight some terms on the paper's abstract
    by a provided comma-separated list of them provided by the -h (or --highlights) argument.

    You can control the command logging verbosity by the -v (or --verbose) argument.
    """

    logger.info("Calling findpapers to refine your paper list...")
    try:
        highlights = (
            [x.strip() for x in highlights.split(",")]
            if highlights is not None
            else None
        )

        categories_by_facet = {} if len(categories) > 0 else None
        for categories_string in categories:
            string_split = categories_string.split(":")
            facet = string_split[0].strip()
            categories_by_facet[facet] = [x.strip() for x in string_split[1].split(",")]

        database = paperplumber.FindPapersDatabase(path=path)
        database.refine(
            categories=categories_by_facet,
            highlights=highlights,
            show_abstract=show_abstract,
            show_extra_info=show_extra_info,
            only_selected_papers=only_selected_papers,
            only_removed_papers=only_removed_papers,
            read_only=read_only,
            verbose=verbose,
        )

    except Exception as error:
        if verbose:
            logger.debug(error, exc_info=True)
        else:
            typer.echo(error)
        raise typer.Exit(code=1)


@app.command("download")
def download(
    path: str = typer.Argument(
        ..., help="A valid path for the search result and full-text papers files"
    ),
    only_selected_papers: bool = typer.Option(
        False,
        "-s",
        "--selected",
        show_default=True,
        help="A flag to indicate if only selected papers (selections can be done on refine command) will be downloaded",
    ),
    categories: List[str] = typer.Option(
        [],
        "-c",
        "--categories",
        show_default=True,
        help="A comma-separated list of categories (categorization can be done on refine command) that will be used to filter which papers will be downloaded, using the following pattern: <facet>:<term_b>,<term_c>,...",
    ),
    proxy: str = typer.Option(
        None,
        "-x",
        "--proxy",
        show_default=True,
        help="proxy URL that can be used during requests",
    ),
    verbose: bool = typer.Option(
        False,
        "-v",
        "--verbose",
        show_default=True,
        help="If you wanna a verbose mode logging",
    ),
):
    # pylint disable=line-too-long
    """
    Download full-text papers using the search results.

    If you've done your search, (probably made the search refinement too) and wanna download the papers,
    this is the command that you need to call. This command will try to download the PDF version of the papers to
    the output directory path.

    You can download only the selected papers by using the -s (or --selected) flag

    You can filter which kind of categorized papers will be downloaded providing
    a comma-separated list of categories is provided by the -c (or --categories) argument,
    You need to define these categories following the pattern: <facet>:<term_b>,<term_c>,...

    E.g.:
    --categories "Contribution:Metric,Tool"

    The -c parameter can be defined several times, so you can define as many filters as you want
    The -c parameter is case-sensitive.

    We use some heuristics to do our job, but sometime they won't work properly, and we cannot be able
    to download the papers, but we logging the downloads or failures in a file download.log
    placed on the output directory, you can check out the log to find what papers cannot be downloaded
    and try to get them manually later.

    Note: Some papers are behind a paywall and won't be able to be downloaded by this command.
    However, if you have a proxy provided for the institution where you study or work that permit you
    to "break" this paywall. You can use this proxy configuration here
    by setting the environment variable FINDPAPERS_PROXY.

    You can control the command logging verbosity by the -v (or --verbose) argument.
    """

    logger.info("Calling findpapers to download your papers...")

    try:
        categories_by_facet = {} if len(categories) > 0 else None
        for categories_string in categories:
            string_split = categories_string.split(":")
            facet = string_split[0].strip()
            categories_by_facet[facet] = [x.strip() for x in string_split[1].split(",")]
        database = paperplumber.FindPapersDatabase(path=path)
        database.download(
            only_selected_papers=only_selected_papers,
            categories_filter=categories_by_facet,
            proxy=proxy,
            verbose=verbose,
        )

    except Exception as error:
        if verbose:
            logger.debug(error, exc_info=True)
        else:
            typer.echo(error)
        raise typer.Exit(code=1)


@app.command("list")
def list_available(
    path: str = typer.Argument(
        ..., help="A valid path for the search result and full-text papers files"
    ),
    verbose: bool = typer.Option(
        False,
        "-v",
        "--verbose",
        show_default=True,
        help="If you wanna a verbose mode logging",
    ),
):
    # pylint disable=line-too-long
    """
    List the available papers in the local directory, after searching.
    You can control the command logging verbosity by the -v (or --verbose) argument.
    """

    try:
        database = paperplumber.FindPapersDatabase(path=path)
        papers = database.list_available_papers()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Publication date", style="dim", width=10)
        table.add_column("Title", style="dim", width=50)
        table.add_column("Authors", style="dim", width=50)

        for paper in papers:
            table.add_row(
                paper["publication_date"], paper["title"], ",".join(paper["authors"])
            )
        console = Console()
        console.print(table)

    except Exception as error:
        if verbose:
            logger.debug(error, exc_info=True)
        else:
            typer.echo(error)
        raise typer.Exit(code=1)

@app.command("parse")
def parse(
    path: str = typer.Argument(
        ..., help="A valid path for the search result and full-text papers files"
    ),
    target: str = typer.Argument(
        ..., help="The value to extract from the papers"
    ),
    verbose: bool = typer.Option(
        False,
        "-v",
        "--verbose",
        show_default=True,
        help="If you wanna a verbose mode logging",
    ),
    filter_with_embedding_search: bool = typer.Option(
        True,
        "-f",
        "--filter-with-embedding-search",
        show_default=True,
        help="If you wanna filter pages based on similarity to target",
    ),
):
    # pylint disable=line-too-long
    """
    Parse the available papers in the local directory, after searching.
    You can control the command logging verbosity by the -v (or --verbose) argument.
    """
    try:
        # Instantiate a database to list all available pdfs in the specified path
        database = FindPapersDatabase(path=path)
        downloaded_papers = database.list_downloaded_papers()

        values_dict = {}

        # Iterate over all papers
        for paper_path in downloaded_papers:
            pdf_path = os.path.join(path, "pdfs", paper_path)

            # If filter_with_embedding_search is True, filter pages based on similarity to target
            if filter_with_embedding_search:
                doc = EmbeddingSearcher(pdf_path)
                pages = doc.similarity_search(target)
                scanner = FileScanner.from_pages(pages)
                values = scanner.scan(target)
                values_dict[paper_path] = values
            else:
                scanner = FileScanner(pdf_path)
                values = scanner.scan(target)
                values_dict[paper_path] = values

        with open('output.json', 'w') as f:
            json.dump(values_dict, f)


    except Exception as error:
        if verbose:
            logger.debug(error, exc_info=True)
        else:
            typer.echo(error)
        raise typer.Exit(code=1)


@app.command("version")
def version():
    """
    Show current findpapers version
    """

    typer.echo(f"paperplumber {paperplumber.__version__}")

def main():
    """Main function to be called by the command line interface"""
    app()

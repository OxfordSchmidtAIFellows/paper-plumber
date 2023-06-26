# PaperPlumber

Paper Plumber is a Python package that employs large language models to scan, understand, and extract key data points
from scientific papers, streamlining research and data analysis. Currently the project is a CLI application. It's built
on top of the findpapers package. You can find more information about findpapers
at https://github.com/meta-tabchen/paper-finder.

## Installation

To use this package, you need to install it first. You can do this by cloning the repository and installing the
dependencies. More detailed instructions will be provided soon.

## Usage

After the package is installed, you can run paperplumber with different commands and options. Here is a quick overview
of the commands available.

### Commands

+ download - Download full-text papers using the search results.
+ list - List the available papers in the local directory, after searching. You can control the command logging
  verbosity by the `-v` (or `--verbose`) argument.
+ parse - Parse the available papers in the local directory, after searching. You can control the command logging
  verbosity by the `-v` (or `--verbose`) argument.
+ refine - Refine the search results by selecting/classifying the papers.
+ search - Search for papers metadata using a query.
+ version - Show the current version.

Each command has its own set of options which can be found in the `--help` information for each command.

For instance, the parse command usage is as follows:

```
paperplumber parse [OPTIONS] PATH TARGET
```

This command is used to parse the available papers in the local directory, after searching.

Arguments for parse

+ `path` - A valid path for the search result and full-text papers files. This argument is required.
+ `target` - The value to extract from the papers. This argument is also required.
  Options for parse
+ `--verbose`, `-v` - Use this option if you want verbose mode logging.
+ `--filter-with-embedding-search`, `-f` - Use this option if you want to filter pages based on similarity to target. By
  default, it is set to True.
  If you need help, you can use the --help option after any command to get more information about that command.

### Full example

The following command search papers that contains `quantum computing` and `two-qubit gate error`, download them and
extract the values of `two-qubit error` in these pdfs.

```
paperplumber search -q  "[quantum computing] AND [two-qubit gate error]" `pwd`
paperplumber download `pwd`
paperplumber parse `pwd` "two-qubit gate error"
```

## License

This project is licensed under the MIT License.

## Support

If you have any questions or run into any trouble, please open an issue on the GitHub repository.

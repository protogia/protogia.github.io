# PYTHON_ARGCOMPLETE_OK

import argcomplete
import pretty_errors
import os
import nbformat
import nbconvert
import datetime
from nbconvert import MarkdownExporter

from argparse import ArgumentParser, Namespace
from rich_argparse import RichHelpFormatter

pretty_errors.configure(
    separator_character = '*',
    line_number_first   = True,
    display_link        = True,
    lines_before        = 5,
    lines_after         = 2,
    line_color          = pretty_errors.RED + '> ' + pretty_errors.default_config.line_color,
    code_color          = '  ' + pretty_errors.default_config.line_color,
    truncate_code       = True,
    display_locals      = True
)


def parse_arguments() -> Namespace:
    parser = ArgumentParser(
        prog="ipynb2md",
        formatter_class=RichHelpFormatter,
        description="A command-line tool for converting jupyter-notebooks into markdown-files and add metainformations."
    )
    
    parser.add_argument(
        "-f", "--file",
        type=str,
        help="Path to the jupyter-notebook file to convert."
    )
    
    parser.add_argument(
        "-d", "--destination",
        type=str,
        help="Destination folder."
    )
    
    argcomplete.autocomplete(parser)
    
    return parser.parse_args()


def main() -> None:
    cli_args: Namespace = parse_arguments()
    
    if cli_args.destination is None or cli_args.file is None:
        raise ValueError("You must specify a destination and and notebook-file to convert.")
    
    if not os.path.isdir(cli_args.destination):
        raise NotADirectoryError(f"The destination '{cli_args.destination}' does not exist or is not a directory.")
    
    if not os.path.isfile(cli_args.file) or not cli_args.file.endswith(".ipynb"):
        raise FileNotFoundError(f"File '{cli_args.file}' does not exist or is not jupyter notebook.")
    
    try:
        # convert notebook to markdown
        with open(cli_args.file, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)

        markdown_exporter = MarkdownExporter()
        (body, resources) = markdown_exporter.from_file(cli_args.file)

        # Determine output path
        filename = os.path.splitext(os.path.basename(cli_args.file))[0]
        output_path = os.path.join(cli_args.destination, f"{filename}.md")
        
        # add metainformation for hugo-webblog
        if cli_args.destination.endswith("blog"):
            with open("archetypes/blog.md", "r", encoding='utf-8') as f:
                metadata = f.read()
                
                # replace placeholders for blogpost-title and date
                title = filename.replace("-", " ").replace(".md", "")
                metadata = metadata.replace("'{{ replace .File.ContentBaseName `-` ` ` | title }}'", title)
                metadata = metadata.replace("'{{ .Date }}'", f"'{datetime.datetime.now(datetime.timezone.utc).isoformat()}'")
            body = metadata + '\n\n' + body

        with open(output_path, 'w', encoding='utf-8') as outfile:
            outfile.write(body)
        print(f"Notebook converted to Markdown: {output_path}")
        
    except Exception as e:
        print(f"An error occurred during conversion: {e}")


if __name__=="__main__":
    main()
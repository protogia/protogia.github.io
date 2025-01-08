# PYTHON_ARGCOMPLETE_OK

import argcomplete
import pretty_errors
import os
import nbformat
import datetime

from rich import print
from nbconvert import MarkdownExporter
from argparse import ArgumentParser, Namespace
from rich_argparse import RichHelpFormatter
from websiteconfig import config as hugoconfig

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
    
    # convert notebook to markdown
    with open(cli_args.file, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)

    markdown_exporter = MarkdownExporter()
    (body, resources) = markdown_exporter.from_file(cli_args.file)

    # Determine output path
    filename = os.path.splitext(os.path.basename(cli_args.file))[0]
    output_path = os.path.join(cli_args.destination, f"{filename}.md")

    if 'outputs' in resources:
        #Create directory for blogpost-images
        image_dir = os.path.join(hugoconfig.WEBSITE_IMG_PATH, filename)
        os.makedirs(image_dir, exist_ok=True)

        for output in resources['outputs']:
            image_path = os.path.join(image_dir, output)

            with open(image_path, 'wb') as image_file:
                image_file.write(resources["outputs"][output])
            
            # Replace the image data in the markdown with a local link
            # ![png](?)
            body = body.replace(f"![png]({output})", f"![alt-text]({image_path})")
            body = body.replace(f"![alt-text](static/", f"![alt-text](/") # remove trailing static/ -folderinformation
                                
    # add metainformation for hugo-webblog
    if "content/blog"  in cli_args.destination:
        with open("archetypes/blog.md", "r", encoding='utf-8') as f:
            metadata = f.read()
            
            # replace placeholders for blogpost-title and date
            title = filename.replace("-", " ").replace(".md", "")
            metadata = metadata.replace("'{{ replace .File.ContentBaseName `-` ` ` | title }}'", title)
            metadata = metadata.replace("'{{ .Date }}'", f"'{datetime.datetime.now(datetime.timezone.utc).isoformat()}'")
        body = metadata + '\n\n' + body

    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write(body)
    print(f"[green]Notebook converted to Markdown:[/green] [italic yellow]{output_path}[/italic yellow]")
        

if __name__=="__main__":
    main()
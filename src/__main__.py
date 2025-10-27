# PYTHON_ARGCOMPLETE_OK

import argcomplete
import pretty_errors
import os
import nbformat
import datetime
import json

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
    

    with open(cli_args.file, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)

    # export plotly-output-cells to json    
    plotly_count = 0
    
    for cell in notebook.cells:
        if cell.cell_type == 'code' and hasattr(cell, 'outputs'):
            
            new_outputs = [] # new list to store *only* non-plotly outputs
            for output in cell.outputs:
                if 'data' in output:
                    plotly_mime_type = 'application/vnd.plotly.v1+json'
                    
                    if plotly_mime_type in output['data']:
                        # chartdata
                        chart_data = output['data'][plotly_mime_type]
                        
                        # path and filename
                        plotly_count += 1
                        
                        filename = f"plotly_chart_{plotly_count}.json"

                        plotly_dest = os.path.join(
                            hugoconfig.WEBSITE_PLOTLY_PATH, 
                            os.path.splitext(os.path.basename(cli_args.file))[0]
                        )
                        
                        if os.path.exists(plotly_dest) == False:
                            os.mkdir(plotly_dest)
                        
                        output_path = os.path.join(
                            plotly_dest,
                            filename
                        )
                        
                        # save the file
                        with open(output_path, 'w', encoding='utf-8') as json_file:
                            json.dump(chart_data, json_file, indent=4)                         
                        print(f"Extracted chart from cell {cell.execution_count} to {output_path}")
                                                
                        # replace plotly-chart-cell in plaintext-notebook with hugo-placeholder
                        hugo_json_path = os.path.join(
                            '/', # Start from Hugo root
                            os.path.basename(hugoconfig.WEBSITE_PLOTLY_PATH), 
                            filename
                        ).replace('\\', '/')
                        
                        placeholder = f'{{{{< plotly json="{hugo_json_path}" >}}}}'
                            
                        placeholder_output = nbformat.v4.new_output(
                            output_type='display_data',
                            data={'text/markdown': placeholder}
                        )
                        
                        new_outputs.append(placeholder_output)                    
                    else:
                        new_outputs.append(output)
                else:
                    new_outputs.append(output)

            # update cells after plotly-chart-replacement
            cell.outputs = new_outputs
            
    if plotly_count == 0:
        print(f"No Plotly charts found in the outputs of '{cli_args.file}'.")
    else:
        print(f"Successfully extracted {plotly_count} total static/plotly/<projectname>/*.json.")

    markdown_exporter = MarkdownExporter()
    (body, resources) = markdown_exporter.from_notebook_node(notebook)

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
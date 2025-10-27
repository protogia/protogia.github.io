# PYTHON_ARGCOMPLETE_OK

import argcomplete
import pretty_errors
import os
import nbformat
import datetime
import json
import re 

from rich import print
from nbconvert import MarkdownExporter, exporters
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

# ---
# NOTE: parse_arguments remains unchanged
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
# ---


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
    plotly_mime_type = 'application/vnd.plotly.v1+json'
    for cell in notebook.cells:
        if cell.cell_type == 'code' and hasattr(cell, 'outputs'):
            
            new_outputs = [] # store *only* non-plotly outputs
            placeholder_cell = None
            
            for output in cell.outputs:
                if 'data' in output:
                    
                    if plotly_mime_type in output['data']:
                        chart_data = output['data'][plotly_mime_type]
                        
                        # path and filename
                        plotly_count += 1
                        filename = f"plotly_chart_{plotly_count}.json"

                        plotly_dest = os.path.join(
                            hugoconfig.WEBSITE_PLOTLY_PATH, 
                            os.path.splitext(os.path.basename(cli_args.file))[0]
                        )
                        
                        os.makedirs(plotly_dest, exist_ok=True)
                        
                        output_path = os.path.join(
                            plotly_dest,
                            filename
                        )
                        
                        # save file
                        with open(output_path, 'w', encoding='utf-8') as json_file:
                            json.dump(chart_data, json_file, indent=4)                         
                        print(f"Extracted chart from cell {cell.execution_count} to {output_path}")
                                                
                        # replace plotly-chart-cell in plaintext-notebook with hugo-placeholder
                        hugo_json_path = os.path.join(
                            '/', # Start from Hugo root
                            os.path.basename(hugoconfig.WEBSITE_PLOTLY_PATH), 
                            os.path.basename(os.path.splitext(cli_args.file)[0]), # folder name
                            filename
                        ).replace('\\', '/')
                        
                        placeholder = f'{{{{< plotly json="{hugo_json_path}" >}}}}'
                            
                        # Store the placeholder in a new markdown cell
                        placeholder_cell = nbformat.v4.new_markdown_cell(placeholder)
                                        
                    else:
                        new_outputs.append(output)
                else:
                    new_outputs.append(output)

            # Update the original cell's outputs, removing the plotly output
            cell.outputs = [out for out in new_outputs if isinstance(out, dict)]
            
            # Insert the placeholder cell after the current code cell
            if placeholder_cell:
                try:
                    cell_index = notebook.cells.index(cell)
                    notebook.cells.insert(cell_index + 1, placeholder_cell)
                except ValueError:
                    print(f"[red]Error:[/red] Could not find cell in notebook structure.")
                    pass

    if plotly_count == 0:
        print(f"No Plotly charts found in the outputs of '{cli_args.file}'.")
    else:
        print(f"Successfully extracted {plotly_count} total static/plotly/<projectname>/*.json.")      

    # convert notebook to markdown, applying shortcode grouping
    markdown_exporter = MarkdownExporter()
    basic_exporter = exporters.get_exporter('markdown')(config=markdown_exporter.config)

    grouped_markdown = []
    current_group_content = ""
    is_in_group = False
    temp_nb = nbformat.v4.new_notebook()

    for cell in notebook.cells:
        temp_nb.cells = [cell]
        (cell_markdown, resources) = basic_exporter.from_notebook_node(temp_nb)
        cell_markdown = cell_markdown.strip() 

        is_code_cell = cell.cell_type == 'code'

        if is_code_cell:
            if not is_in_group:
                # Start a new group
                current_group_content += '{{<details title="">}} \n\n'
                is_in_group = True
            
            # append the cell content (code and its non-plotly outputs)
            current_group_content += cell_markdown + "\n\n"
        
        else:
            # this is a separator cell (Markdown or Plotly shortcode)
            if is_in_group:
                # close the previous group
                current_group_content += "{{</details>}}\n\n"
                grouped_markdown.append(current_group_content)
                current_group_content = ""
                is_in_group = False
            
            # now append the current cell itself (Markdown prose/headings/plotly)
            grouped_markdown.append(cell_markdown + "\n\n")

    # If the notebook ends while inside a group, close it
    if is_in_group:
        current_group_content += "{{/details}}\n\n"
        grouped_markdown.append(current_group_content)

    body = "".join(grouped_markdown).strip()
    
    # Handle Static Resource (Image) Replacement
    # Re-run the full exporter *only* to gather the resources dictionary for image data
    (full_body, resources) = markdown_exporter.from_notebook_node(notebook)

    if 'outputs' in resources:
        filename_base = os.path.splitext(os.path.basename(cli_args.file))[0]
        image_dir = os.path.join(hugoconfig.WEBSITE_IMG_PATH, filename_base)
        os.makedirs(image_dir, exist_ok=True)
        
        for output in resources['outputs']:
            image_path = os.path.join(image_dir, output)

            # Write the image data to file
            with open(image_path, 'wb') as image_file:
                image_file.write(resources["outputs"][output])
            
            # Construct the Hugo relative path
            hugo_image_path = os.path.join(
                '/', 
                os.path.basename(hugoconfig.WEBSITE_IMG_PATH),
                filename_base,
                output
            ).replace('\\', '/')
            
            # Replace the image data reference in the markdown with the local link
            body = re.sub(
                rf'\[png\]\({re.escape(output)}\)', 
                f"![alt-text]({hugo_image_path})", 
                body
            )


    # Final Formatting
    filename_base = os.path.splitext(os.path.basename(cli_args.file))[0]

    # add metainformation for hugo-webblog
    if "content/blog"  in cli_args.destination:
        with open("archetypes/blog.md", "r", encoding='utf-8') as f:
            metadata = f.read()
            
            # replace placeholders for blogpost-title and date
            title = filename_base.replace("-", " ").replace(".md", "")
            metadata = metadata.replace("'{{ replace .File.ContentBaseName `-` ` ` | title }}'", f"'{title}'")
            metadata = metadata.replace("'{{ .Date }}'", f"'{datetime.datetime.now(datetime.timezone.utc).isoformat()}'")
        body = metadata.strip() + '\n\n' + body

# Determine output path
    output_path = os.path.join(cli_args.destination, f"{filename_base}.md")

    # --- Add language tags (```python) only to opening fences ---
    lang = notebook.metadata.get("language_info", {}).get("name", "python")

    lines = body.splitlines()
    inside_code = False
    for i, line in enumerate(lines):
        # detect a fence that has only ``` (optionally with spaces)
        if re.fullmatch(r"\s*```", line):
            if not inside_code:
                # opening fence → add language
                lines[i] = f"```{lang}"
                inside_code = True
            else:
                # closing fence → leave as plain ```
                inside_code = False
    body = "\n".join(lines)
    # ------------------------------------------------------------


    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write(body)

    print(f"[green]Notebook converted to Markdown:[/green] [italic yellow]{output_path}[/italic yellow]")


if __name__=="__main__":
    main()
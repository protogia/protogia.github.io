# PYTHON_ARGCOMPLETE_OK

import argcomplete
import pretty_errors
import os
import nbformat
import datetime
import json
import re 
from bs4 import BeautifulSoup 

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

## HTML Table to Markdown Conversion
def html_table_to_markdown(html_string: str) -> str:
    """Converts a single HTML table (like those from pandas) to a Markdown table."""
    soup = BeautifulSoup(html_string, 'html.parser')
    table = soup.find('table', class_='dataframe')
    
    if not table:
        return "" 
        
    markdown_lines = []
    
    # --- 1. Header Row and Separator ---
    header_row = []
    separator_row = []
    
    # Extract headers from <thead>
    for th in table.find('thead').find_all('th'):
        header_row.append(th.get_text().strip())
        separator_row.append('---')
    
    # Remove the first element if it's the empty index header
    if header_row and header_row[0] == "":
        header_row = header_row[1:]
        separator_row = separator_row[1:]

    # Join the header and separator rows for markdown
    if header_row:
        markdown_lines.append(f"| {' | '.join(header_row)} |")
        markdown_lines.append(f"| {' | '.join(separator_row)} |")
    
    # --- 2. Data Rows ---
    for tr in table.find('tbody').find_all('tr'):
        data_row = []
        
        # Get row index (<th> in <tbody>) and data (<td>)
        index_th = tr.find('th')
        if index_th:
            data_row.append(index_th.get_text().strip())
        
        for td in tr.find_all('td'):
            data_row.append(td.get_text().strip())
        
        # Join the data row for markdown
        markdown_lines.append(f"| {' | '.join(data_row)} |")
        
    # Add a newline after the table to ensure it renders correctly after the shortcode
    return "\n".join(markdown_lines) + "\n"
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
    dataframe_count = 0
    plotly_mime_type = 'application/vnd.plotly.v1+json'
    dataframe_html_mime_type = 'text/html' 
    
    # Find the indices of cells that are code cells
    code_cell_indices = [i for i, cell in enumerate(notebook.cells) if cell.cell_type == 'code']
    
    # Iterate in reverse to allow for safe insertion of new cells
    for cell_index in reversed(code_cell_indices):
        cell = notebook.cells[cell_index]

        if cell.cell_type == 'code' and hasattr(cell, 'outputs'):
            
            placeholder_cell = None
            dataframe_cell = None
            outputs_to_remove = [] 

            for output_idx, output in enumerate(cell.outputs):
                if 'data' in output:
                    
                    # 1. Plotly Handling
                    if plotly_mime_type in output['data']:
                        chart_data = output['data'][plotly_mime_type]
                        
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
                        
                        with open(output_path, 'w', encoding='utf-8') as json_file:
                            json.dump(chart_data, json_file, indent=4)                         
                        print(f"Extracted chart from cell {cell.execution_count} to {output_path}")
                                                
                        hugo_json_path = os.path.join(
                            '/', 
                            os.path.basename(hugoconfig.WEBSITE_PLOTLY_PATH), 
                            os.path.basename(os.path.splitext(cli_args.file)[0]), 
                            filename
                        ).replace('\\', '/')
                        
                        placeholder = f'{{{{< plotly json="{hugo_json_path}" >}}}}'
                            
                        # Plotly placeholder cell: DO NOT ADD A SPECIAL TAG
                        placeholder_cell = nbformat.v4.new_markdown_cell(placeholder)
                        
                        outputs_to_remove.append(output_idx) 

                    # 2. Dataframe HTML Handling 
                    elif dataframe_html_mime_type in output['data']:
                        html_content = output['data'][dataframe_html_mime_type]
                        
                        if isinstance(html_content, list):
                            html_content = "".join(html_content)

                        markdown_table = html_table_to_markdown(html_content)
                        
                        if markdown_table:
                            dataframe_cell = nbformat.v4.new_markdown_cell(markdown_table)
                            # Dataframe cell: USE A SPECIFIC TAG to keep it in the group
                            dataframe_cell.metadata['is_dataframe_output'] = True 
                            dataframe_count += 1
                            print(f"Extracted dataframe table from cell {cell.execution_count} and converted to Markdown.")
                            
                            outputs_to_remove.append(output_idx) 
                        
            # --- Apply Changes ---
            
            # 1. Update the original cell's outputs, REMOVING Plotly/Dataframe HTML
            cell.outputs = [out for idx, out in enumerate(cell.outputs) if idx not in outputs_to_remove]
            
            # 2. Insert new cells (Markdown Table first, then Plotly shortcode)
            if dataframe_cell:
                # Insert Dataframe Markdown cell
                notebook.cells.insert(cell_index + 1, dataframe_cell)
            
            if placeholder_cell:
                # Insert Plotly placeholder cell 
                notebook.cells.insert(cell_index + 1, placeholder_cell)

    if plotly_count == 0:
        print(f"No Plotly charts found in the outputs of '{cli_args.file}'.")
    else:
        print(f"Successfully extracted {plotly_count} total static/plotly/<projectname>/*.json.")      

    if dataframe_count == 0:
        print(f"No dataframe tables found in the outputs of '{cli_args.file}'.")
    else:
        print(f"Successfully converted {dataframe_count} dataframe tables to Markdown.")


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
        # CHECK FOR THE DATAFRAME-SPECIFIC METADATA TAG
        is_dataframe_output = cell.metadata.get('is_dataframe_output', False) 

        if is_code_cell:
            if not is_in_group:
                # Start a new group
                current_group_content += '{{<details title="Show code">}}\n\n' 
                is_in_group = True
            
            # append the cell content (code and its non-plotly outputs)
            current_group_content += cell_markdown + "\n\n"
        
        # --- MODIFIED GROUPING LOGIC ---
        
        # If it is a Dataframe output, and we are currently in a group, include it.
        elif is_dataframe_output and is_in_group:
             current_group_content += cell_markdown + "\n\n"
             
        # If it is NOT a code cell AND NOT a dataframe output 
        # (This catches prose/heading AND the UNTAGGED Plotly shortcode cell)
        else:
            # This cell acts as a separator/group closer
            if is_in_group:
                # Close the previous group
                current_group_content += "{{</details>}}\n\n"
                grouped_markdown.append(current_group_content)
                current_group_content = ""
                is_in_group = False
            
            # Now append the current cell itself (Prose/Heading/Plotly)
            grouped_markdown.append(cell_markdown + "\n\n")
        # -------------------------------

    # If the notebook ends while inside a group, close it
    if is_in_group:
        current_group_content += "{{</details>}}\n\n"
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
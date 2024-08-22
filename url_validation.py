import re
import requests
import pandas as pd
import pretty_errors

from rich import print as richprint
from rich.table import Table
from pathlib import Path
from argparse import ArgumentParser
from rich_argparse import RichHelpFormatter
from tabulate import tabulate

def parse_arguments():
    parser = ArgumentParser(
        description='Check external links in files.',
        formatter_class=RichHelpFormatter
    )

    parser.add_argument(
        "--directory", "-d",
        type=str,
        default=".",
        help="The directory to start scanning from."
    )
    
    parser.add_argument(
        "--only-failure", "-f",
        action="store_true",
        help="Only display URLs that resulted in a failure status code."
    )
    
    parser.add_argument(
        "--show-redirects", "-r",
        action="store_false",
        help="Display information if url validated successfull and is redirect."
    )    
    
    cli_args = parser.parse_args()
    return cli_args

def main():
    cli_args = parse_arguments()
    
    # Pfad zum Projektverzeichnis
    project_dir = Path(cli_args.directory)
    
    data = []
    for md_file in project_dir.rglob("*.md"):
        data += [result for result in check_files_for_urls(md_file)]

    # create pandas.df with source, destination-url, statuscode, redirect-info
    columns=["source", "url", "statuscode", "is_redirect"]
    df = pd.DataFrame(columns=columns, data=data)
    visualize_results(df, only_failure=cli_args.only_failure, show_redirects=cli_args.show_redirects)
    
    if (df['statuscode'] >= 300).any() or df['statuscode'].isnull().any():
        exit(1)
    else:
        exit(0)

def visualize_results(df, only_failure=False, show_redirects=False):

    if show_redirects:
        df = df.drop(columns=["is_redirect"])
    if only_failure:
        df = df[(df['statuscode'] < 200) | (df['statuscode'] >= 300) | df['statuscode'].isna()]

    table = Table(title="Overview of outgoing-urls:")
    for col in df.columns:
        table.add_column(col)

    numerical_column = 'statuscode'
    for i, row in df.iterrows():
        colored_row = []
        for col in df.columns:
            val = row[col]
                
            if col == numerical_column:
                if val < 200:
                    colored_row.append(f"[blue]{val}[blue]")
                elif val >= 200 and val < 300:
                    colored_row.append(f"[green]{val}[green]")
                elif val >= 300 and val < 400:
                    colored_row.append(f"[white]{val}[white]")
                elif val >= 400 and val < 500:
                    colored_row.append(f"[bold red]{val}[/bold red]")
                elif val >= 500:
                    colored_row.append(f"[bold orange]{val}[/bold orange]")
                else:
                    colored_row.append("[red]None[red]")
            else:
                colored_row.append(str(val))

        table.add_row(*colored_row)
    richprint(table)


def check_files_for_urls(file):
    # regexp for all possible urls ...
    link_pattern = re.compile(r'\b[a-zA-Z][a-zA-Z0-9+.-]*:\/\/[^\s/$.?#].[^\s]*\b') 

    with open(file, "r", encoding="utf-8") as file:
        content = file.read()
        links = link_pattern.findall(content)
        for link in links:
            response = check_link(link)

            if response:
                data = [file.name, link, response.status_code, response.is_redirect]
            else:
                data = [file.name, link, None, None]
            yield data
          
                
def check_link(url):
    try: 
        response = requests.head(url, allow_redirects=True, timeout=8)
        return response
    except requests.RequestException as e:
        # print(e)
        return None


if __name__=="__main__":
    main()
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

console = Console()

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'Void - Input', 'DATA-BASE')
BASE_DIR = os.path.normpath(BASE_DIR)


def search(term, folder):
    results = []
    files_searched = 0
    encodings = ['utf-8', 'latin-1', 'cp1252']

    if not os.path.isdir(folder):
        return results, 0, f"Folder not found: {folder}"

    all_files = []
    for root, _, files in os.walk(folder):
        for f in files:
            all_files.append(os.path.join(root, f))

    for filepath in all_files:
        files_searched += 1
        filename = os.path.basename(filepath)
        content = None

        for enc in encodings:
            try:
                with open(filepath, 'r', encoding=enc) as fh:
                    content = fh.readlines()
                break
            except UnicodeDecodeError:
                continue
            except OSError:
                break

        if content is None:
            continue

        for line_num, line in enumerate(content, start=1):
            if term.lower() in line.lower():
                results.append({
                    "folder":   os.path.dirname(filepath),
                    "file":     filename,
                    "line":     line_num,
                    "content":  line.strip(),
                })

    return results, files_searched, None


def display_results(term, results, files_searched):
    console.print()

    if not results:
        console.print(Panel(
            f"[bold red]No results[/bold red] for [white]« {term} »[/white]\n"
            f"[dim]{files_searched} file(s) scanned[/dim]",
            border_style="red",
            box=box.DOUBLE_EDGE,
        ))
        return

    table = Table(
        title=f"[bold red]Results for[/bold red] [bold white]« {term} »[/bold white]",
        box=box.DOUBLE_EDGE,
        border_style="red",
        header_style="bold red",
        show_lines=True,
    )
    table.add_column("#", justify="right", width=4, style="dim")
    table.add_column("File", style="bold white", width=25)
    table.add_column("Line", justify="right", width=6, style="cyan")
    table.add_column("Content", style="white")

    for i, r in enumerate(results, start=1):
        highlighted = r["content"].replace(term, f"[bold yellow]{term}[/bold yellow]")
        table.add_row(str(i), r["file"], str(r["line"]), highlighted)

    console.print(table)
    console.print()
    console.print(Panel(
        f"[bold green]  {len(results)} result(s) found[/bold green]   "
        f"[dim]{files_searched} file(s) scanned[/dim]",
        border_style="dim white",
    ))
    console.print()


if __name__ == "__main__":
    try:
        console.print()
        console.print(Panel(
            "[bold red]VOID[/bold red] — [bold white]Search DataBase[/bold white]",
            border_style="red",
            box=box.DOUBLE_EDGE,
        ))
        console.print()

        term = console.input(
            "[bold red][[/bold red][bold white]=[/bold white][bold red]][/bold red] Search: "
        ).strip()

        if not term:
            console.print("[bold red][!] Empty search term. Cancelled.[/bold red]")
            raise SystemExit(0)

        with Progress(
            SpinnerColumn(spinner_name="dots", style="bold red"),
            TextColumn("[bold white]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            progress.add_task(f"Searching « {term} »...", total=None)
            results, files_searched, error = search(term, BASE_DIR)

        if error:
            console.print(f"[bold red][!] {error}[/bold red]")
        else:
            display_results(term, results, files_searched)

    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold red][!] Interrupted.[/bold red]")

import random
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich import box

console = Console()

OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'Void - Output', 'Generated'
)
OUTPUT_DIR = os.path.normpath(OUTPUT_DIR)

CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

GENERATORS = {
    "1": {"name": "Amazon",      "format": "XXXX-XXXXXX-XXXXX",           "blocks": [4, 6, 5],          "file": "amazon.txt"},
    "2": {"name": "Netflix",     "format": "XXXX-XXXXXX-XXXX",            "blocks": [4, 6, 4],           "file": "netflix.txt"},
    "3": {"name": "Roblox",      "format": "XXXX-XXXX-XXXX-XXXX",         "blocks": [4, 4, 4, 4],        "file": "roblox.txt"},
    "4": {"name": "Apple",       "format": "XXXXXXXXXXXXXXXX",            "blocks": [16],                "file": "apple.txt"},
    "5": {"name": "Steam",       "format": "XXXXX-XXXXX-XXXXX",           "blocks": [5, 5, 5],           "file": "steam.txt"},
    "6": {"name": "Google Play", "format": "XXXXXXXXXXXXXXXX",            "blocks": [16],                "file": "googleplay.txt"},
    "7": {"name": "Spotify",     "format": "XXXX-XXXX-XXXX-XXXX-XXXX-XX", "blocks": [4, 4, 4, 4, 4, 2], "file": "spotify.txt"},
}


def generate_code(blocks):
    return "-".join(
        ''.join(random.choice(CHARACTERS) for _ in range(n))
        for n in blocks
    )


def ask_count(prompt):
    while True:
        try:
            n = int(console.input(prompt).strip())
            if n > 0:
                return n
            console.print("[bold red][!] Enter a number greater than 0.[/bold red]")
        except ValueError:
            console.print("[bold red][!] Invalid input. Enter an integer.[/bold red]")


def run_generator(key):
    cfg = GENERATORS[key]
    name = cfg["name"]
    fmt  = cfg["format"]

    console.print()
    console.print(Panel(
        f"[bold red]{name} Generator[/bold red]\n"
        f"[dim]Format: [bold white]{fmt}[/bold white][/dim]",
        border_style="red", box=box.DOUBLE_EDGE,
    ))
    console.print()

    n = ask_count(
        "[bold red][[/bold red][bold white]?[/bold white][bold red]][/bold red] "
        "How many codes to generate: "
    )

    codes = []
    with Progress(
        SpinnerColumn(spinner_name="dots", style="bold red"),
        TextColumn("[bold white]{task.description}"),
        BarColumn(bar_width=30, style="red", complete_style="green"),
        TextColumn("[green]{task.completed}[white]/[white]{task.total}"),
        console=console, transient=True,
    ) as progress:
        task = progress.add_task("Generating...", total=n)
        for _ in range(n):
            codes.append(generate_code(cfg["blocks"]))
            progress.advance(task)

    table = Table(
        title=f"[bold red]{n} {name} Codes[/bold red]",
        box=box.DOUBLE_EDGE, border_style="red", header_style="bold red", show_lines=True,
    )
    table.add_column("#", justify="right", width=6, style="dim")
    table.add_column("Code", style="bold cyan")

    for i, code in enumerate(codes, start=1):
        table.add_row(str(i), code)

    console.print()
    console.print(table)
    console.print()

    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        path = os.path.join(OUTPUT_DIR, cfg["file"])
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(codes) + "\n")
        console.print(f"[bold green][✓] Saved to:[/bold green] [cyan]{path}[/cyan]")
    except OSError as e:
        console.print(f"[bold red][!] Could not save: {e}[/bold red]")


def show_menu():
    console.print()
    console.print(Panel(
        "[bold red]VOID[/bold red] — [bold white]Generator[/bold white]",
        border_style="red", box=box.DOUBLE_EDGE,
    ))
    console.print()

    table = Table(box=box.SIMPLE, show_header=False, border_style="red")
    table.add_column("Option", style="bold red", width=6)
    table.add_column("Generator", style="bold white")
    table.add_column("Format", style="dim cyan")

    for key, cfg in GENERATORS.items():
        table.add_row(f"[{key}]", cfg["name"], cfg["format"])
    table.add_row("[0]", "Exit", "")

    console.print(table)


def main():
    try:
        while True:
            show_menu()
            choice = console.input(
                "[bold red][[/bold red][bold white]=[/bold white][bold red]][/bold red] Option: "
            ).strip()

            if choice == "0":
                console.print("[bold red][!] Goodbye.[/bold red]")
                break
            elif choice in GENERATORS:
                run_generator(choice)
                console.print()
                console.input("[dim]Press Enter to continue...[/dim]")
            else:
                console.print(f"[bold red][!] Unknown option '{choice}'.[/bold red]")

    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold red][!] Interrupted.[/bold red]")


if __name__ == "__main__":
    main()

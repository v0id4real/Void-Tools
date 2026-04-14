import random
import os
from datetime import datetime
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
    "1": {
        "nom":    "Amazon",
        "format": "XXXX-XXXXXX-XXXXX",
        "blocs":  [4, 6, 5],
        "fichier": "amazon.txt",
    },
    "2": {
        "nom":    "Netflix",
        "format": "XXXX-XXXXXX-XXXX",
        "blocs":  [4, 6, 4],
        "fichier": "netflix.txt",
    },
    "3": {
        "nom":    "Roblox",
        "format": "XXXX-XXXX-XXXX-XXXX",
        "blocs":  [4, 4, 4, 4],
        "fichier": "roblox.txt",
    },
    "4": {
        "nom":    "Apple",
        "format": "XXXXXXXXXXXXXXXX",
        "blocs":  [16],
        "fichier": "apple.txt",
    },
    "5": {
        "nom":    "Steam",
        "format": "XXXXX-XXXXX-XXXXX",
        "blocs":  [5, 5, 5],
        "fichier": "steam.txt",
    },
    "6": {
        "nom":    "Google Play",
        "format": "XXXXXXXXXXXXXXXX",
        "blocs":  [16],
        "fichier": "googleplay.txt",
    },
    "7": {
        "nom":    "Spotify",
        "format": "XXXX-XXXX-XXXX-XXXX-XXXX-XX",
        "blocs":  [4, 4, 4, 4, 4, 2],
        "fichier": "spotify.txt",
    },
}


def generer_code(blocs):
    return "-".join(
        ''.join(random.choice(CHARACTERS) for _ in range(n))
        for n in blocs
    )


def demander_nombre(prompt):
    while True:
        try:
            n = int(console.input(prompt).strip())
            if n > 0:
                return n
            console.print("[bold red][!] Entrez un nombre supérieur à 0.[/bold red]")
        except ValueError:
            console.print("[bold red][!] Entrée invalide. Entrez un entier.[/bold red]")


def lancer_generateur(cle):
    cfg = GENERATORS[cle]
    nom = cfg["nom"]
    fmt = cfg["format"]
    blocs = cfg["blocs"]
    fichier = cfg["fichier"]

    console.print()
    console.print(Panel(
        f"[bold red]{nom} Generator[/bold red]\n"
        f"[dim]Format : [bold white]{fmt}[/bold white][/dim]",
        border_style="red", box=box.DOUBLE_EDGE,
    ))
    console.print()

    n = demander_nombre(
        "[bold red][[/bold red][bold white]?[/bold white][bold red]][/bold red] "
        "Combien de codes à générer : "
    )

    codes = []
    with Progress(
        SpinnerColumn(spinner_name="dots", style="bold red"),
        TextColumn("[bold white]{task.description}"),
        BarColumn(bar_width=30, style="red", complete_style="green"),
        TextColumn("[green]{task.completed}[white]/[white]{task.total}"),
        console=console, transient=True,
    ) as progress:
        tache = progress.add_task("Génération...", total=n)
        for _ in range(n):
            codes.append(generer_code(blocs))
            progress.advance(tache)

    table = Table(
        title=f"[bold red]{n} Codes {nom}[/bold red]",
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
        chemin = os.path.join(OUTPUT_DIR, fichier)
        with open(chemin, "w", encoding="utf-8") as f:
            f.write("\n".join(codes) + "\n")
        console.print(f"[bold green][✓] Sauvegardé dans :[/bold green] [cyan]{chemin}[/cyan]")
    except OSError as e:
        console.print(f"[bold red][!] Impossible de sauvegarder : {e}[/bold red]")


def afficher_menu():
    console.print()
    console.print(Panel(
        "[bold red]VOID[/bold red] — [bold white]Generator[/bold white]",
        border_style="red", box=box.DOUBLE_EDGE,
    ))
    console.print()

    table = Table(box=box.SIMPLE, show_header=False, border_style="red")
    table.add_column("Option", style="bold red", width=6)
    table.add_column("Générateur", style="bold white")
    table.add_column("Format", style="dim cyan")

    for cle, cfg in GENERATORS.items():
        table.add_row(f"[{cle}]", cfg["nom"], cfg["format"])
    table.add_row("[0]", "Quitter", "")

    console.print(table)


def main():
    try:
        while True:
            afficher_menu()
            choix = console.input(
                "[bold red][[/bold red][bold white]=[/bold white][bold red]][/bold red] Option : "
            ).strip()

            if choix == "0":
                console.print("[bold red][!] Au revoir.[/bold red]")
                break
            elif choix in GENERATORS:
                lancer_generateur(choix)
                console.print()
                console.input("[dim]Appuyez sur Entrée pour continuer...[/dim]")
            else:
                console.print(f"[bold red][!] Option '{choix}' non reconnue.[/bold red]")

    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold red][!] Interrompu.[/bold red]")


if __name__ == "__main__":
    main()

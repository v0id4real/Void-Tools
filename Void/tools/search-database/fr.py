import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich import box
from rich.text import Text

console = Console()

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'Void - Input', 'DATA-BASE')
BASE_DIR = os.path.normpath(BASE_DIR)


def rechercher(terme, dossier):
    resultats = []
    fichiers_recherches = 0
    encodages = ['utf-8', 'latin-1', 'cp1252']

    if not os.path.isdir(dossier):
        return resultats, 0, f"Dossier introuvable : {dossier}"

    all_files = []
    for racine, _, fichiers in os.walk(dossier):
        for f in fichiers:
            all_files.append(os.path.join(racine, f))

    for chemin in all_files:
        fichiers_recherches += 1
        nom_fichier = os.path.basename(chemin)
        contenu = None

        for enc in encodages:
            try:
                with open(chemin, 'r', encoding=enc) as fh:
                    contenu = fh.readlines()
                break
            except UnicodeDecodeError:
                continue
            except OSError:
                break

        if contenu is None:
            continue

        for num_ligne, ligne in enumerate(contenu, start=1):
            if terme.lower() in ligne.lower():
                resultats.append({
                    "dossier": os.path.dirname(chemin),
                    "fichier": nom_fichier,
                    "ligne":   num_ligne,
                    "contenu": ligne.strip(),
                })

    return resultats, fichiers_recherches, None


def afficher_resultats(terme, resultats, fichiers_recherches):
    console.print()

    if not resultats:
        console.print(Panel(
            f"[bold red]Aucun résultat[/bold red] pour [white]« {terme} »[/white]\n"
            f"[dim]{fichiers_recherches} fichier(s) analysé(s)[/dim]",
            border_style="red",
            box=box.DOUBLE_EDGE,
        ))
        return

    table = Table(
        title=f"[bold red]Résultats pour[/bold red] [bold white]« {terme} »[/bold white]",
        box=box.DOUBLE_EDGE,
        border_style="red",
        header_style="bold red",
        show_lines=True,
    )
    table.add_column("#", justify="right", width=4, style="dim")
    table.add_column("Fichier", style="bold white", width=25)
    table.add_column("Ligne", justify="right", width=6, style="cyan")
    table.add_column("Contenu", style="white")

    for i, r in enumerate(resultats, start=1):
        contenu_affiche = r["contenu"]
        contenu_affiche = contenu_affiche.replace(
            terme, f"[bold yellow]{terme}[/bold yellow]"
        )
        table.add_row(
            str(i),
            r["fichier"],
            str(r["ligne"]),
            contenu_affiche,
        )

    console.print(table)
    console.print()
    console.print(Panel(
        f"[bold green]  {len(resultats)} résultat(s) trouvé(s)[/bold green]   "
        f"[dim]{fichiers_recherches} fichier(s) analysé(s)[/dim]",
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

        terme = console.input(
            "[bold red][[/bold red][bold white]=[/bold white][bold red]][/bold red] Recherche : "
        ).strip()

        if not terme:
            console.print("[bold red][!] Terme vide. Annulé.[/bold red]")
            raise SystemExit(0)

        with Progress(
            SpinnerColumn(spinner_name="dots", style="bold red"),
            TextColumn("[bold white]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            progress.add_task(f"Recherche de « {terme} »...", total=None)
            resultats, fichiers_recherches, erreur = rechercher(terme, BASE_DIR)

        if erreur:
            console.print(f"[bold red][!] {erreur}[/bold red]")
        else:
            afficher_resultats(terme, resultats, fichiers_recherches)

    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold red][!] Interrompu.[/bold red]")

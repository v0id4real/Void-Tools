import requests
import webbrowser
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich import box
from rich.text import Text

console = Console()

SITES = {
    "Twitter":    "https://twitter.com/{}",
    "Facebook":   "https://www.facebook.com/{}",
    "Instagram":  "https://www.instagram.com/{}",
    "GitHub":     "https://github.com/{}",
    "Reddit":     "https://www.reddit.com/user/{}",
    "LinkedIn":   "https://www.linkedin.com/in/{}",
    "Pinterest":  "https://www.pinterest.com/{}",
    "Tumblr":     "https://{}.tumblr.com",
    "YouTube":    "https://www.youtube.com/{}",
    "Vimeo":      "https://vimeo.com/{}",
    "TikTok":     "https://www.tiktok.com/@{}",
    "Twitch":     "https://www.twitch.tv/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Medium":     "https://medium.com/@{}",
    "DeviantArt": "https://www.deviantart.com/{}",
    "Behance":    "https://www.behance.net/{}",
    "Flickr":     "https://www.flickr.com/people/{}",
    "Dribbble":   "https://dribbble.com/{}",
    "Patreon":    "https://www.patreon.com/{}",
    "Goodreads":  "https://www.goodreads.com/{}",
    "GitLab":     "https://gitlab.com/{}",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

NOT_FOUND_INDICATORS = [
    "page not found", "user not found", "profile not found",
    "this account doesn't exist", "sorry, this page isn't available",
    "404", "doesn't exist", "n'existe pas",
]


def verifier_nom_utilisateur(site, url_template, nom_utilisateur):
    url = url_template.format(nom_utilisateur)
    try:
        response = requests.get(url, headers=HEADERS, timeout=8, allow_redirects=True)
        if response.status_code == 404:
            return (site, False, None)
        if response.status_code == 200:
            content_lower = response.text.lower()
            for indicator in NOT_FOUND_INDICATORS:
                if indicator in content_lower:
                    return (site, False, None)
            return (site, True, url)
        return (site, False, None)
    except requests.RequestException:
        return (site, False, None)


def principal(nom_utilisateur):
    console.print()
    console.print(Panel(
        f"[bold red]Recherche de :[/bold red] [bold white]{nom_utilisateur}[/bold white]\n"
        f"[dim]Vérification sur {len(SITES)} plateformes...[/dim]",
        title="[bold red]  VOID — NAME TRACKER  [/bold red]",
        border_style="red",
        box=box.DOUBLE_EDGE,
    ))
    console.print()

    trouves = []
    non_trouves = []

    with Progress(
        SpinnerColumn(spinner_name="dots", style="bold red"),
        TextColumn("[bold white]{task.description}"),
        BarColumn(bar_width=30, style="red", complete_style="green"),
        TextColumn("[green]{task.completed}[white]/[white]{task.total}"),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:
        tache = progress.add_task("Analyse en cours...", total=len(SITES))

        with ThreadPoolExecutor(max_workers=15) as executor:
            futures = {
                executor.submit(verifier_nom_utilisateur, site, url, nom_utilisateur): site
                for site, url in SITES.items()
            }
            for future in as_completed(futures):
                site, existe, url = future.result()
                if existe:
                    trouves.append((site, url))
                else:
                    non_trouves.append(site)
                progress.advance(tache)

    table = Table(
        title=f"[bold white]Résultats pour[/bold white] [bold red]{nom_utilisateur}[/bold red]",
        box=box.DOUBLE_EDGE,
        border_style="red",
        header_style="bold red",
        show_lines=True,
    )
    table.add_column("Statut", justify="center", width=8)
    table.add_column("Plateforme", justify="left", width=14)
    table.add_column("URL", justify="left")

    for site, url in sorted(trouves, key=lambda x: x[0]):
        table.add_row("[bold green]  TROUVÉ[/bold green]", f"[bold white]{site}[/bold white]", f"[cyan]{url}[/cyan]")

    for site in sorted(non_trouves):
        table.add_row("[red]  ABSENT[/red]", f"[dim]{site}[/dim]", "[dim]—[/dim]")

    console.print(table)
    console.print()

    console.print(Panel(
        f"[bold green]  Trouvé : {len(trouves)}[/bold green]   [bold red]  Absent : {len(non_trouves)}[/bold red]",
        title="[bold white]Résumé[/bold white]",
        border_style="dim white",
    ))
    console.print()

    if trouves:
        try:
            reponse = console.input("[bold red][[/bold red][bold white]?[/bold white][bold red]][/bold red] Ouvrir les liens trouvés dans le navigateur ? [bold white](oui/non)[/bold white] : ").strip().lower()
            if reponse in ("oui", "o", "yes", "y"):
                for _, url in trouves:
                    webbrowser.open(url)
                console.print("[bold green][✓] Liens ouverts.[/bold green]")
        except (KeyboardInterrupt, EOFError):
            pass


if __name__ == "__main__":
    try:
        console.print()
        nom = console.input("[bold red][[/bold red][bold white]=[/bold white][bold red]][/bold red] Entrez le nom d'utilisateur à rechercher : ").strip()
        if not nom:
            console.print("[bold red][!] Nom d'utilisateur vide. Annulé.[/bold red]")
        else:
            principal(nom)
    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold red][!] Interrompu.[/bold red]")

import re
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

console = Console()

TIMEOUT = 8
IP_REGEX = re.compile(
    r'^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$'
)


def localiser_ip(ip):
    resp = requests.get(f"https://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,zip,lat,lon,isp,org,as,query", timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def afficher(ip, data):
    if data.get("status") == "fail":
        console.print(f"[bold red][!] Erreur API : {data.get('message', 'Inconnu')}[/bold red]")
        return

    table = Table(
        title=f"[bold red]IP Localisation[/bold red] — [bold white]{ip}[/bold white]",
        box=box.DOUBLE_EDGE,
        border_style="red",
        header_style="bold red",
        show_lines=True,
    )
    table.add_column("Champ", style="bold white", width=20)
    table.add_column("Valeur", style="cyan")

    table.add_row("IP",          data.get("query",      "N/A"))
    table.add_row("Pays",        data.get("country",    "N/A"))
    table.add_row("Région",      data.get("regionName", "N/A"))
    table.add_row("Ville",       data.get("city",       "N/A"))
    table.add_row("Code postal", data.get("zip",        "N/A"))
    table.add_row("Latitude",    str(data.get("lat",    "N/A")))
    table.add_row("Longitude",   str(data.get("lon",    "N/A")))
    table.add_row("FAI",         data.get("isp",        "N/A"))
    table.add_row("Organisation",data.get("org",        "N/A"))
    table.add_row("AS",          data.get("as",         "N/A"))

    console.print()
    console.print(table)
    console.print()


if __name__ == "__main__":
    try:
        console.print()
        console.print(Panel(
            "[bold red]VOID[/bold red] — [bold white]IP Localisation[/bold white]",
            border_style="red", box=box.DOUBLE_EDGE,
        ))
        console.print()

        ip = console.input(
            "[bold red][[/bold red][bold white]=[/bold white][bold red]][/bold red] Adresse IP : "
        ).strip()

        if not ip:
            console.print("[bold red][!] Adresse vide. Annulé.[/bold red]")
            raise SystemExit(0)

        if not IP_REGEX.match(ip):
            console.print(f"[bold red][!] Format IP invalide :[/bold red] {ip}")
            raise SystemExit(0)

        with Progress(
            SpinnerColumn(spinner_name="dots", style="bold red"),
            TextColumn("[bold white]{task.description}"),
            console=console, transient=True,
        ) as p:
            p.add_task("Localisation en cours...", total=None)
            data = localiser_ip(ip)

        afficher(ip, data)

    except requests.RequestException as e:
        console.print(f"[bold red][!] Erreur réseau : {e}[/bold red]")
    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold red][!] Interrompu.[/bold red]")

import random
import ipaddress
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich import box

console = Console()

TIMEOUT = 5

RESERVED_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("100.64.0.0/10"),
    ipaddress.ip_network("0.0.0.0/8"),
    ipaddress.ip_network("240.0.0.0/4"),
]


def est_publique(ip_str):
    try:
        ip = ipaddress.ip_address(ip_str)
        return not any(ip in net for net in RESERVED_NETWORKS)
    except ValueError:
        return False


def generer_ip_publique():
    while True:
        ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        if est_publique(ip):
            return ip


def envoyer_webhook(url, ips):
    contenu = "\n".join(f"`{ip}`" for ip in ips)
    payload = {"content": f"**IPs générées :**\n{contenu}"}
    try:
        resp = requests.post(url, json=payload, timeout=TIMEOUT)
        return resp.status_code == 204
    except requests.RequestException:
        return False


def demander_nombre():
    while True:
        try:
            n = int(console.input(
                "[bold red][[/bold red][bold white]=[/bold white][bold red]][/bold red] "
                "Nombre d'IPs à générer : "
            ).strip())
            if n > 0:
                return n
            console.print("[bold red][!] Entrez un nombre supérieur à 0.[/bold red]")
        except ValueError:
            console.print("[bold red][!] Entrée invalide. Entrez un entier.[/bold red]")


if __name__ == "__main__":
    try:
        console.print()
        console.print(Panel(
            "[bold red]VOID[/bold red] — [bold white]IP Generator[/bold white]",
            border_style="red", box=box.DOUBLE_EDGE,
        ))
        console.print()

        nombre = demander_nombre()

        webhook_url = console.input(
            "[bold red][[/bold red][bold white]=[/bold white][bold red]][/bold red] "
            "URL Webhook Discord (laisser vide pour ignorer) : "
        ).strip()

        ips = []
        with Progress(
            SpinnerColumn(spinner_name="dots", style="bold red"),
            TextColumn("[bold white]{task.description}"),
            BarColumn(bar_width=30, style="red", complete_style="green"),
            TextColumn("[green]{task.completed}[white]/[white]{task.total}"),
            console=console,
            transient=True,
        ) as progress:
            tache = progress.add_task("Génération...", total=nombre)
            for _ in range(nombre):
                ips.append(generer_ip_publique())
                progress.advance(tache)

        table = Table(
            title=f"[bold red]{nombre} IPs Générées[/bold red]",
            box=box.DOUBLE_EDGE,
            border_style="red",
            header_style="bold red",
            show_lines=True,
        )
        table.add_column("#", justify="right", width=6, style="dim")
        table.add_column("Adresse IP", style="cyan", width=18)

        for i, ip in enumerate(ips, start=1):
            table.add_row(str(i), ip)

        console.print()
        console.print(table)
        console.print()

        save = console.input(
            "[bold red][[/bold red][bold white]?[/bold white][bold red]][/bold red] "
            "Sauvegarder dans un fichier ? [bold white](oui/non)[/bold white] : "
        ).strip().lower()
        if save in ("oui", "o", "yes", "y"):
            chemin = "ips_generes.txt"
            with open(chemin, "w") as f:
                f.write("\n".join(ips))
            console.print(f"[bold green][✓] Sauvegardé dans {chemin}[/bold green]")

        if webhook_url:
            console.print("[dim]Envoi au webhook Discord...[/dim]")
            if envoyer_webhook(webhook_url, ips):
                console.print("[bold green][✓] Envoyé avec succès.[/bold green]")
            else:
                console.print("[bold red][!] Échec de l'envoi au webhook.[/bold red]")

    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold red][!] Interrompu.[/bold red]")

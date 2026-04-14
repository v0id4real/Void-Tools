import re
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich import box

console = Console()

TIMEOUT = 8
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}

PORTS_COMMUNS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 6379: "Redis", 8080: "HTTP-alt", 27017: "MongoDB",
}


def extraire_domaine(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    parsed = urlparse(url)
    return parsed.netloc or parsed.path.split("/")[0], url


def resoudre_ip(domaine):
    try:
        return socket.gethostbyname(domaine)
    except socket.gaierror:
        return None


def obtenir_statut(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        return resp.status_code, resp.elapsed.total_seconds()
    except requests.RequestException:
        return None, None


def lookup_ip(ip):
    try:
        resp = requests.get(
            f"https://ip-api.com/json/{ip}?fields=status,isp,org,as,country,regionName,city",
            timeout=TIMEOUT
        )
        data = resp.json()
        if data.get("status") == "success":
            return data
    except requests.RequestException:
        pass
    return {}


def scanner_port(ip, port, service):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        ouvert = sock.connect_ex((ip, port)) == 0
    except socket.error:
        ouvert = False
    finally:
        sock.close()
    return port, service, ouvert


def scanner_ports(ip):
    resultats = {}
    with ThreadPoolExecutor(max_workers=20) as ex:
        futures = {ex.submit(scanner_port, ip, p, s): p for p, s in PORTS_COMMUNS.items()}
        for fut in as_completed(futures):
            port, service, ouvert = fut.result()
            resultats[port] = (service, ouvert)
    return resultats


def afficher(url_original, domaine, url, ip, statut_http, temps_rep, infos_ip, ports):
    console.print()

    table = Table(
        title=f"[bold red]Analyse Complète[/bold red] — [bold white]{domaine}[/bold white]",
        box=box.DOUBLE_EDGE, border_style="red", header_style="bold red", show_lines=True,
    )
    table.add_column("Champ", style="bold white", width=22)
    table.add_column("Valeur", style="cyan")

    securise = url.startswith("https://")
    couleur_https = "green" if securise else "red"
    couleur_statut = "green" if statut_http and 200 <= statut_http < 400 else "red"

    table.add_row("URL", url)
    table.add_row("Domaine", domaine)
    table.add_row("HTTPS", f"[{couleur_https}]{'Oui' if securise else 'Non'}[/{couleur_https}]")
    table.add_row("Code HTTP", f"[{couleur_statut}]{statut_http or 'N/A'}[/{couleur_statut}]")
    table.add_row("Temps réponse", f"{temps_rep:.2f}s" if temps_rep else "N/A")
    table.add_row("IP", ip or "Impossible de résoudre")

    if infos_ip:
        table.add_row("Pays",         infos_ip.get("country",    "N/A"))
        table.add_row("Région",       infos_ip.get("regionName", "N/A"))
        table.add_row("Ville",        infos_ip.get("city",       "N/A"))
        table.add_row("FAI",          infos_ip.get("isp",        "N/A"))
        table.add_row("Organisation", infos_ip.get("org",        "N/A"))
        table.add_row("AS",           infos_ip.get("as",         "N/A"))

    console.print(table)
    console.print()

    table_ports = Table(
        title="[bold red]Scan des Ports[/bold red]",
        box=box.DOUBLE_EDGE, border_style="red", header_style="bold red", show_lines=True,
    )
    table_ports.add_column("Statut", justify="center", width=10)
    table_ports.add_column("Port", justify="right", width=8)
    table_ports.add_column("Service", style="bold white", width=14)

    ouverts = [(p, s) for p, (s, o) in sorted(ports.items()) if o]
    fermes  = [(p, s) for p, (s, o) in sorted(ports.items()) if not o]

    for p, s in ouverts:
        table_ports.add_row("[bold green]  OUVERT[/bold green]", str(p), s)
    for p, s in fermes:
        table_ports.add_row("[red]  FERMÉ[/red]", f"[dim]{p}[/dim]", f"[dim]{s}[/dim]")

    console.print(table_ports)
    console.print()
    console.print(Panel(
        f"[bold green]  Ports ouverts : {len(ouverts)}[/bold green]   [bold red]  Fermés : {len(fermes)}[/bold red]",
        border_style="dim white",
    ))
    console.print()


if __name__ == "__main__":
    try:
        console.print()
        console.print(Panel(
            "[bold red]VOID[/bold red] — [bold white]IP All Lookup[/bold white]",
            border_style="red", box=box.DOUBLE_EDGE,
        ))
        console.print()
        console.print("[dim]Exemple : https://discord.com[/dim]")
        console.print()

        url_input = console.input(
            "[bold red][[/bold red][bold white]=[/bold white][bold red]][/bold red] URL du site web : "
        ).strip()

        if not url_input:
            console.print("[bold red][!] URL vide. Annulé.[/bold red]")
            raise SystemExit(0)

        domaine, url = extraire_domaine(url_input)

        with Progress(
            SpinnerColumn(spinner_name="dots", style="bold red"),
            TextColumn("[bold white]{task.description}"),
            console=console, transient=True,
        ) as p:
            t = p.add_task("Résolution DNS...", total=None)
            ip = resoudre_ip(domaine)

            p.update(t, description="Vérification HTTP...")
            statut_http, temps_rep = obtenir_statut(url)

            p.update(t, description="Lookup IP...")
            infos_ip = lookup_ip(ip) if ip else {}

            p.update(t, description="Scan des ports...")

        ports = {}
        if ip:
            with Progress(
                SpinnerColumn(spinner_name="dots", style="bold red"),
                TextColumn("[bold white]{task.description}"),
                BarColumn(bar_width=30, style="red", complete_style="green"),
                TextColumn("[green]{task.completed}[white]/[white]{task.total}"),
                TimeElapsedColumn(),
                console=console, transient=True,
            ) as progress:
                tache = progress.add_task("Scan ports...", total=len(PORTS_COMMUNS))
                with ThreadPoolExecutor(max_workers=20) as ex:
                    futures = {ex.submit(scanner_port, ip, port, svc): port for port, svc in PORTS_COMMUNS.items()}
                    for fut in as_completed(futures):
                        port, service, ouvert = fut.result()
                        ports[port] = (service, ouvert)
                        progress.advance(tache)

        afficher(url_input, domaine, url, ip, statut_http, temps_rep, infos_ip, ports)

    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold red][!] Interrompu.[/bold red]")

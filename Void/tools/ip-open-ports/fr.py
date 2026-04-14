import re
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich import box

console = Console()

IP_REGEX = re.compile(
    r'^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$'
)

PORTS_COMMUNS = {
    21:    "FTP",
    22:    "SSH",
    23:    "Telnet",
    25:    "SMTP",
    53:    "DNS",
    80:    "HTTP",
    110:   "POP3",
    143:   "IMAP",
    443:   "HTTPS",
    445:   "SMB",
    3306:  "MySQL",
    3389:  "RDP",
    5432:  "PostgreSQL",
    6379:  "Redis",
    8080:  "HTTP-alt",
    8443:  "HTTPS-alt",
    27017: "MongoDB",
}


def scanner_port(ip, port, service):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        result = sock.connect_ex((ip, port))
        ouvert = result == 0
    except socket.error:
        ouvert = False
    finally:
        sock.close()
    return port, service, ouvert


def scanner_ports(ip):
    resultats = []
    with Progress(
        SpinnerColumn(spinner_name="dots", style="bold red"),
        TextColumn("[bold white]{task.description}"),
        BarColumn(bar_width=30, style="red", complete_style="green"),
        TextColumn("[green]{task.completed}[white]/[white]{task.total}"),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:
        tache = progress.add_task("Scan des ports...", total=len(PORTS_COMMUNS))

        with ThreadPoolExecutor(max_workers=20) as ex:
            futures = {
                ex.submit(scanner_port, ip, port, service): (port, service)
                for port, service in PORTS_COMMUNS.items()
            }
            for fut in as_completed(futures):
                port, service, ouvert = fut.result()
                resultats.append((port, service, ouvert))
                progress.advance(tache)

    return sorted(resultats, key=lambda x: x[0])


def afficher(ip, resultats):
    ouverts = [(p, s) for p, s, o in resultats if o]
    fermes  = [(p, s) for p, s, o in resultats if not o]

    table = Table(
        title=f"[bold red]Ports Ouverts[/bold red] — [bold white]{ip}[/bold white]",
        box=box.DOUBLE_EDGE,
        border_style="red",
        header_style="bold red",
        show_lines=True,
    )
    table.add_column("Statut", justify="center", width=10)
    table.add_column("Port", justify="right", width=8)
    table.add_column("Service", style="bold white", width=14)

    for port, service in ouverts:
        table.add_row("[bold green]  OUVERT[/bold green]", str(port), service)
    for port, service in fermes:
        table.add_row("[red]  FERMÉ[/red]", f"[dim]{port}[/dim]", f"[dim]{service}[/dim]")

    console.print()
    console.print(table)
    console.print()
    console.print(Panel(
        f"[bold green]  Ouverts : {len(ouverts)}[/bold green]   [bold red]  Fermés : {len(fermes)}[/bold red]",
        border_style="dim white",
    ))
    console.print()


if __name__ == "__main__":
    try:
        console.print()
        console.print(Panel(
            "[bold red]VOID[/bold red] — [bold white]IP Open Ports[/bold white]",
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

        resultats = scanner_ports(ip)
        afficher(ip, resultats)

    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold red][!] Interrompu.[/bold red]")

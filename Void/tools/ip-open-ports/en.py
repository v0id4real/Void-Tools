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

COMMON_PORTS = {
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


def scan_port(ip, port, service):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        result = sock.connect_ex((ip, port))
        open_ = result == 0
    except socket.error:
        open_ = False
    finally:
        sock.close()
    return port, service, open_


def scan_ports(ip):
    results = []
    with Progress(
        SpinnerColumn(spinner_name="dots", style="bold red"),
        TextColumn("[bold white]{task.description}"),
        BarColumn(bar_width=30, style="red", complete_style="green"),
        TextColumn("[green]{task.completed}[white]/[white]{task.total}"),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("Scanning ports...", total=len(COMMON_PORTS))

        with ThreadPoolExecutor(max_workers=20) as ex:
            futures = {
                ex.submit(scan_port, ip, port, service): (port, service)
                for port, service in COMMON_PORTS.items()
            }
            for fut in as_completed(futures):
                port, service, open_ = fut.result()
                results.append((port, service, open_))
                progress.advance(task)

    return sorted(results, key=lambda x: x[0])


def display(ip, results):
    open_ports   = [(p, s) for p, s, o in results if o]
    closed_ports = [(p, s) for p, s, o in results if not o]

    table = Table(
        title=f"[bold red]Open Ports[/bold red] — [bold white]{ip}[/bold white]",
        box=box.DOUBLE_EDGE,
        border_style="red",
        header_style="bold red",
        show_lines=True,
    )
    table.add_column("Status", justify="center", width=10)
    table.add_column("Port", justify="right", width=8)
    table.add_column("Service", style="bold white", width=14)

    for port, service in open_ports:
        table.add_row("[bold green]  OPEN[/bold green]", str(port), service)
    for port, service in closed_ports:
        table.add_row("[red]  CLOSED[/red]", f"[dim]{port}[/dim]", f"[dim]{service}[/dim]")

    console.print()
    console.print(table)
    console.print()
    console.print(Panel(
        f"[bold green]  Open: {len(open_ports)}[/bold green]   [bold red]  Closed: {len(closed_ports)}[/bold red]",
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
            "[bold red][[/bold red][bold white]=[/bold white][bold red]][/bold red] IP Address: "
        ).strip()

        if not ip:
            console.print("[bold red][!] Empty address. Cancelled.[/bold red]")
            raise SystemExit(0)

        if not IP_REGEX.match(ip):
            console.print(f"[bold red][!] Invalid IP format:[/bold red] {ip}")
            raise SystemExit(0)

        results = scan_ports(ip)
        display(ip, results)

    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold red][!] Interrupted.[/bold red]")

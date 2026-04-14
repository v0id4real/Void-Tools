import re
import socket
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

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 6379: "Redis", 8080: "HTTP-alt", 27017: "MongoDB",
}


def extract_domain(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    parsed = urlparse(url)
    return parsed.netloc or parsed.path.split("/")[0], url


def resolve_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None


def get_http_status(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        return resp.status_code, resp.elapsed.total_seconds()
    except requests.RequestException:
        return None, None


def ip_lookup(ip):
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


def scan_port(ip, port, service):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        open_ = sock.connect_ex((ip, port)) == 0
    except socket.error:
        open_ = False
    finally:
        sock.close()
    return port, service, open_


def display(url_input, domain, url, ip, http_status, response_time, ip_info, ports):
    console.print()

    table = Table(
        title=f"[bold red]Full Analysis[/bold red] — [bold white]{domain}[/bold white]",
        box=box.DOUBLE_EDGE, border_style="red", header_style="bold red", show_lines=True,
    )
    table.add_column("Field", style="bold white", width=20)
    table.add_column("Value", style="cyan")

    secure = url.startswith("https://")
    https_color = "green" if secure else "red"
    status_color = "green" if http_status and 200 <= http_status < 400 else "red"

    table.add_row("URL",           url)
    table.add_row("Domain",        domain)
    table.add_row("HTTPS",         f"[{https_color}]{'Yes' if secure else 'No'}[/{https_color}]")
    table.add_row("HTTP Status",   f"[{status_color}]{http_status or 'N/A'}[/{status_color}]")
    table.add_row("Response Time", f"{response_time:.2f}s" if response_time else "N/A")
    table.add_row("IP",            ip or "Could not resolve")

    if ip_info:
        table.add_row("Country",      ip_info.get("country",    "N/A"))
        table.add_row("Region",       ip_info.get("regionName", "N/A"))
        table.add_row("City",         ip_info.get("city",       "N/A"))
        table.add_row("ISP",          ip_info.get("isp",        "N/A"))
        table.add_row("Organization", ip_info.get("org",        "N/A"))
        table.add_row("AS",           ip_info.get("as",         "N/A"))

    console.print(table)
    console.print()

    table_ports = Table(
        title="[bold red]Port Scan[/bold red]",
        box=box.DOUBLE_EDGE, border_style="red", header_style="bold red", show_lines=True,
    )
    table_ports.add_column("Status", justify="center", width=10)
    table_ports.add_column("Port", justify="right", width=8)
    table_ports.add_column("Service", style="bold white", width=14)

    open_ports   = [(p, s) for p, (s, o) in sorted(ports.items()) if o]
    closed_ports = [(p, s) for p, (s, o) in sorted(ports.items()) if not o]

    for p, s in open_ports:
        table_ports.add_row("[bold green]  OPEN[/bold green]", str(p), s)
    for p, s in closed_ports:
        table_ports.add_row("[red]  CLOSED[/red]", f"[dim]{p}[/dim]", f"[dim]{s}[/dim]")

    console.print(table_ports)
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
            "[bold red]VOID[/bold red] — [bold white]IP All Lookup[/bold white]",
            border_style="red", box=box.DOUBLE_EDGE,
        ))
        console.print()
        console.print("[dim]Example: https://discord.com[/dim]")
        console.print()

        url_input = console.input(
            "[bold red][[/bold red][bold white]=[/bold white][bold red]][/bold red] Website URL: "
        ).strip()

        if not url_input:
            console.print("[bold red][!] Empty URL. Cancelled.[/bold red]")
            raise SystemExit(0)

        domain, url = extract_domain(url_input)

        with Progress(
            SpinnerColumn(spinner_name="dots", style="bold red"),
            TextColumn("[bold white]{task.description}"),
            console=console, transient=True,
        ) as p:
            t = p.add_task("Resolving DNS...", total=None)
            ip = resolve_ip(domain)

            p.update(t, description="Checking HTTP status...")
            http_status, response_time = get_http_status(url)

            p.update(t, description="IP Lookup...")
            ip_info = ip_lookup(ip) if ip else {}

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
                task = progress.add_task("Scanning ports...", total=len(COMMON_PORTS))
                with ThreadPoolExecutor(max_workers=20) as ex:
                    futures = {ex.submit(scan_port, ip, port, svc): port for port, svc in COMMON_PORTS.items()}
                    for fut in as_completed(futures):
                        port, service, open_ = fut.result()
                        ports[port] = (service, open_)
                        progress.advance(task)

        display(url_input, domain, url, ip, http_status, response_time, ip_info, ports)

    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold red][!] Interrupted.[/bold red]")

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


def get_operator(ip):
    resp = requests.get(
        f"https://ip-api.com/json/{ip}?fields=status,message,isp,org,as,asname,query",
        timeout=TIMEOUT
    )
    resp.raise_for_status()
    return resp.json()


def display(ip, data):
    if data.get("status") == "fail":
        console.print(f"[bold red][!] API error: {data.get('message', 'Unknown')}[/bold red]")
        return

    table = Table(
        title=f"[bold red]IP Operator[/bold red] — [bold white]{ip}[/bold white]",
        box=box.DOUBLE_EDGE,
        border_style="red",
        header_style="bold red",
        show_lines=True,
    )
    table.add_column("Field", style="bold white", width=20)
    table.add_column("Value", style="cyan")

    table.add_row("IP",           data.get("query",  "N/A"))
    table.add_row("ISP",          data.get("isp",    "N/A"))
    table.add_row("Organization", data.get("org",    "N/A"))
    table.add_row("AS",           data.get("as",     "N/A"))
    table.add_row("AS Name",      data.get("asname", "N/A"))

    console.print()
    console.print(table)
    console.print()


if __name__ == "__main__":
    try:
        console.print()
        console.print(Panel(
            "[bold red]VOID[/bold red] — [bold white]IP Operator[/bold white]",
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

        with Progress(
            SpinnerColumn(spinner_name="dots", style="bold red"),
            TextColumn("[bold white]{task.description}"),
            console=console, transient=True,
        ) as p:
            p.add_task("Fetching operator info...", total=None)
            data = get_operator(ip)

        display(ip, data)

    except requests.RequestException as e:
        console.print(f"[bold red][!] Network error: {e}[/bold red]")
    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold red][!] Interrupted.[/bold red]")

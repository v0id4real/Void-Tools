import re
import subprocess
import platform
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

console = Console()

IP_REGEX = re.compile(
    r'^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$'
)


def ping(ip, count=4):
    system = platform.system().lower()
    if system == "windows":
        cmd = ["ping", "-n", str(count), ip]
        encoding = "cp850"
    else:
        cmd = ["ping", "-c", str(count), ip]
        encoding = "utf-8"

    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
        )
        output = proc.stdout.decode(encoding, errors="replace")
        success = "TTL" in output or "ttl" in output or proc.returncode == 0
        return success, output
    except subprocess.TimeoutExpired:
        return False, "Timeout expired."
    except FileNotFoundError:
        return False, "Ping command not found."
    except Exception as e:
        return False, str(e)


if __name__ == "__main__":
    try:
        console.print()
        console.print(Panel(
            "[bold red]VOID[/bold red] — [bold white]IP Pinger[/bold white]",
            border_style="red", box=box.DOUBLE_EDGE,
        ))
        console.print()

        ip = console.input(
            "[bold red][[/bold red][bold white]=[/bold white][bold red]][/bold red] IP address to ping: "
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
            p.add_task(f"Pinging {ip}...", total=None)
            success, result = ping(ip)

        if success:
            console.print(Panel(
                f"[bold green]  Ping successful to {ip}[/bold green]",
                border_style="green", box=box.DOUBLE_EDGE,
            ))
        else:
            console.print(Panel(
                f"[bold red]  Ping failed to {ip}[/bold red]",
                border_style="red", box=box.DOUBLE_EDGE,
            ))

        console.print()
        console.print(f"[dim]{result}[/dim]")

    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold red][!] Interrupted.[/bold red]")

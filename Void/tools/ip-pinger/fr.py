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


def pinger(ip, count=4):
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
        succes = "TTL" in output or "ttl" in output or proc.returncode == 0
        return succes, output
    except subprocess.TimeoutExpired:
        return False, "Timeout dépassé."
    except FileNotFoundError:
        return False, "Commande ping introuvable."
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
            "[bold red][[/bold red][bold white]=[/bold white][bold red]][/bold red] Adresse IP à pinger : "
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
            p.add_task(f"Ping vers {ip}...", total=None)
            succes, resultat = pinger(ip)

        if succes:
            console.print(Panel(
                f"[bold green]  Ping réussi vers {ip}[/bold green]",
                border_style="green", box=box.DOUBLE_EDGE,
            ))
        else:
            console.print(Panel(
                f"[bold red]  Ping échoué vers {ip}[/bold red]",
                border_style="red", box=box.DOUBLE_EDGE,
            ))

        console.print()
        console.print(f"[dim]{resultat}[/dim]")

    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold red][!] Interrompu.[/bold red]")

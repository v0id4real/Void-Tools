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


def is_public(ip_str):
    try:
        ip = ipaddress.ip_address(ip_str)
        return not any(ip in net for net in RESERVED_NETWORKS)
    except ValueError:
        return False


def generate_public_ip():
    while True:
        ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        if is_public(ip):
            return ip


def send_webhook(url, ips):
    content = "\n".join(f"`{ip}`" for ip in ips)
    payload = {"content": f"**Generated IPs:**\n{content}"}
    try:
        resp = requests.post(url, json=payload, timeout=TIMEOUT)
        return resp.status_code == 204
    except requests.RequestException:
        return False


def ask_count():
    while True:
        try:
            n = int(console.input(
                "[bold red][[/bold red][bold white]=[/bold white][bold red]][/bold red] "
                "Number of IPs to generate: "
            ).strip())
            if n > 0:
                return n
            console.print("[bold red][!] Enter a number greater than 0.[/bold red]")
        except ValueError:
            console.print("[bold red][!] Invalid input. Enter an integer.[/bold red]")


if __name__ == "__main__":
    try:
        console.print()
        console.print(Panel(
            "[bold red]VOID[/bold red] — [bold white]IP Generator[/bold white]",
            border_style="red", box=box.DOUBLE_EDGE,
        ))
        console.print()

        count = ask_count()

        webhook_url = console.input(
            "[bold red][[/bold red][bold white]=[/bold white][bold red]][/bold red] "
            "Discord Webhook URL (leave empty to skip): "
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
            task = progress.add_task("Generating...", total=count)
            for _ in range(count):
                ips.append(generate_public_ip())
                progress.advance(task)

        table = Table(
            title=f"[bold red]{count} Generated IPs[/bold red]",
            box=box.DOUBLE_EDGE,
            border_style="red",
            header_style="bold red",
            show_lines=True,
        )
        table.add_column("#", justify="right", width=6, style="dim")
        table.add_column("IP Address", style="cyan", width=18)

        for i, ip in enumerate(ips, start=1):
            table.add_row(str(i), ip)

        console.print()
        console.print(table)
        console.print()

        save = console.input(
            "[bold red][[/bold red][bold white]?[/bold white][bold red]][/bold red] "
            "Save to file? [bold white](yes/no)[/bold white]: "
        ).strip().lower()
        if save in ("yes", "y", "oui", "o"):
            path = "generated_ips.txt"
            with open(path, "w") as f:
                f.write("\n".join(ips))
            console.print(f"[bold green][✓] Saved to {path}[/bold green]")

        if webhook_url:
            console.print("[dim]Sending to Discord webhook...[/dim]")
            if send_webhook(webhook_url, ips):
                console.print("[bold green][✓] Sent successfully.[/bold green]")
            else:
                console.print("[bold red][!] Failed to send to webhook.[/bold red]")

    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold red][!] Interrupted.[/bold red]")

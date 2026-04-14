import requests
import webbrowser
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich import box

console = Console()

SITES = {
    "Twitter":    "https://twitter.com/{}",
    "Facebook":   "https://www.facebook.com/{}",
    "Instagram":  "https://www.instagram.com/{}",
    "GitHub":     "https://github.com/{}",
    "Reddit":     "https://www.reddit.com/user/{}",
    "LinkedIn":   "https://www.linkedin.com/in/{}",
    "Pinterest":  "https://www.pinterest.com/{}",
    "Tumblr":     "https://{}.tumblr.com",
    "YouTube":    "https://www.youtube.com/{}",
    "Vimeo":      "https://vimeo.com/{}",
    "TikTok":     "https://www.tiktok.com/@{}",
    "Twitch":     "https://www.twitch.tv/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Medium":     "https://medium.com/@{}",
    "DeviantArt": "https://www.deviantart.com/{}",
    "Behance":    "https://www.behance.net/{}",
    "Flickr":     "https://www.flickr.com/people/{}",
    "Dribbble":   "https://dribbble.com/{}",
    "Patreon":    "https://www.patreon.com/{}",
    "Goodreads":  "https://www.goodreads.com/{}",
    "GitLab":     "https://gitlab.com/{}",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

NOT_FOUND_INDICATORS = [
    "page not found", "user not found", "profile not found",
    "this account doesn't exist", "sorry, this page isn't available",
    "404", "doesn't exist",
]


def check_username(site, url_template, username):
    url = url_template.format(username)
    try:
        response = requests.get(url, headers=HEADERS, timeout=8, allow_redirects=True)
        if response.status_code == 404:
            return (site, False, None)
        if response.status_code == 200:
            content_lower = response.text.lower()
            for indicator in NOT_FOUND_INDICATORS:
                if indicator in content_lower:
                    return (site, False, None)
            return (site, True, url)
        return (site, False, None)
    except requests.RequestException:
        return (site, False, None)


def main(username):
    console.print()
    console.print(Panel(
        f"[bold red]Searching for:[/bold red] [bold white]{username}[/bold white]\n"
        f"[dim]Checking across {len(SITES)} platforms...[/dim]",
        title="[bold red]  VOID — NAME TRACKER  [/bold red]",
        border_style="red",
        box=box.DOUBLE_EDGE,
    ))
    console.print()

    found = []
    not_found = []

    with Progress(
        SpinnerColumn(spinner_name="dots", style="bold red"),
        TextColumn("[bold white]{task.description}"),
        BarColumn(bar_width=30, style="red", complete_style="green"),
        TextColumn("[green]{task.completed}[white]/[white]{task.total}"),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("Scanning...", total=len(SITES))

        with ThreadPoolExecutor(max_workers=15) as executor:
            futures = {
                executor.submit(check_username, site, url, username): site
                for site, url in SITES.items()
            }
            for future in as_completed(futures):
                site, exists, url = future.result()
                if exists:
                    found.append((site, url))
                else:
                    not_found.append(site)
                progress.advance(task)

    table = Table(
        title=f"[bold white]Results for[/bold white] [bold red]{username}[/bold red]",
        box=box.DOUBLE_EDGE,
        border_style="red",
        header_style="bold red",
        show_lines=True,
    )
    table.add_column("Status", justify="center", width=8)
    table.add_column("Platform", justify="left", width=14)
    table.add_column("URL", justify="left")

    for site, url in sorted(found, key=lambda x: x[0]):
        table.add_row("[bold green]  FOUND[/bold green]", f"[bold white]{site}[/bold white]", f"[cyan]{url}[/cyan]")

    for site in sorted(not_found):
        table.add_row("[red]  ABSENT[/red]", f"[dim]{site}[/dim]", "[dim]—[/dim]")

    console.print(table)
    console.print()

    console.print(Panel(
        f"[bold green]  Found: {len(found)}[/bold green]   [bold red]  Absent: {len(not_found)}[/bold red]",
        title="[bold white]Summary[/bold white]",
        border_style="dim white",
    ))
    console.print()

    if found:
        try:
            answer = console.input("[bold red][[/bold red][bold white]?[/bold white][bold red]][/bold red] Open found links in browser? [bold white](yes/no)[/bold white]: ").strip().lower()
            if answer in ("yes", "y", "oui", "o"):
                for _, url in found:
                    webbrowser.open(url)
                console.print("[bold green][✓] Links opened.[/bold green]")
        except (KeyboardInterrupt, EOFError):
            pass


if __name__ == "__main__":
    try:
        console.print()
        username = console.input("[bold red][[/bold red][bold white]=[/bold white][bold red]][/bold red] Enter the username to search: ").strip()
        if not username:
            console.print("[bold red][!] Empty username. Cancelled.[/bold red]")
        else:
            main(username)
    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold red][!] Interrupted.[/bold red]")

import re
import concurrent.futures
import dns.resolver
import dns.exception
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

console = Console()

HUNTER_API_KEY = '432dfd7cbfec2b733603e519786b4156a789bac3'
REPUTATION_API = "https://email-reputation.api.useinsider.com/lookup/{}"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}
EMAIL_REGEX = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')

TIMEOUT = 6


def _join_or_na(val):
    if isinstance(val, list) and val:
        return "\n".join(val)
    return "[dim]N/A[/dim]"


def resolve_dns(domain, rtype):
    try:
        return [str(r.exchange if rtype == 'MX' else r) for r in dns.resolver.resolve(domain, rtype)]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout, Exception):
        return None


def fetch_details(email):
    parts = email.split('@')
    full_domain = parts[-1]
    username = parts[0]
    match = re.search(r"@([^@.]+)\.", email)
    domain_name = match.group(1) if match else None
    tld = f".{email.split('.')[-1]}"

    dns_queries = {
        "mx_servers":    (full_domain, 'MX'),
        "spf_records":   (full_domain, 'SPF'),
        "dmarc_records": (f'_dmarc.{full_domain}', 'TXT'),
        "txt_records":   (full_domain, 'TXT'),
        "srv_records":   (f'_sip._tcp.{full_domain}', 'SRV'),
        "a_records":     (full_domain, 'A'),
        "aaaa_records":  (full_domain, 'AAAA'),
    }

    details = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        futures = {ex.submit(resolve_dns, dom, rtype): key for key, (dom, rtype) in dns_queries.items()}
        for fut in concurrent.futures.as_completed(futures):
            key = futures[fut]
            details[key] = fut.result()

    try:
        rep_resp = requests.get(REPUTATION_API.format(email), headers=HEADERS, timeout=TIMEOUT)
        details["reputation"] = rep_resp.json().get("reputation", "N/A")
    except Exception:
        details["reputation"] = "N/A"

    return details, full_domain, domain_name, tld, username


def verify_email(email):
    url = (
        f'https://api.hunter.io/v2/email-verifier?email={email}'
        f'&api_key={HUNTER_API_KEY}'
    )
    try:
        resp = requests.get(url, headers={'Accept': 'application/json'}, timeout=TIMEOUT)
        data = resp.json()
        status = data.get('data', {}).get('status', 'unknown')
        score = data.get('data', {}).get('score', 'N/A')
        return status, score
    except Exception:
        return 'error', 'N/A'


def display_results(email, details, full_domain, domain_name, tld, username, verif_status, verif_score):
    table_base = Table(
        title="[bold red]Email Information[/bold red]",
        box=box.DOUBLE_EDGE,
        border_style="red",
        header_style="bold red",
        show_lines=True,
    )
    table_base.add_column("Field", style="bold white", width=20)
    table_base.add_column("Value", style="cyan")

    status_color = "green" if verif_status == "valid" else "red"
    table_base.add_row("Email", email)
    table_base.add_row("Username", username or "N/A")
    table_base.add_row("Domain Name", domain_name or "N/A")
    table_base.add_row("TLD", tld or "N/A")
    table_base.add_row("Full Domain", full_domain or "N/A")
    table_base.add_row("Status (Hunter.io)", f"[{status_color}]{verif_status}[/{status_color}]")
    table_base.add_row("Hunter.io Score", str(verif_score))
    table_base.add_row("Reputation", str(details.get("reputation", "N/A")))

    console.print()
    console.print(table_base)

    table_dns = Table(
        title="[bold red]DNS Records[/bold red]",
        box=box.DOUBLE_EDGE,
        border_style="red",
        header_style="bold red",
        show_lines=True,
    )
    table_dns.add_column("Type", style="bold white", width=10)
    table_dns.add_column("Value(s)", style="cyan")

    dns_fields = [
        ("MX",    details.get("mx_servers")),
        ("SPF",   details.get("spf_records")),
        ("DMARC", details.get("dmarc_records")),
        ("TXT",   details.get("txt_records")),
        ("SRV",   details.get("srv_records")),
        ("A",     details.get("a_records")),
        ("AAAA",  details.get("aaaa_records")),
    ]
    for rtype, val in dns_fields:
        table_dns.add_row(rtype, _join_or_na(val))

    console.print(table_dns)
    console.print()


if __name__ == "__main__":
    try:
        console.print()
        console.print(Panel(
            "[bold red]VOID[/bold red] — [bold white]Email Info[/bold white]",
            border_style="red",
            box=box.DOUBLE_EDGE,
        ))
        console.print()

        email_input = console.input("[bold red][[/bold red][bold white]=[/bold white][bold red]][/bold red] Enter email: ").strip()

        if not email_input:
            console.print("[bold red][!] Empty email address. Cancelled.[/bold red]")
            raise SystemExit(0)

        if not EMAIL_REGEX.match(email_input):
            console.print(f"[bold red][!] Invalid email format:[/bold red] [white]{email_input}[/white]")
            raise SystemExit(0)

        with Progress(
            SpinnerColumn(spinner_name="dots", style="bold red"),
            TextColumn("[bold white]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            progress.add_task("Fetching DNS information...", total=None)
            details, full_domain, domain_name, tld, username = fetch_details(email_input)
            verif_status, verif_score = verify_email(email_input)

        display_results(
            email_input, details, full_domain, domain_name,
            tld, username, verif_status, verif_score
        )

    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold red][!] Interrupted.[/bold red]")

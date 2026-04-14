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


def resolver_dns(domaine, rtype):
    try:
        return [str(r.exchange if rtype == 'MX' else r) for r in dns.resolver.resolve(domaine, rtype)]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout, Exception):
        return None


def recuperer_details(email):
    parties = email.split('@')
    domaine_complet = parties[-1]
    nom_utilisateur = parties[0]
    match = re.search(r"@([^@.]+)\.", email)
    nom_domaine = match.group(1) if match else None
    tld = f".{email.split('.')[-1]}"

    dns_queries = {
        "mx_servers":    (domaine_complet, 'MX'),
        "spf_records":   (domaine_complet, 'SPF'),
        "dmarc_records": (f'_dmarc.{domaine_complet}', 'TXT'),
        "txt_records":   (domaine_complet, 'TXT'),
        "srv_records":   (f'_sip._tcp.{domaine_complet}', 'SRV'),
        "a_records":     (domaine_complet, 'A'),
        "aaaa_records":  (domaine_complet, 'AAAA'),
    }

    details = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        futures = {ex.submit(resolver_dns, dom, rtype): key for key, (dom, rtype) in dns_queries.items()}
        for fut in concurrent.futures.as_completed(futures):
            key = futures[fut]
            details[key] = fut.result()

    try:
        rep_resp = requests.get(REPUTATION_API.format(email), headers=HEADERS, timeout=TIMEOUT)
        details["reputation"] = rep_resp.json().get("reputation", "N/A")
    except Exception:
        details["reputation"] = "N/A"

    return details, domaine_complet, nom_domaine, tld, nom_utilisateur


def verifier_email(email):
    url = (
        f'https://api.hunter.io/v2/email-verifier?email={email}'
        f'&api_key={HUNTER_API_KEY}'
    )
    try:
        resp = requests.get(url, headers={'Accept': 'application/json'}, timeout=TIMEOUT)
        data = resp.json()
        statut = data.get('data', {}).get('status', 'inconnu')
        score = data.get('data', {}).get('score', 'N/A')
        return statut, score
    except Exception:
        return 'erreur', 'N/A'


def afficher_resultats(email, details, domaine_complet, nom_domaine, tld, nom_utilisateur, statut_verif, score_verif):
    table_base = Table(
        title="[bold red]Informations Email[/bold red]",
        box=box.DOUBLE_EDGE,
        border_style="red",
        header_style="bold red",
        show_lines=True,
    )
    table_base.add_column("Champ", style="bold white", width=22)
    table_base.add_column("Valeur", style="cyan")

    couleur_statut = "green" if statut_verif == "valid" else "red"
    table_base.add_row("Email", email)
    table_base.add_row("Nom d'utilisateur", nom_utilisateur or "N/A")
    table_base.add_row("Nom de domaine", nom_domaine or "N/A")
    table_base.add_row("TLD", tld or "N/A")
    table_base.add_row("Domaine complet", domaine_complet or "N/A")
    table_base.add_row("Statut (Hunter.io)", f"[{couleur_statut}]{statut_verif}[/{couleur_statut}]")
    table_base.add_row("Score Hunter.io", str(score_verif))
    table_base.add_row("Réputation", str(details.get("reputation", "N/A")))

    console.print()
    console.print(table_base)

    table_dns = Table(
        title="[bold red]Enregistrements DNS[/bold red]",
        box=box.DOUBLE_EDGE,
        border_style="red",
        header_style="bold red",
        show_lines=True,
    )
    table_dns.add_column("Type", style="bold white", width=10)
    table_dns.add_column("Valeur(s)", style="cyan")

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

        email_input = console.input("[bold red][[/bold red][bold white]=[/bold white][bold red]][/bold red] Entrez l'email : ").strip()

        if not email_input:
            console.print("[bold red][!] Adresse email vide. Annulé.[/bold red]")
            raise SystemExit(0)

        if not EMAIL_REGEX.match(email_input):
            console.print(f"[bold red][!] Format email invalide :[/bold red] [white]{email_input}[/white]")
            raise SystemExit(0)

        with Progress(
            SpinnerColumn(spinner_name="dots", style="bold red"),
            TextColumn("[bold white]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            t1 = progress.add_task("Récupération des informations DNS...", total=None)
            details, domaine_complet, nom_domaine, tld, nom_utilisateur = recuperer_details(email_input)
            progress.update(t1, description="Vérification Hunter.io...")
            statut_verif, score_verif = verifier_email(email_input)

        afficher_resultats(
            email_input, details, domaine_complet, nom_domaine,
            tld, nom_utilisateur, statut_verif, score_verif
        )

    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold red][!] Interrompu.[/bold red]")

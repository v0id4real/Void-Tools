import phonenumbers
from phonenumbers import geocoder, carrier, timezone as ph_timezone
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

NUMBER_TYPES = {
    phonenumbers.PhoneNumberType.MOBILE:               "Mobile",
    phonenumbers.PhoneNumberType.FIXED_LINE:           "Fixed Line",
    phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed or Mobile",
    phonenumbers.PhoneNumberType.TOLL_FREE:            "Toll Free",
    phonenumbers.PhoneNumberType.PREMIUM_RATE:         "Premium Rate",
    phonenumbers.PhoneNumberType.SHARED_COST:          "Shared Cost",
    phonenumbers.PhoneNumberType.VOIP:                 "VoIP",
    phonenumbers.PhoneNumberType.PERSONAL_NUMBER:      "Personal",
    phonenumbers.PhoneNumberType.PAGER:                "Pager",
    phonenumbers.PhoneNumberType.UAN:                  "UAN",
    phonenumbers.PhoneNumberType.UNKNOWN:              "Unknown",
}


def analyze_number(phone_number):
    try:
        parsed = phonenumbers.parse(phone_number, None)
    except phonenumbers.NumberParseException as e:
        return None, f"Cannot parse number: {e}"

    if not phonenumbers.is_valid_number(parsed):
        return None, "Invalid number"

    country_code = f"+{parsed.country_code}"
    operator = carrier.name_for_number(parsed, "en") or "Unknown"
    num_type = NUMBER_TYPES.get(phonenumbers.number_type(parsed), "Unknown")
    timezones = ph_timezone.time_zones_for_number(parsed)
    tz = timezones[0] if timezones else "Unknown"
    country = phonenumbers.region_code_for_number(parsed) or "Unknown"
    region = geocoder.description_for_number(parsed, "en") or "Unknown"
    national_fmt = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
    intl_fmt = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    possible = phonenumbers.is_possible_number(parsed)

    info = {
        "Input Number":        phone_number,
        "National Format":     national_fmt,
        "International Format": intl_fmt,
        "Status":              "[bold green]Valid[/bold green]",
        "Possible":            "[bold green]Yes[/bold green]" if possible else "[bold red]No[/bold red]",
        "Country Code":        country_code,
        "Country":             country,
        "Region":              region,
        "Timezone":            tz,
        "Operator":            operator,
        "Number Type":         num_type,
    }
    return info, None


def display(info):
    table = Table(
        title="[bold red]Phone Number Information[/bold red]",
        box=box.DOUBLE_EDGE,
        border_style="red",
        header_style="bold red",
        show_lines=True,
    )
    table.add_column("Field", style="bold white", width=22)
    table.add_column("Value", style="cyan")

    for field, value in info.items():
        table.add_row(field, str(value))

    console.print()
    console.print(table)
    console.print()


if __name__ == "__main__":
    try:
        console.print()
        console.print(Panel(
            "[bold red]VOID[/bold red] — [bold white]Number Info[/bold white]",
            border_style="red",
            box=box.DOUBLE_EDGE,
        ))
        console.print()

        number = console.input(
            "[bold red][[/bold red][bold white]=[/bold white][bold red]][/bold red] "
            "Phone number (with country code, e.g. +33612345678): "
        ).strip()

        if not number:
            console.print("[bold red][!] Empty number. Cancelled.[/bold red]")
            raise SystemExit(0)

        info, error = analyze_number(number)

        if error:
            console.print(f"[bold red][!] {error}[/bold red]")
        else:
            display(info)

    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold red][!] Interrupted.[/bold red]")

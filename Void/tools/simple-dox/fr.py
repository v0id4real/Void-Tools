import os
from colorama import Fore, init
init(autoreset=True)

path =os.getcwd () 

def collecter_informations(nom_dox):
    save_directory = fr"{path}\Void - Output\Save-Dox"
    
    pseudo = input(Fore.RED + "[?] Entrez le pseudo de la personne: ")
    nom = input(Fore.RED + "[?] Entrez le nom, prénom de la personne: ")
    age = input(Fore.RED + "[?] Entrez l'âge de la personne: ")
    adresse = input(Fore.RED + "[?] Entrez l'adresse de la personne: ")
    numero_telephone = input(Fore.RED + "[?] Entrez le numéro de téléphone de la personne: ")
    adresse_ip = input(Fore.RED + "[?] Entrez l'adresse IP de la personne: ")
    
    output_file_path = os.path.join(save_directory, f"{nom_dox}.txt")
    with open(output_file_path, "w") as file:
        file.write("Informations collectées :\n")
        file.write(f"Nom: {nom}\n")
        file.write(f"Pseudo: {pseudo}\n")
        file.write(f"Âge: {age}\n")
        file.write(f"Adresse: {adresse}\n")
        file.write(f"Numéro de téléphone: {numero_telephone}\n")
        file.write(f"Adresse IP de la personne: {adresse_ip}\n")
    
    return output_file_path

if __name__ == "__main__":
    print(Fore.RED + "[=] Bienvenue dans le simple Dox Creator!")
    nom_dox = input(Fore.RED + "[?] Entrez le nom du DOX: ")
    output_file_path = collecter_informations(nom_dox)
    print(Fore.GREEN + f"[+] Le fichier {nom_dox}.txt a été sauvegardé dans : {output_file_path}")
    input(Fore.YELLOW + "[!] Appuyez sur Entrée pour continuer...")

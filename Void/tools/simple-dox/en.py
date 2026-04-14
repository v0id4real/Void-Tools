import os
from colorama import Fore, init
init(autoreset=True)
path =os.getcwd () 

def collect_information(nom_dox):
    save_directory = fr"{path}\Void - Output\Save-Dox"

    
    pseudo = input(Fore.RED + "[?] Enter the person's username: ")
    nom = input(Fore.RED + "[?] Enter the person's full name: ")
    age = input(Fore.RED + "[?] Enter the person's age: ")
    address = input(Fore.RED + "[?] Enter the person's address: ")
    phone_number = input(Fore.RED + "[?] Enter the person's phone number: ")
    ip_address = input(Fore.RED + "[?] Enter the person's IP address: ")
    
    output_file_path = os.path.join(save_directory, f"{nom_dox}.txt")
    with open(output_file_path, "w") as file:
        file.write("Collected Information:\n")
        file.write(f"Name: {nom}\n")
        file.write(f"Username: {pseudo}\n")
        file.write(f"Age: {age}\n")
        file.write(f"Address: {address}\n")
        file.write(f"Phone Number: {phone_number}\n")
        file.write(f"Person's IP Address: {ip_address}\n")
    
    return output_file_path

if __name__ == "__main__":
    print(Fore.RED + "[=] Welcome to Simple Dox Creator!")
    nom_dox = input(Fore.RED + "[?] Enter the DOX name: ")
    output_file_path = collect_information(nom_dox)
    print(Fore.GREEN + f"[+] The file {nom_dox}.txt has been saved to: {output_file_path}")
    input(Fore.YELLOW + "[!] Press Enter to continue...")

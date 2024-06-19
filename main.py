from openai import OpenAI
import sys

# Définition d'un prompt système que l'IA utilisera pour commenter le code.
SYSTEM_PROMPT = """
Tu es un assistant IA chargé d'aider les développeurs à commenter leurs codes. 
Ton rôle est de retourner le code python commenté de la manière qui t'es demandé.
N'ajoutes aucun mot clef et retourne seulement le code commenté, sans précisé le language du code.
"""

def main():
    """
    Fonction principale qui réalise les étapes suivantes:
    1. Obtient le fichier Python à commenter.
    2. Lit le contenu du fichier.
    3. Crée un prompt basé sur le code lu.
    4. Appelle le modèle de langage pour générer les commentaires.
    5. Écrit le code commenté dans le fichier.
    """
    # Obtient le nom du fichier Python depuis les arguments de la ligne de commande.
    python_file = get_python_file()  
    # Ouvre et lit le contenu du fichier Python.
    if python_file != None:
        code = open_python_file(python_file)
        # Crée un prompt à partir du code lu.
        prompt = create_prompt(code)
        print(prompt)
        # Appelle le modèle de langage pour obtenir le code commenté.
        commented_code = call_llm(prompt)
        print(commented_code)
        # Écrit le code commenté dans le fichier original.
        write_python_file(python_file, commented_code)
    else:
        pass


def get_python_file() -> str:
    """
    Récupère le nom du fichier Python à commenter depuis les arguments de la ligne de commande.
    
    Returns:
        str: Le nom du fichier Python si fourni, None sinon.
    """
    # Vérifie le nombre d'arguments passés en ligne de commande.
    if len(sys.argv) > 2:
        print("Usage : Python main.py <fichier_a_commenter.py>")
    else: 
        # Retourne le premier argument (le nom du fichier Python).
        return sys.argv[1]
    
    return None


def open_python_file(python_file: str) -> str:
    """
    Ouvre et lit le contenu du fichier Python spécifié.
    
    Args:
        python_file (str): Le nom du fichier Python.
        
    Returns:
        str: Le contenu du fichier.
    """
    # Ouvre le fichier en mode lecture et lit son contenu.
    with open(python_file, 'r') as file:
        code = file.read()
        
    return code


def call_llm(prompt: str) -> str:
    """
    Appelle le modèle de langage pour générer les commentaires pour le code fourni.
    
    Args:
        prompt (str): Le prompt à envoyer au modèle de langage.
        
    Returns:
        str: Le code commenté généré par le modèle de langage.
    """
    # Initialise le client OpenAI avec les informations d'authentification.
    client = OpenAI(
        organization="org-hxzkzI0BvBrIUBTCM8Ukg4hX",
        project="proj_egQnKwuK7lvmdC38Xoed2wUj",
        api_key="sk-proj-PBRVTyzyE9gr11SM9BCaT3BlbkFJRsoyXsoWbavK6pR5iWhD"
    )

    # Envoie le prompt au modèle de langage pour obtenir le code commenté.
    commented_code = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, 
                  {"role": "user", "content": prompt}]
    )

    return commented_code.choices[0].message.content


def create_prompt(code: str) -> str:
    """
    Crée un prompt pour le modèle de langage basé sur le code à commenter.
    
    Args:
        code (str): Le code source à commenter.
        
    Returns:
        str: Un prompt prêt à être envoyé au modèle de langage.
    """
    template = f"""Je souhaites que tu commentes le code suivant : 

    {code}

    Je souhaites que tu commentes chaque fonction en ajoutant dans leurs documentation un docstring ultra-complet et en ajoutant le type des variables.
    Je souhaites aussi que tu ajoutes un commentaire à chaque ligne de code ou bloc de code complexe.

    """
    return template


def write_python_file(python_file: str, commented_code: str) -> None:
    """
    Écrit le code commenté dans le fichier Python spécifié.
    
    Args:
        python_file (str): Le nom du fichier Python.
        commented_code (str): Le code commenté à écrire dans le fichier.
    """
    # Ouvre le fichier en mode écriture et enregistre le code commenté.
    with open(python_file, 'w') as file:
        file.write(commented_code)



# Vérifie si le script est exécuté en tant que programme principal.
if __name__ == '__main__':
    main()
import os
import random
import string

class Utils:
  @staticmethod
  def format_prix(valeur):
    return f"{valeur:,.2f}".replace(",", " ").replace(".", ",")

  @staticmethod
  def generer_phrase(min_mots=1, max_mots=4, min_lettres=4, max_lettres=10):
      nb_mots = random.randint(min_mots, max_mots)
      mots = []

      for _ in range(nb_mots):
          longueur = random.randint(min_lettres, max_lettres)
          mot = "".join(random.choice(string.ascii_lowercase) for _ in range(longueur))
          mots.append(mot)

      return " ".join(mots)

  @staticmethod
  def get_limit():
        return 100
   
  @staticmethod
  def dir_folder_photos_produits():
    # Récupère le dossier où se trouve le fichier actuel
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Si utils.py est dans un sous-dossier, on remonte d'un cran (optionnel selon ta structure)
    racine_projet = os.path.dirname(current_dir) 
    
    # Construction du chemin
    path = os.path.join(racine_projet, "resources", "uploads", "photos_produits")
    
    # ASTUCE : Créer le dossier automatiquement s'il n'existe pas
    if not os.path.exists(path):
        os.makedirs(path)
        
    return path  
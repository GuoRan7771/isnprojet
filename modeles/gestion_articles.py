# modeles/gestion_articles.py
from modeles.gestion_donnees import GestionDonnees
import os
import uuid # Pour générer des ID uniques plus robustes

CHEMIN_ARTICLES = "donnees/articles.json"

def charger_articles():
    """Charge tous les articles depuis le fichier JSON."""
    print("--- Début charger_articles ---")
    try:
        donnees = GestionDonnees.charger_donnees(CHEMIN_ARTICLES)
        if not isinstance(donnees, list):
            print(f"AVERTISSEMENT: Le contenu de {CHEMIN_ARTICLES} n'est pas une liste valide. Type: {type(donnees)}. Initialisation à [].")
            sauvegarder_articles([])
            return []
        print(f"--- Fin charger_articles (Succès, {len(donnees)} articles chargés) ---")
        return donnees
    except FileNotFoundError:
        print(f"ERREUR: Fichier non trouvé - {CHEMIN_ARTICLES}. Création d'un fichier vide.")
        sauvegarder_articles([])
        return []
    except Exception as e:
        print(f"ERREUR CRITIQUE dans charger_articles: {e}")
        import traceback
        traceback.print_exc()
        return []

def sauvegarder_articles(articles):
    """Sauvegarde la liste complète des articles dans le fichier JSON."""
    if not isinstance(articles, list):
        print(f"ERREUR: Tentative de sauvegarde de données non-liste dans {CHEMIN_ARTICLES}. Type: {type(articles)}")
        return False
    print(f"--- Début sauvegarde articles ({len(articles)} articles) ---")
    try:
        GestionDonnees.sauvegarder_donnees(CHEMIN_ARTICLES, articles)
        print("--- Fin sauvegarde articles (Succès) ---")
        return True
    except Exception as e:
        print(f"ERREUR CRITIQUE lors de la sauvegarde dans {CHEMIN_ARTICLES}: {e}")
        import traceback
        traceback.print_exc()
        return False

def obtenir_prochain_id_article():
     """ Génère un ID unique pour un nouvel article (type UUID). """
     # Utiliser UUID est plus sûr pour éviter les collisions si on supprime/réutilise des IDs numériques
     return str(uuid.uuid4()) # Retourne une chaîne unique

     # Alternative simple (moins robuste si on supprime des articles):
     # articles = charger_articles()
     # if not articles: return "article_1"
     # max_num = 0
     # for art in articles:
     #     if isinstance(art, dict) and art.get("id_article", "").startswith("article_"):
     #         try:
     #             num = int(art["id_article"].split("_")[-1])
     #             if num > max_num: max_num = num
     #         except ValueError:
     #             continue # Ignorer les ID mal formatés
     # return f"article_{max_num + 1}"


def ajouter_article(titre, contenu):
    """Ajoute un nouvel article."""
    print("--- Début ajouter_article ---")
    if not titre or not contenu:
        print("ERREUR: Titre et contenu sont requis.")
        return False

    articles = charger_articles()
    if not isinstance(articles, list):
        print("ERREUR: Impossible de charger les articles pour en ajouter un.")
        articles = []

    # Vérifier si un article avec le même titre existe déjà (optionnel)
    # for art in articles:
    #     if isinstance(art, dict) and art.get("titre", "").lower() == titre.lower():
    #         print(f"AVERTISSEMENT: Un article avec le titre '{titre}' existe déjà. Ajout annulé.")
    #         return False

    nouvel_id = obtenir_prochain_id_article()

    nouvel_article = {
        "id_article": nouvel_id,
        "titre": titre.strip(),
        "contenu": contenu.strip(),
        "mots_cles_ids": [] # Liste vide au début, sera remplie par la fonctionnalité "划词"
    }

    articles.append(nouvel_article)

    if sauvegarder_articles(articles):
        print(f"Article '{titre}' ajouté avec succès (ID: {nouvel_id}).")
        print("--- Fin ajouter_article (Succès) ---")
        return nouvel_id
    else:
        print(f"ERREUR: Échec de la sauvegarde après tentative d'ajout de l'article '{titre}'.")
        print("--- Fin ajouter_article (Échec Sauvegarde) ---")
        return False

def obtenir_liste_articles():
    """Retourne une liste de tuples (id_article, titre) pour affichage."""
    print("--- Début obtenir_liste_articles ---")
    articles = charger_articles()
    liste_simple = []
    if isinstance(articles, list):
        for art in articles:
            if isinstance(art, dict):
                id_art = art.get("id_article")
                titre_art = art.get("titre", "Sans Titre")
                if id_art:
                    liste_simple.append((id_art, titre_art))
    print(f"--- Fin obtenir_liste_articles ({len(liste_simple)} articles trouvés) ---")
    return liste_simple

def obtenir_details_article(id_article):
    """Retourne le dictionnaire complet d'un article par son ID."""
    print(f"--- Début obtenir_details_article (ID: {id_article}) ---")
    articles = charger_articles()
    if isinstance(articles, list):
        for art in articles:
            if isinstance(art, dict) and art.get("id_article") == id_article:
                print("--- Fin obtenir_details_article (Trouvé) ---")
                return art
    print("--- Fin obtenir_details_article (Non trouvé) ---")
    return None

def ajouter_ou_modifier_article(donnees_article):
    """
    Ajoute un nouvel article ou modifie un article existant.
    :param donnees_article: Dictionnaire contenant les infos de l'article.
                           Doit contenir 'id_article' pour une modification.
    :return: True si succès, False sinon.
    """
    print(f"[mod_articles] Tentative d'ajout/modification avec données: {{'titre': '{donnees_article.get('titre')}', ...}}") # Log partiel
    try:
        articles = charger_articles()
        id_a_traiter = donnees_article.get("id_article")

        if id_a_traiter:
            # --- Modification ---
            article_trouve = False
            for i, article in enumerate(articles):
                if article.get("id_article") == id_a_traiter:
                    articles[i].update({k: v for k, v in donnees_article.items() if k != "id_article"})
                    articles[i]["id_article"] = id_a_traiter # Assurer présence ID
                    article_trouve = True
                    print(f"[mod_articles] Article ID {id_a_traiter} mis à jour.")
                    break
            if not article_trouve:
                print(f"[mod_articles] ERREUR: Article ID {id_a_traiter} non trouvé pour modification.")
                return False
        else:
            # --- Ajout ---
            nouvel_id = str(uuid.uuid4())
            donnees_article["id_article"] = nouvel_id
            # Ajouter d'autres champs par défaut si nécessaire
            articles.append(donnees_article)
            print(f"[mod_articles] Nouvel article ajouté avec ID {nouvel_id}.")

        # Sauvegarder
        success = GestionDonnees.sauvegarder_donnees(CHEMIN_ARTICLES, articles)
        if success:
            print("[mod_articles] Liste d'articles sauvegardée avec succès.")
            return True
        else:
            print("[mod_articles] ERREUR lors de la sauvegarde de la liste d'articles.")
            return False

    except Exception as e:
        print(f"[mod_articles] ERREUR dans ajouter_ou_modifier_article: {e}")
        import traceback
        traceback.print_exc()
        return False

def supprimer_article(id_article):
    """Supprime un article par son ID (id_article). Retourne True si succès, False sinon."""
    print(f"[mod_articles] Demande de suppression pour article ID: {id_article}")
    articles = charger_articles()
    if not isinstance(articles, list):
        print("[mod_articles] ERREUR: Impossible de charger les articles pour suppression.")
        return False
    taille_avant = len(articles)
    articles_mis_a_jour = [art for art in articles if not (isinstance(art, dict) and art.get("id_article") == id_article)]
    taille_apres = len(articles_mis_a_jour)
    if taille_avant == taille_apres:
        print(f"[mod_articles] AVERTISSEMENT: Article avec ID {id_article} non trouvé pour suppression.")
        return False
    if sauvegarder_articles(articles_mis_a_jour):
        print(f"[mod_articles] Article ID {id_article} supprimé avec succès.")
        return True
    else:
        print(f"[mod_articles] ERREUR: Échec de la sauvegarde après suppression de l'article ID {id_article}.")
        return False
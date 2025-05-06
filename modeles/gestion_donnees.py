# 开发时间 : 2025/5/2 3:55
# -*- coding: utf-8 -*-
# Dans modeles/gestion_donnees.py

import json
import os
import uuid # Pour générer des IDs uniques
import traceback # Pour imprimer les erreurs détaillées

class GestionDonnees:
    """
    Gère la lecture et l'écriture des données des articles
    dans un fichier JSON.
    """
    def __init__(self, chemin_fichier='donnees/articles.json'):
        """
        Initialise le gestionnaire de données.

        Args:
            chemin_fichier (str): Le chemin vers le fichier JSON de stockage.
        """
        self.chemin_fichier = chemin_fichier
        self.chemin_dossier = os.path.dirname(chemin_fichier)
        print(f"[Modèle] Initialisation avec fichier: {self.chemin_fichier}")
        # S'assurer que le dossier existe, sinon le créer
        if not os.path.exists(self.chemin_dossier):
            try:
                print(f"[Modèle] Le dossier {self.chemin_dossier} n'existe pas, tentative de création...")
                os.makedirs(self.chemin_dossier)
                print(f"[Modèle] Dossier {self.chemin_dossier} créé avec succès.")
            except OSError as e:
                print(f"[Modèle] ERREUR FATALE: Impossible de créer le dossier {self.chemin_dossier}: {e}")
                # On pourrait lever une exception ici pour arrêter proprement
                # raise Exception(f"Impossible de créer le dossier de données: {e}")
                self.chemin_fichier = None # Indiquer que le stockage n'est pas possible

        # S'assurer que le fichier existe, sinon le créer avec une liste vide
        if self.chemin_fichier and not os.path.exists(self.chemin_fichier):
            print(f"[Modèle] Le fichier {self.chemin_fichier} n'existe pas, tentative de création avec une liste vide...")
            self.sauvegarder_articles([]) # Sauvegarde une liste vide pour créer le fichier

    def charger_articles(self):
        """
        Charge la liste des articles depuis le fichier JSON.

        Returns:
            list: Une liste de dictionnaires représentant les articles.
                  Retourne une liste vide en cas d'erreur ou si le fichier n'existe pas.
        """
        print(f"[Modèle] --- Début charger_articles depuis {self.chemin_fichier} ---")
        if not self.chemin_fichier or not os.path.exists(self.chemin_fichier):
            print(f"[Modèle] Avertissement: Fichier {self.chemin_fichier} non trouvé ou chemin invalide. Retourne une liste vide.")
            return []
        try:
            with open(self.chemin_fichier, 'r', encoding='utf-8') as f:
                articles = json.load(f)
                # Vérifier si ce qui est chargé est bien une liste
                if not isinstance(articles, list):
                    print(f"[Modèle] ERREUR: Le contenu de {self.chemin_fichier} n'est pas une liste JSON valide. Retourne une liste vide.")
                    return []
                print(f"[Modèle] --- Fin charger_articles (Succès, {len(articles)} articles chargés) ---")
                return articles
        except json.JSONDecodeError as e:
            print(f"[Modèle] ERREUR: Impossible de décoder le JSON depuis {self.chemin_fichier}. Fichier peut-être corrompu? {e}")
            traceback.print_exc()
            return [] # Retourne une liste vide en cas d'erreur de décodage
        except Exception as e:
            print(f"[Modèle] ERREUR inattendue lors du chargement de {self.chemin_fichier}: {e}")
            traceback.print_exc()
            return [] # Retourne une liste vide pour toute autre erreur

    def sauvegarder_articles(self, articles):
        """
        Sauvegarde la liste des articles dans le fichier JSON.

        Args:
            articles (list): La liste des dictionnaires d'articles à sauvegarder.

        Returns:
            bool: True si la sauvegarde a réussi, False sinon.
        """
        print(f"[Modèle] --- Début sauvegarde articles ({len(articles)} articles) dans {self.chemin_fichier} ---")
        if not self.chemin_fichier:
             print("[Modèle] ERREUR: Chemin de fichier non défini, sauvegarde annulée.")
             return False
        if not isinstance(articles, list):
             print(f"[Modèle] ERREUR: Tentative de sauvegarde de données qui ne sont pas une liste ({type(articles)}). Sauvegarde annulée.")
             return False

        try:
            # S'assurer que le dossier existe toujours (au cas où il aurait été supprimé entre temps)
            if not os.path.exists(self.chemin_dossier):
                print(f"[Modèle] Le dossier {self.chemin_dossier} n'existe plus, tentative de re-création...")
                os.makedirs(self.chemin_dossier)

            # Écrire dans le fichier
            with open(self.chemin_fichier, 'w', encoding='utf-8') as f:
                # indent=4 pour une meilleure lisibilité du fichier JSON
                # ensure_ascii=False pour correctement gérer les caractères non-ASCII (comme les accents)
                json.dump(articles, f, indent=4, ensure_ascii=False)
            print(f"[Modèle] --- Fin sauvegarde dans {self.chemin_fichier} (Succès) ---")
            return True
        except Exception as e:
            print(f"[Modèle] ERREUR lors de la sauvegarde dans {self.chemin_fichier}: {e}")
            traceback.print_exc()
            return False # Retourne False en cas d'erreur

    def ajouter_article(self, titre, contenu):
        """
        Ajoute un nouvel article à la liste et sauvegarde.

        Args:
            titre (str): Le titre du nouvel article.
            contenu (str): Le contenu du nouvel article.

        Returns:
            bool: True si l'ajout et la sauvegarde ont réussi, False sinon.
        """
        print(f"[Modèle] --- Début ajouter_article (Titre: {titre}) ---")
        articles = self.charger_articles() # Charge la liste actuelle

        # Créer le dictionnaire pour le nouvel article
        nouvel_article = {
            "id_article": str(uuid.uuid4()), # Génère un ID unique universel
            "titre": titre,
            "contenu": contenu
            # Ajouter d'autres champs si nécessaire (date_creation, etc.)
        }
        print(f"[Modèle] Nouvel article créé avec ID: {nouvel_article['id_article']}")

        # Ajouter le nouvel article à la liste
        articles.append(nouvel_article)

        # Sauvegarder la liste mise à jour
        succes_sauvegarde = self.sauvegarder_articles(articles)

        if succes_sauvegarde:
             print(f"[Modèle] Article '{titre}' ajouté avec succès et liste sauvegardée.")
             print("[Modèle] --- Fin ajouter_article (Succès) ---")
             return True
        else:
             print(f"[Modèle] ERREUR: L'article '{titre}' a été ajouté en mémoire mais la sauvegarde a échoué.")
             print("[Modèle] --- Fin ajouter_article (Échec Sauvegarde) ---")
             # On pourrait essayer d'annuler l'ajout en mémoire ici, mais c'est complexe.
             # Le plus simple est de signaler l'échec.
             return False

    # --- NOUVELLE MÉTHODE POUR LA SUPPRESSION ---
    def supprimer_article(self, id_article_a_supprimer):
        """
        Supprime un article de la liste basé sur son ID et sauvegarde.

        Args:
            id_article_a_supprimer (str): L'ID de l'article à supprimer.

        Returns:
            bool: True si l'article a été trouvé, supprimé et la liste sauvegardée.
                  False si l'article n'a pas été trouvé ou si la sauvegarde a échoué.
        """
        print(f"[Modèle] --- Début supprimer_article (ID: {id_article_a_supprimer}) ---")
        if not id_article_a_supprimer:
            print("[Modèle] ERREUR: Tentative de suppression avec un ID vide.")
            return False

        articles = self.charger_articles()
        longueur_initiale = len(articles)
        article_trouve = False

        # Créer une nouvelle liste sans l'article à supprimer
        # C'est plus sûr que de modifier la liste pendant l'itération
        articles_mis_a_jour = []
        for article in articles:
            if article.get("id_article") == id_article_a_supprimer:
                article_trouve = True
                print(f"[Modèle] Article à supprimer trouvé: ID={id_article_a_supprimer}, Titre='{article.get('titre', 'N/A')}'")
                # Ne pas ajouter cet article à la nouvelle liste
            else:
                articles_mis_a_jour.append(article)

        # Vérifier si l'article a été trouvé
        if article_trouve:
            # Vérifier si la longueur a bien diminué (double sécurité)
            if len(articles_mis_a_jour) == longueur_initiale - 1:
                print("[Modèle] Article retiré de la liste en mémoire. Tentative de sauvegarde...")
                # Sauvegarder la liste mise à jour (sans l'article supprimé)
                succes_sauvegarde = self.sauvegarder_articles(articles_mis_a_jour)
                if succes_sauvegarde:
                    print(f"[Modèle] Article ID {id_article_a_supprimer} supprimé avec succès du fichier.")
                    print("[Modèle] --- Fin supprimer_article (Succès) ---")
                    return True
                else:
                    print(f"[Modèle] ERREUR: L'article ID {id_article_a_supprimer} a été trouvé mais la sauvegarde a échoué!")
                    print("[Modèle] --- Fin supprimer_article (Échec Sauvegarde) ---")
                    return False
            else:
                # Ne devrait pas arriver si la logique est correcte, mais sécurité
                print(f"[Modèle] ERREUR: Article trouvé mais la taille de la liste n'a pas diminué comme prévu!")
                print("[Modèle] --- Fin supprimer_article (Erreur Logique) ---")
                return False
        else:
            # Si l'article n'a pas été trouvé dans la liste
            print(f"[Modèle] ERREUR: Article avec ID {id_article_a_supprimer} non trouvé dans le fichier.")
            print("[Modèle] --- Fin supprimer_article (Non Trouvé) ---")
            return False

    # --- Méthodes à implémenter pour Ouvrir/Modifier ---
    # def obtenir_details_article(self, id_article):
    #     print(f"[Modèle] Recherche des détails pour l'article ID: {id_article}")
    #     articles = self.charger_articles()
    #     for article in articles:
    #         if article.get("id_article") == id_article:
    #             print(f"[Modèle] Article trouvé: {article.get('titre')}")
    #             return article # Retourne le dictionnaire complet
    #     print(f"[Modèle] Article ID {id_article} non trouvé.")
    #     return None # Retourne None si non trouvé

    # def modifier_article(self, id_article, nouveau_titre, nouveau_contenu):
    #     print(f"[Modèle] Tentative de modification de l'article ID: {id_article}")
    #     articles = self.charger_articles()
    #     article_modifie = False
    #     for article in articles:
    #         if article.get("id_article") == id_article:
    #             print(f"[Modèle] Article trouvé. Mise à jour Titre='{nouveau_titre}', Contenu='{nouveau_contenu[:30]}...'")
    #             article["titre"] = nouveau_titre
    #             article["contenu"] = nouveau_contenu
    #             # Mettre à jour d'autres champs si nécessaire (ex: date_modification)
    #             article_modifie = True
    #             break # Sortir de la boucle une fois l'article trouvé et modifié

    #     if article_modifie:
    #         print("[Modèle] Article modifié en mémoire. Tentative de sauvegarde...")
    #         succes_sauvegarde = self.sauvegarder_articles(articles)
    #         if succes_sauvegarde:
    #             print("[Modèle] Modifications sauvegardées avec succès.")
    #             return True
    #         else:
    #             print("[Modèle] ERREUR: Modification effectuée en mémoire mais sauvegarde échouée!")
    #             return False
    #     else:
    #         print(f"[Modèle] ERREUR: Article ID {id_article} non trouvé pour modification.")
    #         return False
    def charger_donnees(chemin_fichier):
        """
        Charge les données depuis un fichier JSON.
        Retourne les données décodées (typiquement une liste ou un dictionnaire).
        Retourne une liste vide si le fichier n'existe pas ou est vide.
        :param chemin_fichier: Le chemin complet vers le fichier JSON.
        :return: Les données chargées ou une liste vide en cas d'erreur ou fichier non trouvé.
        """
        print(f"[Gestion Données] Tentative de chargement depuis: {chemin_fichier}")
        try:
            # Vérifier si le fichier existe
            if not os.path.exists(chemin_fichier):
                print(f"[Gestion Données] Fichier non trouvé: {chemin_fichier}. Retourne une liste vide.")
                return [] # Ou {} si vous préférez un dictionnaire vide par défaut

            # Lire le fichier
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                # Vérifier si le fichier est vide
                contenu = f.read()
                if not contenu:
                    print(f"[Gestion Données] Fichier vide: {chemin_fichier}. Retourne une liste vide.")
                    return [] # Ou {}
                # Si non vide, essayer de décoder le JSON
                donnees = json.loads(contenu)
                print(f"[Gestion Données] Données chargées avec succès depuis {chemin_fichier}.")
                return donnees
        except json.JSONDecodeError as e:
            print(f"[Gestion Données] ERREUR: Échec du décodage JSON depuis {chemin_fichier} - {e}")
            # Gérer le cas d'un fichier JSON corrompu. Retourner une liste vide ou lever une exception ?
            return [] # Plus sûr de retourner une liste vide pour éviter de planter l'app
        except IOError as e:
            print(f"[Gestion Données] ERREUR: Échec de lecture du fichier {chemin_fichier} - {e}")
            return [] # Retourner une liste vide en cas d'erreur de lecture
        except Exception as e:
            print(f"[Gestion Données] ERREUR INATTENDUE lors du chargement depuis {chemin_fichier} - {e}")
            return []
    def sauvegarder_donnees(chemin_fichier, donnees):
        """
        Sauvegarde les données fournies dans un fichier JSON.
        Crée les répertoires parents si nécessaire.
        :param chemin_fichier: Le chemin complet vers le fichier JSON de destination.
        :param donnees: Les données à sauvegarder (doivent être sérialisables en JSON).
        :return: True si la sauvegarde a réussi, False sinon.
        """
        print(f"[Gestion Données] Tentative de sauvegarde vers: {chemin_fichier}")
        try:
            # Créer les répertoires parents si ils n'existent pas
            repertoire = os.path.dirname(chemin_fichier)
            if repertoire and not os.path.exists(repertoire):
                os.makedirs(repertoire)
                print(f"[Gestion Données] Répertoire créé: {repertoire}")

            # Écrire dans le fichier
            with open(chemin_fichier, 'w', encoding='utf-8') as f:
                # Utiliser indent=4 pour une meilleure lisibilité du fichier JSON
                json.dump(donnees, f, ensure_ascii=False, indent=4)
            print(f"[Gestion Données] Données sauvegardées avec succès dans {chemin_fichier}.")
            return True
        except IOError as e:
            print(f"[Gestion Données] ERREUR: Échec de l'écriture dans le fichier {chemin_fichier} - {e}")
            return False
        except TypeError as e:
            # Cela peut arriver si 'donnees' contient des objets non sérialisables en JSON
            print(f"[Gestion Données] ERREUR: Les données ne sont pas sérialisables en JSON pour {chemin_fichier} - {e}")
            return False
        except Exception as e:
            print(f"[Gestion Données] ERREUR INATTENDUE lors de la sauvegarde dans {chemin_fichier} - {e}")
            return False
    
    def charger_donnees(chemin_fichier):
        """
        Charge des données depuis un fichier JSON.
        Retourne une liste vide si le fichier n'existe pas ou est invalide.
        :param chemin_fichier: Le chemin complet vers le fichier JSON.
        :return: Les données chargées (souvent une liste de dictionnaires) ou une liste vide.
        """
        print(f"[Gestion Données] Tentative de chargement depuis: {chemin_fichier}")
        if not os.path.exists(chemin_fichier):
            print(f"[Gestion Données] Fichier non trouvé: {chemin_fichier}. Retourne [].")
            return [] # Retourner une liste vide si le fichier n'existe pas
        try:
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                donnees = json.load(f)
                # Optionnel: Vérifier si c'est bien une liste si c'est attendu
                if not isinstance(donnees, list):
                    print(f"[Gestion Données] AVERTISSEMENT: Données chargées depuis {chemin_fichier} ne sont pas une liste.")
                    # Décider quoi faire: retourner [] ou les données telles quelles?
                    # Pour être cohérent avec la gestion d'erreur initiale, retournons []
                    return []
                print(f"[Gestion Données] Données chargées avec succès depuis {chemin_fichier}.")
                return donnees
        except json.JSONDecodeError as e:
            print(f"[Gestion Données] ERREUR: Fichier JSON invalide {chemin_fichier} - {e}")
            return [] # Retourner une liste vide en cas d'erreur de décodage
        except Exception as e:
            print(f"[Gestion Données] ERREUR INATTENDUE lors du chargement depuis {chemin_fichier} - {e}")
            return [] # Retourner une liste vide pour les autres erreurs
    
    @staticmethod
    def sauvegarder_donnees(chemin_fichier, donnees):
        """
        Sauvegarde les données fournies (liste ou dictionnaire) dans un fichier JSON.

        :param chemin_fichier: Le chemin complet du fichier où sauvegarder.
        :param donnees: Les données à sauvegarder.
        :return: True si la sauvegarde réussit, False sinon.
        """
        try:
            # S'assurer que le répertoire parent existe, sinon le créer
            repertoire = os.path.dirname(chemin_fichier)
            if not os.path.exists(repertoire):
                os.makedirs(repertoire, exist_ok=True)
                print(f"[gestion_donnees] Répertoire créé: {repertoire}")

            # Écrire dans le fichier
            with open(chemin_fichier, 'w', encoding='utf-8') as f:
                # ensure_ascii=False pour supporter les caractères non-ASCII (comme le chinois)
                # indent=4 pour une meilleure lisibilité du fichier JSON
                json.dump(donnees, f, ensure_ascii=False, indent=4)

            print(f"[gestion_donnees] Données sauvegardées avec succès dans {chemin_fichier}")
            return True
        except IOError as e:
            print(f"[gestion_donnees] ERREUR d'entrée/sortie lors de la sauvegarde dans {chemin_fichier}: {e}")
            return False
        except Exception as e:
            print(f"[gestion_donnees] ERREUR inattendue lors de la sauvegarde dans {chemin_fichier}: {e}")
            return False
    
    @staticmethod
    def charger_donnees(chemin_fichier):
        """
        Charge les données depuis un fichier JSON.

        :param chemin_fichier: Le chemin complet du fichier à charger.
        :return: Les données chargées (typiquement une liste ou un dictionnaire),
                ou une liste vide [] si le fichier n'existe pas ou est invalide.
                (Adaptez la valeur de retour par défaut si nécessaire, ex: {} pour un dictionnaire)
        """
        valeur_par_defaut = [] # Ou {} si tu attends un dict par défaut
        if not os.path.exists(chemin_fichier):
            print(f"[gestion_donnees] Fichier {chemin_fichier} non trouvé. Retourne {valeur_par_defaut}.")
            return valeur_par_defaut

        try:
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                # Gérer le cas où le fichier est vide
                contenu = f.read()
                if not contenu:
                    print(f"[gestion_donnees] Fichier {chemin_fichier} est vide. Retourne {valeur_par_defaut}.")
                    return valeur_par_defaut
                # Rembobiner ou recharger pour lire le JSON
                f.seek(0) # Ou simplement utiliser json.load(f) si non vide
                donnees = json.load(f)
            print(f"[gestion_donnees] Données chargées avec succès depuis {chemin_fichier}")
            return donnees
        except json.JSONDecodeError as e:
            print(f"[gestion_donnees] ERREUR: Fichier {chemin_fichier} n'est pas un JSON valide ou est corrompu: {e}. Retourne {valeur_par_defaut}.")
            # Optionnel: sauvegarder le fichier corrompu avant de retourner vide
            # import shutil
            # shutil.copyfile(chemin_fichier, chemin_fichier + ".corrompu")
            return valeur_par_defaut
        except IOError as e:
            print(f"[gestion_donnees] ERREUR d'entrée/sortie lors du chargement depuis {chemin_fichier}: {e}. Retourne {valeur_par_defaut}.")
            return valeur_par_defaut
        except Exception as e:
            print(f"[gestion_donnees] ERREUR inattendue lors du chargement depuis {chemin_fichier}: {e}. Retourne {valeur_par_defaut}.")
            return valeur_par_defaut
# 开发时间 : 2025/5/2 3:53
# -*- coding: utf-8 -*-
# Dans controleur.py (ou votre fichier principal)

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import random
import os
# --- Utiliser les alias d'importation corrects ---
import modeles.vocabulaire as mod_vocab
import vues.vue_vocabulaire as vue_liste_mots_appris # Alias pour le module contenant VueListeMotsAppris
import vues.vue_details_mot as vue_details
import vues.vue_apprentissage as vue_app
import vues.vue_edition_mot as vue_edition

import modeles.gestion_articles as mod_articles
import vues.vue_liste_articles as vue_liste_articles_vue # Alias pour le module contenant VueListeArticles
import vues.vue_article as vue_article # Pour afficher les détails d'un article
# vue_import n'est plus nécessaire si on utilise filedialog directement
# import vues.vue_importation_article as vue_import

class Controleur:
    def __init__(self, root):
        """
        Initialise le contrôleur principal de l'application.
        :param root: La fenêtre racine Tkinter.
        """
        self.root = root
        self.vue_actuelle = None
        # --- Variables pour la session d'étude ---
        self.cartes_urgentes = []
        self.cartes_revision = []
        self.carte_actuelle_details = None # Stocke (id_mot, direction, maitrise) de la carte en cours
        self.details_mot_complets = None # Stocke le dictionnaire complet du mot en cours
        self.reponse_correcte_actuelle = "" # Stocke la réponse attendue pour la carte en cours
        self.id_article_en_cours = None # Pour filtrer l'étude par article
        self.mod_articles = mod_articles

        # --- Référence pour rafraîchissement ---
        # Garde une référence à la vue liste des articles pour pouvoir la rafraîchir
        self.vue_liste_articles_instance = None

        # --- Style et Configuration Fenêtre ---
        style = ttk.Style()
        try:
             style.theme_use('vista') # Ou 'xpnative', 'clam', 'alt', 'default', 'classic'
        except tk.TclError:
             print("Thème 'vista' non disponible, utilisation du thème par défaut.")
             style.theme_use('default')
        try:
            chemin_fichier_vocab = "donnees/vocabulaire.json" # Assurez-vous que le chemin est correct
            self.mod_vocab = mod_vocab
            print(f"[Contrôleur Init] Instance de ModeleVocabulaire créée avec succès depuis {chemin_fichier_vocab}.")
        except FileNotFoundError:
            print(f"[Contrôleur Init] ERREUR: Fichier vocabulaire non trouvé à {chemin_fichier_vocab}. Création d'un modèle vide.")
            # Gérer l'erreur, peut-être créer un modèle vide ou afficher un message
            self.mod_articles = mod_articles
        except Exception as e:
            print(f"[Contrôleur Init] ERREUR lors de l'initialisation de ModeleVocabulaire: {e}")
            # Gérer l'erreur critique
            raise

        self.root.title("App Aprentissage Langues")
        self.root.geometry("800x600")

        self.creer_navigation()
        # Afficher la vue initiale (par exemple, la liste des articles ou des mots)
        self.afficher_vue_liste_articles() # Ou afficher_vue_liste_mots()

    def creer_navigation(self):
        """Crée un cadre avec des boutons pour naviguer entre les vues principales."""
        frame_navigation = ttk.Frame(self.root, padding=(10, 5, 10, 5)) # Ajustement padding
        frame_navigation.pack(side="top", fill="x")

        btn_nav_mots = ttk.Button(frame_navigation, text="Liste Mots", command=self.afficher_vue_liste_mots)
        btn_nav_mots.pack(side="left", padx=5)

        btn_nav_articles = ttk.Button(frame_navigation, text="Liste Articles", command=self.afficher_vue_liste_articles)
        btn_nav_articles.pack(side="left", padx=5)

        # Ajouter d'autres boutons de navigation si nécessaire (ex: Démarrer Apprentissage global)
        # btn_nav_apprendre = ttk.Button(frame_navigation, text="Apprendre", command=self.afficher_vue_apprentissage)
        # btn_nav_apprendre.pack(side="left", padx=5)

    def effacer_vue_actuelle(self):
        """Détruit ou retire la vue actuellement affichée dans le cadre principal."""
        if self.vue_actuelle:
            print(f"[Contrôleur] Effacement de la vue actuelle: {type(self.vue_actuelle).__name__}")
            # Utiliser pack_forget() ou grid_forget() selon le gestionnaire de géométrie utilisé
            # Si toutes les vues principales utilisent pack:
            self.vue_actuelle.pack_forget()
            self.vue_actuelle.destroy()
            self.vue_actuelle = None
        # S'assurer que la référence à la liste article est aussi nettoyée si elle est détruite
        if not isinstance(self.vue_actuelle, vue_liste_articles_vue.VueListeArticles):
            self.vue_liste_articles_instance = None

    # --- Méthodes d'affichage des vues ---

    def afficher_vue_liste_mots(self):
        """Affiche la vue de la liste des mots appris."""
        print("[Contrôleur] Affichage de la vue liste des mots.")
        self.effacer_vue_actuelle()
        self.vue_actuelle = vue_liste_mots_appris.VueListeMotsAppris(self.root, self)
        self.vue_actuelle.pack(expand=True, fill='both', padx=10, pady=(0, 10)) # Ajuster padding si besoin
        # Pas besoin d'appeler rafraichir ici car la vue le fait dans son __init__ ou via charger_liste_mots

    def afficher_vue_liste_articles(self):
        """Affiche la vue listant les articles importés."""
        print("[Contrôleur] Affichage de la vue liste des articles.")
        self.effacer_vue_actuelle()
        self.vue_actuelle = vue_liste_articles_vue.VueListeArticles(self.root, self)
        self.vue_liste_articles_instance = self.vue_actuelle # Conserver la référence
        self.vue_actuelle.pack(expand=True, fill='both', padx=10, pady=10) # Ajuster padding
        # Pas besoin d'appeler rafraichir ici car la vue le fait dans son __init__ ou via charger_liste_articles

    def afficher_vue_apprentissage(self, id_article=None):
        """Affiche la vue d'apprentissage (jeu)."""
        print(f"[Contrôleur] Affichage de la vue apprentissage (Article ID: {id_article}).")
        self.id_article_en_cours = id_article # Mémoriser l'article pour la session
        self.effacer_vue_actuelle()
        self.vue_actuelle = vue_app.VueApprentissage(self.root, self)
        self.vue_actuelle.pack(expand=True, fill='both', padx=10, pady=10)
        self.demarrer_session_etude() # Lancer la logique d'étude

    def afficher_details_mot(self, id_mot):
        """Affiche les détails d'un mot dans une fenêtre Toplevel."""
        print(f"[Contrôleur] Affichage détails pour mot ID {id_mot}")
        details = mod_vocab.obtenir_details_mot(id_mot)
        if details:
            # Utiliser une fenêtre Toplevel pour les détails
            details_window = tk.Toplevel(self.root)
            details_window.title(f"Détails: {details.get('mot_anglais', 'Mot inconnu')}")
            # Assurez-vous que vue_details.VueDetailsMot existe et prend ces arguments
            vue_details.VueDetailsMot(details_window, self, details)
        else:
            messagebox.showerror("Erreur", f"Impossible de trouver les détails pour le mot ID {id_mot}", parent=self.root)

    def afficher_vue_edition_mot(self, mot_id=None, edition=False):
        """Affiche la vue pour ajouter ou modifier un mot."""
        print(f"[Contrôleur] Affichage vue édition mot (ID: {mot_id}, Edition: {edition})")
        try:
            details_mot = None
            if edition and mot_id:
                nom_methode_modele = 'obtenir_details_mot'
                if hasattr(self.mod_vocab, nom_methode_modele):
                    details_mot = getattr(self.mod_vocab, nom_methode_modele)(mot_id)
                    if not details_mot:
                        print(f"[Contrôleur] ERREUR: Mot ID {mot_id} non trouvé dans le modèle.")
                        messagebox.showerror("Erreur", f"Impossible de trouver les détails du mot avec l'ID: {mot_id}")
                        return
                else:
                    print(f"[Contrôleur] ERREUR: Méthode '{nom_methode_modele}' non trouvée dans mod_vocab.")
                    messagebox.showerror("Erreur Interne", f"Fonctionnalité de récupération des détails du mot manquante ('{nom_methode_modele}').")
                    return
            elif not edition:
                details_mot = None
            else:
                print("[Contrôleur] ERREUR: Tentative d'édition sans mot_id fourni.")
                messagebox.showerror("Erreur Interne", "ID du mot manquant pour l'édition.")
                return
            # 正确调用VueEditionMot
            vue_edition_instance = vue_edition.VueEditionMot(self.root, self, mot_initial=details_mot)
            print(f"[Contrôleur] VueEditionMot affichée pour {'édition' if edition else 'ajout'}.")
        except Exception as e:
            print(f"[Contrôleur] ERREUR lors de l'affichage de la vue d'édition de mot: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erreur", f"Impossible d'ouvrir la vue d'édition de mot:\n{e}")

    def afficher_vue_article(self, id_article):
        """Affiche la vue détaillée d'un article spécifique."""
        print(f"[Contrôleur] Affichage vue article ID: {id_article}")
        try:
            details = mod_articles.obtenir_details_article(id_article) # Assurez-vous que cette fonction existe
            if details:
                self.effacer_vue_actuelle()
                # Assurez-vous que vue_article.VueArticle existe et est importé
                self.vue_actuelle = vue_article.VueArticle(self.root, self, details)
                self.vue_actuelle.pack(expand=True, fill='both', padx=10, pady=10)
            else:
                messagebox.showerror("Erreur", f"Impossible de trouver les détails pour l'article ID {id_article}.", parent=self.root)
                self.afficher_vue_liste_articles() # Revenir à la liste si erreur
        except AttributeError:
             messagebox.showerror("Erreur Modèle", "La fonction 'obtenir_details_article' semble manquante dans le modèle articles.", parent=self.root)
             self.afficher_vue_liste_articles()
        except Exception as e:
             messagebox.showerror("Erreur", f"Erreur lors de l'affichage des détails de l'article:\n{e}", parent=self.root)
             self.afficher_vue_liste_articles()

    def afficher_vue_modification_article(self, id_article):
        """Affiche la vue permettant de modifier un article existant dans une Toplevel."""
        print(f"[Contrôleur] Affichage vue modification article ID: {id_article}")
        try:
            details_actuels = mod_articles.obtenir_details_article(id_article)
            if not details_actuels:
                messagebox.showerror("Erreur", f"Impossible de trouver l'article ID {id_article} pour le modifier.", parent=self.root)
                return

            # Créer une Toplevel pour l'édition
            edition_window = tk.Toplevel(self.root)
            edition_window.title(f"Modifier Article: {details_actuels.get('titre', '')[:30]}...")

            # --- Vous devrez créer cette vue d'édition ---
            try:
                import vues.vue_edition_article # Assurez-vous que ce fichier/classe existe
                vue_edition_instance = vues.vue_edition_article.VueEditionArticle(edition_window, self, details_actuels)
                # Cette vue aura des champs pré-remplis et un bouton "Sauvegarder" qui appellera self.sauvegarder_article
            except ImportError:
                 messagebox.showerror("Erreur Implémentation", "La vue d'édition d'article (vues.vue_edition_article) n'est pas encore créée.", parent=self.root)
                 edition_window.destroy() # Fermer la fenêtre vide
            except Exception as e:
                 messagebox.showerror("Erreur", f"Erreur lors de l'ouverture de la vue d'édition: {e}", parent=self.root)
                 edition_window.destroy()

        except AttributeError:
             messagebox.showerror("Erreur Modèle", "La fonction 'obtenir_details_article' semble manquante dans le modèle articles.", parent=self.root)
        except Exception as e:
             messagebox.showerror("Erreur", f"Erreur lors de la préparation de la modification:\n{e}", parent=self.root)

    def afficher_vue_importation_article(self):
        """Ouvre un dialogue pour choisir un fichier article et tente de l'importer."""
        print("[Contrôleur] Appel de afficher_vue_importation_article (via dialogue).")
        chemin_fichier = filedialog.askopenfilename(
            title="Choisir un fichier article à importer",
            filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")],
            parent=self.root
        )

        if not chemin_fichier:
            print("[Contrôleur] Importation annulée.")
            return

        print(f"[Contrôleur] Fichier sélectionné pour importation: {chemin_fichier}")
        try:
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                contenu = f.read()

            titre = os.path.basename(chemin_fichier)
            donnees_article = {
                'titre': titre,
                'contenu': contenu,
                'chemin': chemin_fichier
                # L'ID sera ajouté par le modèle si c'est un nouvel article
            }
            print(f"[Contrôleur] Article lu, titre='{titre}'. Tentative de sauvegarde.")
            # Appeler la méthode de sauvegarde qui gère ajout/modification
            self.sauvegarder_article(donnees_article)
            # Le rafraîchissement est appelé dans sauvegarder_article si succès

        except Exception as e:
            print(f"[Contrôleur] ERREUR lors de l'importation du fichier {chemin_fichier} - {e}")
            messagebox.showerror("Erreur d'Importation", f"Impossible de lire ou traiter le fichier:\n{e}", parent=self.root)

    # --- Méthodes Logique Apprentissage (Session Étude) ---

    def demarrer_session_etude(self, id_article=None):
        """Lance une session d'étude. Peut être filtrée par id_article."""
        print(f"[Contrôleur] Démarrage session étude (Article ID: {id_article})")
        try:
            self.cartes_urgentes = self.mod_vocab.obtenir_cartes_pour_etude(id_article=id_article, max_maitrise=99)
            self.cartes_revision = []
            if not self.cartes_urgentes:
                messagebox.showinfo("Session d'étude", "Aucune carte à étudier pour le moment.")
                print("[Contrôleur] Aucune carte trouvée pour la session d'étude.")
                return
            print(f"[Contrôleur] {len(self.cartes_urgentes)} cartes obtenues pour la session.")
            vue_etude = vue_app.VueApprentissage(self.root, self)
            self.afficher_vue(vue_etude)
            self.afficher_prochaine_carte()
            print("[Contrôleur] Affichage de VueApprentissage demandé.")
        except Exception as e:
            print(f"[Contrôleur] ERREUR lors du démarrage de la session d'étude: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erreur", f"Impossible de démarrer la session d'étude:\n{e}")

    def editer_mot_selectionne(self):
        """Ouvre la fenêtre d'édition pour le mot sélectionné dans la vue liste."""
        if hasattr(self.vue_actuelle, 'tree'):
            selection = self.vue_actuelle.tree.selection()
            if not selection:
                messagebox.showwarning("Sélection requise", "Veuillez sélectionner un mot à modifier.", parent=self.root)
                return
            mot_id = selection[0]
            self.afficher_vue_edition_mot(mot_id=mot_id, edition=True)

    def afficher_details_mot_par_id(self, mot_id):
        """Affiche une fenêtre de détails pour le mot donné (Toplevel)."""
        details = self.mod_vocab.obtenir_details_mot(mot_id)
        if details:
            import vues.vue_details_mot
            vues.vue_details_mot.VueDetailsMot(self.root, self, details)
        else:
            messagebox.showerror("Erreur", f"Impossible de trouver les détails pour le mot ID {mot_id}", parent=self.root)

    def choisir_prochaine_carte(self):
        """Choisit la prochaine carte selon la priorité (urgent d'abord)."""
        if self.cartes_urgentes:
            return self.cartes_urgentes.pop(0)
        elif self.cartes_revision:
            return self.cartes_revision.pop(0)
        else:
            return None

    def afficher_prochaine_carte(self):
        """Affiche la carte choisie dans la vue d'apprentissage."""
        prochaine_carte = self.choisir_prochaine_carte()
        nb_restantes = len(self.cartes_urgentes) + len(self.cartes_revision) + (1 if prochaine_carte else 0)
        if prochaine_carte is None:
            messagebox.showinfo("Session Terminée", "Félicitations ! Session d'étude terminée.", parent=self.root)
            self.retourner_a_liste_appropriee()
            return
        self.carte_actuelle_details = prochaine_carte
        id_mot, direction, _ = prochaine_carte
        try:
            self.details_mot_complets = mod_vocab.obtenir_details_mot(id_mot)
            if not self.details_mot_complets:
                print(f"ERREUR: Impossible d'obtenir les détails pour l'ID {id_mot}. Carte sautée.")
                self.afficher_prochaine_carte()
                return
        except AttributeError:
             messagebox.showerror("Erreur Modèle", "La fonction 'obtenir_details_mot' semble manquante.", parent=self.root)
             self.retourner_a_liste_appropriee()
             return
        except Exception as e:
             messagebox.showerror("Erreur", f"Erreur lors de la récupération des détails du mot:\n{e}", parent=self.root)
             self.retourner_a_liste_appropriee()
             return
        mot_en = self.details_mot_complets.get("mot_anglais", "")
        mot_fr = self.details_mot_complets.get("traduction_francais", "")
        mot_cn = self.details_mot_complets.get("traduction_chinois", "")
        prompt = ""
        self.reponse_correcte_actuelle = ""
        if direction == 'Eng->Fr':
            prompt = f"Français pour : {mot_en}"
            self.reponse_correcte_actuelle = mot_fr
        elif direction == 'Fr->Eng':
            prompt = f"Anglais pour : {mot_fr}"
            self.reponse_correcte_actuelle = mot_en
        elif direction == 'Eng->Ch':
             prompt = f"Chinois pour : {mot_en}"
             self.reponse_correcte_actuelle = mot_cn
        else:
             print(f"ERREUR: Direction d'apprentissage inconnue '{direction}'. Carte sautée.")
             self.afficher_prochaine_carte()
             return
        if isinstance(self.vue_actuelle, vue_app.VueApprentissage):
            self.vue_actuelle.afficher_carte(prompt, nb_restantes=nb_restantes)
        else:
             print("ERREUR: La vue actuelle n'est pas la vue d'apprentissage.")
             self.retourner_a_liste_appropriee()

    def verifier_reponse(self, reponse_utilisateur):
        """Vérifie la réponse, met à jour la maîtrise et affiche le feedback."""
        if not isinstance(self.vue_actuelle, vue_app.VueApprentissage) or self.carte_actuelle_details is None:
            print("ERREUR: Impossible de vérifier la réponse (vue ou carte non valide).")
            return
        id_mot, direction, _ = self.carte_actuelle_details
        reponse_norm = reponse_utilisateur.strip().lower()
        reponse_correcte_norm = self.reponse_correcte_actuelle.strip().lower()
        est_correct = (reponse_norm == reponse_correcte_norm)
        try:
            if est_correct:
                self.vue_actuelle.afficher_feedback(
                    "Correct !",
                    est_correct=True,
                    reponse_correcte=self.reponse_correcte_actuelle,
                    details_mot=self.details_mot_complets
                )
                mod_vocab.mettre_a_jour_maitrise(id_mot, direction, 'correct')
            else:
                msg = f"Incorrect.\nRéponse correcte : {self.reponse_correcte_actuelle}"
                self.vue_actuelle.afficher_feedback(
                    msg,
                    est_correct=False,
                    reponse_correcte=self.reponse_correcte_actuelle,
                    details_mot=self.details_mot_complets
                )
                mod_vocab.mettre_a_jour_maitrise(id_mot, direction, 'incorrect')
        except AttributeError:
             messagebox.showerror("Erreur Modèle", "La fonction 'mettre_a_jour_maitrise' semble manquante ou a changé d'arguments.", parent=self.root)
        except Exception as e:
             messagebox.showerror("Erreur", f"Erreur lors de la mise à jour de la maîtrise:\n{e}", parent=self.root)

    def montrer_reponse(self):
        """Affiche la réponse correcte et marque la carte comme incorrecte."""
        if not isinstance(self.vue_actuelle, vue_app.VueApprentissage) or self.carte_actuelle_details is None:
            print("ERREUR: Impossible de montrer la réponse (vue ou carte non valide).")
            return
        id_mot, direction, _ = self.carte_actuelle_details
        msg = f"Réponse : {self.reponse_correcte_actuelle}"
        self.vue_actuelle.afficher_feedback(
            msg,
            est_correct=False,
            reponse_correcte=self.reponse_correcte_actuelle,
            details_mot=self.details_mot_complets
        )
        try:
            mod_vocab.mettre_a_jour_maitrise(id_mot, direction, 'incorrect')
        except AttributeError:
             messagebox.showerror("Erreur Modèle", "La fonction 'mettre_a_jour_maitrise' semble manquante ou a changé d'arguments.", parent=self.root)
        except Exception as e:
             messagebox.showerror("Erreur", f"Erreur lors de la mise à jour de la maîtrise:\n{e}", parent=self.root)

    def marquer_comme_facile(self):
        """Marque la carte comme maîtrisée (100) et passe à la suivante."""
        if self.carte_actuelle_details:
            id_mot, direction, _ = self.carte_actuelle_details
            try:
                mod_vocab.mettre_a_jour_maitrise(id_mot, direction, 'facile') # Marquer comme facile
                self.afficher_prochaine_carte() # Passer à la suivante
            except AttributeError:
                 messagebox.showerror("Erreur Modèle", "La fonction 'mettre_a_jour_maitrise' semble manquante ou a changé d'arguments.", parent=self.root)
            except Exception as e:
                 messagebox.showerror("Erreur", f"Erreur lors du marquage comme facile:\n{e}", parent=self.root)
        else:
             print("ERREUR: Aucun détail de carte actuel pour marquer comme facile.")

    def sauter_carte(self):
        """Passe à la carte suivante sans affecter la maîtrise."""
        print("[Contrôleur] Carte sautée.")
        self.afficher_prochaine_carte()

    def retourner_a_liste_appropriee(self):
        """Retourne à la liste d'articles si une session était basée sur un article, sinon à la liste de mots."""
        if self.id_article_en_cours:
            self.afficher_vue_liste_articles()
        else:
            # Ou peut-être préférez-vous toujours retourner à la liste d'articles? Adaptez si besoin.
            self.afficher_vue_liste_mots()
        self.id_article_en_cours = None # Réinitialiser l'ID de l'article en cours

    def retourner_a_liste(self):
        """Retourne à la liste des mots appris."""
        self.afficher_vue_liste_mots()

    # --- Méthodes d'interaction avec le modèle Vocabulaire ---

    def obtenir_mots_appris (self): # Nom utilisé par la vue liste mots
        """Récupère la liste complète des mots du modèle vocabulaire."""
        print("[Contrôleur] Appel de get_mots_appris.")
        try:
            # Assurez-vous que mod_vocab.charger_mots existe
            return mod_vocab.charger_mots()
        except AttributeError:
            print("[Contrôleur] ERREUR: La fonction 'charger_mots' n'existe pas dans mod_vocab.")
            messagebox.showerror("Erreur Modèle", "Impossible de charger le vocabulaire (fonction manquante).", parent=self.root)
            return []
        except Exception as e:
            print(f"[Contrôleur] ERREUR inattendue dans get_mots_appris: {e}")
            messagebox.showerror("Erreur Chargement Mots", f"Une erreur est survenue:\n{e}", parent=self.root)
            return []

    def sauvegarder_mot(self, donnees_mot):
        """Demande au modèle vocabulaire de sauvegarder/modifier un mot."""
        print(f"[Contrôleur] Appel de sauvegarder_mot.")
        try:
            # Assurez-vous que mod_vocab.ajouter_ou_modifier_mot existe
            success = mod_vocab.ajouter_ou_modifier_mot(donnees_mot)
            if success:
                print("[Contrôleur] Mot sauvegardé avec succès via mod_vocab.")
                messagebox.showinfo("Succès", f"Mot '{donnees_mot.get('mot_anglais', 'Inconnu')}' sauvegardé.", parent=self.root) # Notifier l'utilisateur
                self.rafraichir_vue_liste_mots_si_active() # Rafraîchir la liste
                return True
            else:
                print("[Contrôleur] Échec de la sauvegarde du mot via mod_vocab.")
                messagebox.showerror("Échec Sauvegarde", "Le modèle n'a pas pu sauvegarder le mot.", parent=self.root)
                return False
        except AttributeError:
             print("[Contrôleur] ERREUR: La fonction 'ajouter_ou_modifier_mot' n'existe pas dans mod_vocab.")
             messagebox.showerror("Erreur Modèle", "Fonction de sauvegarde du mot manquante.", parent=self.root)
             return False
        except Exception as e:
            print(f"[Contrôleur] ERREUR inattendue dans sauvegarder_mot: {e}")
            messagebox.showerror("Erreur Sauvegarde Mot", f"Une erreur est survenue:\n{e}", parent=self.root)
            return False

    def supprimer_mot(self, id_mot):
        """Demande au modèle vocabulaire de supprimer un mot."""
        print(f"[Contrôleur] Demande de suppression pour mot ID: {id_mot}")
        if not messagebox.askyesno("Confirmation", f"Êtes-vous sûr de vouloir supprimer définitivement le mot ID\n{id_mot} ?", icon='warning', parent=self.root):
            print("[Contrôleur] Suppression du mot annulée.")
            return False
        try:
            success = mod_vocab.supprimer_mot(id_mot)
            if success:
                print("[Contrôleur] Mot supprimé avec succès via mod_vocab.")
                messagebox.showinfo("Succès", "Mot supprimé.", parent=self.root)
                self.afficher_vue_liste_mots()  # 立即刷新单词列表
                return True
            else:
                print("[Contrôleur] Échec de la suppression du mot via mod_vocab.")
                messagebox.showerror("Échec Suppression", "Le modèle n'a pas pu supprimer le mot.", parent=self.root)
                return False
        except AttributeError:
            print("[Contrôleur] ERREUR: La fonction 'supprimer_mot' n'existe pas dans mod_vocab.")
            messagebox.showerror("Erreur Modèle", "Fonction de suppression du mot manquante.", parent=self.root)
            return False
        except Exception as e:
            print(f"[Contrôleur] ERREUR inattendue dans supprimer_mot: {e}")
            messagebox.showerror("Erreur Suppression Mot", f"Une erreur est survenue:\n{e}", parent=self.root)
            return False

    # --- Méthodes d'interaction avec le modèle Articles ---

    def get_liste_articles(self):
        """Récupère la liste des articles (id, titre) du modèle articles."""
        print("[Contrôleur] Appel de get_liste_articles.")
        try:
            # Assurez-vous que mod_articles.obtenir_liste_articles existe et retourne le bon format
            # (typiquement une liste de dictionnaires [{'id': ..., 'titre': ...}])
            return mod_articles.obtenir_liste_articles()
        except AttributeError:
            print("[Contrôleur] ERREUR: La fonction 'obtenir_liste_articles' n'existe pas dans mod_articles.")
            messagebox.showerror("Erreur Modèle", "Impossible de lister les articles (fonction manquante).", parent=self.root)
            return []
        except Exception as e:
            print(f"[Contrôleur] ERREUR inattendue dans get_liste_articles: {e}")
            messagebox.showerror("Erreur Liste Articles", f"Une erreur est survenue:\n{e}", parent=self.root)
            return []

    def sauvegarder_article(self, donnees_article):
        """Demande au modèle articles de sauvegarder/modifier un article."""
        titre = donnees_article.get('titre', 'Sans titre')
        print(f"[Contrôleur] Appel de sauvegarder_article pour '{titre}'.")
        try:
            # Assurez-vous que mod_articles.ajouter_ou_modifier_article existe
            success = mod_articles.ajouter_ou_modifier_article(donnees_article)
            if success:
                print("[Contrôleur] Article sauvegardé avec succès via mod_articles.")
                messagebox.showinfo("Succès", f"Article '{titre}' sauvegardé.", parent=self.root)
                self.rafraichir_vue_liste_articles_si_active()
                # Si la sauvegarde vient d'une fenêtre d'édition Toplevel, on peut la fermer.
                # Cela nécessite de passer une référence à la fenêtre ou de la retrouver.
                return True
            else:
                print("[Contrôleur] Échec de la sauvegarde de l'article via mod_articles.")
                messagebox.showerror("Échec Sauvegarde", "Le modèle n'a pas pu sauvegarder l'article.", parent=self.root)
                return False
        except AttributeError:
             print("[Contrôleur] ERREUR: La fonction 'ajouter_ou_modifier_article' n'existe pas dans mod_articles.")
             messagebox.showerror("Erreur Modèle", "Fonction de sauvegarde de l'article manquante.", parent=self.root)
             return False
        except Exception as e:
            print(f"[Contrôleur] ERREUR inattendue dans sauvegarder_article: {e}")
            messagebox.showerror("Erreur Sauvegarde Article", f"Une erreur est survenue:\n{e}", parent=self.root)
            return False

    def supprimer_article(self, id_article):
        """Demande au modèle articles de supprimer un article."""
        print(f"[Contrôleur] Demande de suppression pour article ID: {id_article}")
        if not messagebox.askyesno("Confirmation", f"Êtes-vous sûr de vouloir supprimer définitivement l'article ID\n{id_article} ?", icon='warning', parent=self.root):
            print("[Contrôleur] Suppression de l'article annulée.")
            return False
        try:
            # 调用正确的模型方法
            success = mod_articles.supprimer_article(id_article)
            if success:
                print("[Contrôleur] Article supprimé avec succès via mod_articles.")
                messagebox.showinfo("Succès", "Article supprimé.", parent=self.root)
                self.rafraichir_vue_liste_articles_si_active()
                return True
            else:
                print("[Contrôleur] Échec de la suppression de l'article via mod_articles.")
                messagebox.showerror("Échec Suppression", "Le modèle n'a pas pu supprimer l'article.", parent=self.root)
                return False
        except AttributeError:
            print("[Contrôleur] ERREUR: La fonction 'supprimer_article' n'existe pas dans mod_articles.")
            messagebox.showerror("Erreur Modèle", "Fonction de suppression de l'article manquante.", parent=self.root)
            return False
        except Exception as e:
            print(f"[Contrôleur] ERREUR inattendue dans supprimer_article: {e}")
            messagebox.showerror("Erreur Suppression Article", f"Une erreur est survenue:\n{e}", parent=self.root)
            return False

    # --- Méthodes utilitaires de rafraîchissement ---

    def rafraichir_vue_liste_mots_si_active(self):
        """Vérifie si la vue actuelle est la liste des mots et la rafraîchit."""
        if self.vue_actuelle and isinstance(self.vue_actuelle, vue_liste_mots_appris.VueListeMotsAppris):
            print("[Contrôleur] Rafraîchissement de la vue liste des mots.")
            try:
                self.vue_actuelle.charger_liste_mots()
            except Exception as e:
                print(f"[Contrôleur] ERREUR lors du rafraîchissement de VueListeMotsAppris: {e}")
        else:
            print("[Contrôleur] La vue actuelle n'est pas la liste des mots, pas de rafraîchissement.")

    def rafraichir_vue_liste_articles_si_active(self):
        """Vérifie si la vue actuelle est la liste des articles et la rafraîchit."""
        # Utiliser la référence conservée self.vue_liste_articles_instance
        if self.vue_liste_articles_instance and isinstance(self.vue_actuelle, vue_liste_articles_vue.VueListeArticles):
            print("[Contrôleur] Rafraîchissement de la vue liste des articles.")
            try:
                # Appeler la méthode de chargement de l'instance conservée
                self.vue_liste_articles_instance.charger_liste_articles()
            except Exception as e:
                print(f"[Contrôleur] ERREUR lors du rafraîchissement de VueListeArticles: {e}")
        else:
             # Si la vue liste n'est pas active mais qu'on veut quand même la rafraichir la prochaine fois qu'elle s'affiche?
             # Pour l'instant, on ne fait rien si elle n'est pas active.
             print("[Contrôleur] La vue actuelle n'est pas la liste des articles (ou référence perdue), pas de rafraîchissement.")

    def afficher_vue(self, vue):
        """Affiche une nouvelle vue (Frame) dans la fenêtre principale."""
        if self.vue_actuelle:
            try:
                self.vue_actuelle.pack_forget()
                self.vue_actuelle.destroy()
            except Exception:
                pass
        self.vue_actuelle = vue
        self.vue_actuelle.pack(expand=True, fill='both', padx=10, pady=10)


# --- Fin de la classe Controleur ---

# Code pour démarrer l'application (typiquement dans le même fichier ou un fichier main.py)
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = Controleur(root)
#     root.mainloop()


# -*- coding: utf-8 -*-
# Dans vues/vue_liste_articles.py

import tkinter as tk
from tkinter import ttk, messagebox # Importer messagebox pour les confirmations et avertissements
import traceback

class VueListeArticles(ttk.Frame):
    """
    Vue qui affiche la liste des articles et permet les interactions
    (importer, ouvrir, modifier, supprimer).
    """
    def __init__(self, parent, controleur):
        """
        Initialise la vue de la liste des articles.

        Args:
            parent: Le widget parent (typiquement la fenêtre principale).
            controleur: L'instance du contrôleur principal.
        """
        print("[Vue Articles Init] --- Début Initialisation ---")
        super().__init__(parent)
        print("[Vue Articles Init] Appel de super().__init__() terminé.")

        self.controleur = controleur
        # Initialiser les attributs des widgets et la liste des IDs à None/vide
        self.listbox_articles = None
        self.btn_importer = None
        self.btn_ouvrir = None
        self.btn_modifier = None
        self.btn_supprimer = None
        self.scrollbar = None
        # Liste parallèle pour stocker les IDs complets dans le même ordre que le Listbox
        self.ids_articles_dans_listbox = []

        try:
            # --- Configuration du cadre principal ---
            print("[Vue Articles Init] Création du cadre principal...")
            cadre_principal = ttk.Frame(self, padding="10")
            cadre_principal.pack(expand=True, fill="both")

            # --- Cadre pour les boutons d'action ---
            print("[Vue Articles Init] Création du cadre des boutons...")
            cadre_boutons = ttk.Frame(cadre_principal)
            cadre_boutons.pack(side="top", fill="x", pady=(0, 10))

            # --- Création et placement des boutons ---
            print("[Vue Articles Init] Création bouton Importer...")
            self.btn_importer = ttk.Button(cadre_boutons, text="Importer", command=self.importer_article)
            self.btn_importer.pack(side="left", padx=5)

            print("[Vue Articles Init] Création bouton Ouvrir...")
            self.btn_ouvrir = ttk.Button(cadre_boutons, text="Ouvrir", command=self.ouvrir_article_selectionne)
            self.btn_ouvrir.pack(side="left", padx=5)

            print("[Vue Articles Init] Création bouton Modifier...")
            self.btn_modifier = ttk.Button(cadre_boutons, text="Modifier", command=self.modifier_article_selectionne)
            self.btn_modifier.pack(side="left", padx=5)

            print("[Vue Articles Init] Création bouton Supprimer...")
            self.btn_supprimer = ttk.Button(cadre_boutons, text="Supprimer", command=self.supprimer_article_selectionne)
            self.btn_supprimer.pack(side="left", padx=5) # Ou side="right" pour le mettre à l'autre bout

            # --- Création du Listbox et de sa Scrollbar ---
            print("[Vue Articles Init] Création du Listbox et Scrollbar...")
            cadre_liste = ttk.Frame(cadre_principal)
            cadre_liste.pack(side="top", fill="both", expand=True)

            self.listbox_articles = tk.Listbox(cadre_liste, selectmode=tk.SINGLE, height=15)
            self.scrollbar = ttk.Scrollbar(cadre_liste, orient=tk.VERTICAL, command=self.listbox_articles.yview)
            self.listbox_articles.configure(yscrollcommand=self.scrollbar.set)

            self.scrollbar.pack(side="right", fill="y")
            self.listbox_articles.pack(side="left", fill="both", expand=True)

            # --- Association de l'événement Double-Clic ---
            print("[Vue Articles Init] Association de l'événement Double-Clic...")
            # <Double-1> correspond au double-clic du bouton gauche de la souris
            self.listbox_articles.bind("<Double-1>", self.ouvrir_article_double_clic)

            # --- Chargement initial des données ---
            print("[Vue Articles Init] Appel de charger_liste_articles...")
            self.charger_liste_articles()

            print("[Vue Articles Init] --- Fin Initialisation (Bloc Try terminé avec succès) ---")

        except Exception as e:
             print(f"[Vue Articles Init] ERREUR FATALE DANS __INIT__: {e}")
             traceback.print_exc()

    def charger_liste_articles(self):
        """Charge ou recharge la liste des articles dans le Listbox."""
        print("[Vue Articles] --- Début charger_liste_articles ---")
        try:
            # Effacer le contenu précédent
            print("[Vue Articles] Effacement du contenu précédent du Listbox et de la liste d'IDs...")
            # Assurez-vous que le nom 'listbox_articles' correspond à votre widget Listbox
            self.listbox_articles.delete(0, tk.END)
            # Assurez-vous que le nom 'ids_articles_dans_listbox' correspond à votre liste d'IDs
            self.ids_articles_dans_listbox.clear()

            # Récupérer les articles depuis le contrôleur
            print("[Vue Articles] Récupération des articles depuis le contrôleur...")
            articles_recus = self.controleur.get_liste_articles() # Récupère [(id, titre), ...]
            print(f"[Vue Articles] Articles reçus: {articles_recus}")

            # Remplir le Listbox si des articles sont reçus
            if articles_recus:
                 # --- MODIFICATION PRINCIPALE ICI ---
                 # Nous traitons maintenant une liste de tuples (id, titre)
                for article_tuple in articles_recus:
                    # Vérifier si c'est bien un tuple avec 2 éléments
                    if isinstance(article_tuple, tuple) and len(article_tuple) == 2:
                        article_id = article_tuple[0]  # Le premier élément est l'ID (UUID)
                        titre = article_tuple[1]       # Le deuxième élément est le titre

                        # Vérifier qu'on a bien un ID et un titre non vides
                        if article_id and titre:
                            # Insérer SEULEMENT le titre dans le Listbox (ce que l'utilisateur voit)
                            self.listbox_articles.insert(tk.END, titre)
                            # Stocker l'ID (UUID) correspondant dans notre liste interne, dans le même ordre
                            self.ids_articles_dans_listbox.append(article_id)
                            # Optionnel: log pour déboguer
                            # print(f"[Vue Articles] Ajouté au listbox: '{titre}' (ID interne: {article_id})")
                        else:
                            print(f"[Vue Articles] AVERTISSEMENT: Tuple d'article incomplet ignoré: {article_tuple}")
                    else:
                        # Si le format n'est pas un tuple de 2 éléments, logguer un avertissement
                        print(f"[Vue Articles] AVERTISSEMENT: Format d'article inattendu (pas tuple de 2) ignoré: {article_tuple}")
            else:
                 print("[Vue Articles] Aucun article à afficher.")
                 # Optionnel : Afficher un message dans le listbox si vide
                 # self.listbox_articles.insert(tk.END, "Aucun article trouvé.")

        except AttributeError as e:
             # Si get_liste_articles n'existe pas dans le contrôleur
             print(f"[Vue Articles] ERREUR DANS charger_liste_articles (AttributeError): Contrôleur sans get_liste_articles? {e}")
             self.listbox_articles.insert(tk.END, "Erreur: Impossible de charger les articles (méthode contrôleur manquante).")
        except Exception as e:
             print(f"[Vue Articles] ERREUR INATTENDUE DANS charger_liste_articles: {e}")
             import traceback
             traceback.print_exc() # Imprime la trace complète pour le débogage
             self.listbox_articles.insert(tk.END, f"Erreur inattendue: {e}")

        print("[Vue Articles] --- Fin charger_liste_articles ---")
    
    def obtenir_id_article_selectionne(self):
        """
        Obtient l'ID complet de l'article actuellement sélectionné dans le Listbox
        en utilisant la liste parallèle `ids_articles_affiches`.

        Returns:
            str: L'ID complet de l'article sélectionné, ou None si rien n'est sélectionné
                 ou si l'index est invalide.
        """
        selection_indices = self.listbox_articles.curselection() # Renvoie un tuple d'indices (ex: (2,))
        if selection_indices:
            index_selectionne = selection_indices[0] # Prendre le premier index
            print(f"[Vue Articles] Index sélectionné dans le Listbox: {index_selectionne}")
            # Vérifier si l'index est valide pour notre liste d'IDs
            if 0 <= index_selectionne < len(self.ids_articles_dans_listbox):
                id_complet = self.ids_articles_dans_listbox[index_selectionne]
                print(f"[Vue Articles] ID complet correspondant trouvé: {id_complet}")
                return id_complet
            else:
                # Cela peut arriver si la liste d'IDs et le listbox sont désynchronisés (ne devrait pas arriver avec le code actuel)
                print(f"[Vue Articles] ERREUR: Index sélectionné ({index_selectionne}) hors limites pour la liste d'IDs (taille {len(self.ids_articles_affiches)}).")
                messagebox.showerror("Erreur Interne", "Erreur de synchronisation entre la liste affichée et les IDs.", parent=self)
                return None
        else:
            print("[Vue Articles] Aucun article sélectionné dans la liste.")
            return None

    def importer_article(self):
        """ Bouton 'Importer'. Demande au contrôleur d'afficher la vue d'importation. """
        print("Bouton 'Importer' cliqué.")
        if self.controleur:
             self.controleur.afficher_vue_importation_article()
        else:
            print("[Vue Articles] ERREUR: Contrôleur non défini.")

    def ouvrir_article_selectionne(self):
        """ Bouton 'Ouvrir'. Demande au contrôleur d'afficher les détails de l'article sélectionné. """
        print("Bouton 'Ouvrir' cliqué.")
        id_article = self.obtenir_id_article_selectionne()
        if id_article and self.controleur:
            print(f"[Vue Articles] Demande au contrôleur d'ouvrir l'article ID: {id_article}")
            self.controleur.afficher_vue_article(id_article)
        elif not id_article:
             messagebox.showwarning("Sélection Requise", "Veuillez sélectionner un article dans la liste pour l'ouvrir.", parent=self)

    def modifier_article_selectionne(self):
        """ Bouton 'Modifier'. Demande au contrôleur d'afficher la vue de modification pour l'article sélectionné. """
        print("Bouton 'Modifier' cliqué.")
        id_article = self.obtenir_id_article_selectionne()
        if id_article and self.controleur:
            print(f"[Vue Articles] Demande au contrôleur de modifier l'article ID: {id_article}")
            self.controleur.afficher_vue_modification_article(id_article)
        elif not id_article:
             messagebox.showwarning("Sélection Requise", "Veuillez sélectionner un article dans la liste pour le modifier.", parent=self)


    def supprimer_article_selectionne(self):
        """ Bouton 'Supprimer'. Demande confirmation puis demande au contrôleur de supprimer l'article sélectionné. """
        print("Bouton 'Supprimer' cliqué.")
        id_article = self.obtenir_id_article_selectionne()
        if id_article and self.controleur:
            titre_article = "cet article" # Valeur par défaut
            try:
                selection_indices = self.listbox_articles.curselection()
                if selection_indices:
                    index_selectionne = selection_indices[0]
                    texte_selectionne = self.listbox_articles.get(index_selectionne)
                    titre_article = texte_selectionne
            except Exception as e:
                print(f"[Vue Articles] Avertissement: Impossible d'extraire le titre pour le message de confirmation - {e}")

            confirmation = messagebox.askyesno(
                "Confirmation de Suppression",
                f"Êtes-vous sûr de vouloir supprimer l'article :\n'{titre_article}'?",
                icon='warning',
                parent=self)
            if confirmation:
                print(f"[Vue Articles] Confirmation reçue. Demande de suppression au contrôleur pour l'article ID: {id_article}")
                self.controleur.supprimer_article(id_article)
            else:
                print("[Vue Articles] Suppression annulée par l'utilisateur.")
        elif not id_article:
            messagebox.showwarning("Sélection Requise", "Veuillez sélectionner un article dans la liste pour le supprimer.", parent=self)

    def ouvrir_article_double_clic(self, event):
         """ Gère l'événement de double-clic sur un élément du Listbox. """
         print(f"Double-clic détecté sur le widget: {event.widget}")
         # Appelle la même logique que le bouton 'Ouvrir'
         self.ouvrir_article_selectionne()

    def ouvrir_article_double_clic(self, event):
         """ Gère l'événement de double-clic sur un élément du Listbox. """
         print(f"Double-clic détecté sur le widget: {event.widget}")
         # Appelle la même logique que le bouton 'Ouvrir'
         self.ouvrir_article_selectionne()


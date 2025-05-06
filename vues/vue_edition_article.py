# -*- coding: utf-8 -*-
# dans vues/vue_edition_article.py

import tkinter as tk
from tkinter import ttk, messagebox # Import messagebox pour les avertissements locaux
from tkinter import scrolledtext # Pour une zone de texte avec barre de défilement intégrée

class VueEditionArticle(ttk.Frame):
    def __init__(self, master, controleur, details_article):
        """
        Initialise la vue d'édition d'un article.

        :param master: Le widget parent (la fenêtre Toplevel).
        :param controleur: L'instance du contrôleur.
        :param details_article: Dictionnaire contenant les détails actuels de l'article
                                 (doit inclure 'id', 'titre', 'contenu').
        """
        super().__init__(master, padding="10")
        self.master = master # Garde une référence à la fenêtre Toplevel
        self.controleur = controleur
        # Crée une copie pour éviter de modifier l'original si l'utilisateur annule
        # self.donnees_edition = details_article.copy()
        # Ou travaille directement sur l'original si la logique de sauvegarde le gère
        self.details_article = details_article # Stocke le dict original pour accès à l'ID etc.

        # Configuration pour que le frame principal s'étende dans la Toplevel
        self.pack(expand=True, fill="both")
        master.geometry("600x400") # Taille initiale de la fenêtre d'édition
        master.minsize(400, 300) # Taille minimale

        # --- Widgets ---
        # Titre
        label_titre = ttk.Label(self, text="Titre:")
        # sticky='w' (west) pour aligner à gauche, 'nw' (north-west) pour haut-gauche
        label_titre.grid(row=0, column=0, sticky="nw", padx=5, pady=(0, 5))

        self.entry_titre = ttk.Entry(self, width=60)
        # sticky='ew' (east-west) pour s'étendre horizontalement
        self.entry_titre.grid(row=0, column=1, sticky="ew", padx=5, pady=(0, 5))
        # Pré-remplir le titre
        self.entry_titre.insert(0, self.details_article.get('titre', '')) # Utilise .get pour sécurité

        # Contenu
        label_contenu = ttk.Label(self, text="Contenu:")
        label_contenu.grid(row=1, column=0, sticky="nw", padx=5, pady=5)

        # Utiliser ScrolledText pour la facilité (intègre Text + Scrollbar)
        self.text_contenu = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=15, width=70)
        # sticky='nsew' pour s'étendre dans toutes les directions
        self.text_contenu.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        # Pré-remplir le contenu
        # 1.0 signifie "ligne 1, caractère 0", tk.END signifie "jusqu'à la fin"
        self.text_contenu.insert("1.0", self.details_article.get('contenu', '')) # Utilise .get

        # --- Boutons ---
        # Créer un frame pour contenir les boutons et les aligner à droite
        frame_boutons = ttk.Frame(self)
        # columnspan=2 pour occuper les deux colonnes, sticky='e' pour aligner à droite
        frame_boutons.grid(row=3, column=0, columnspan=2, sticky="e", pady=(10, 0))

        btn_sauvegarder = ttk.Button(frame_boutons, text="Sauvegarder", command=self.sauvegarder)
        btn_sauvegarder.pack(side="left", padx=5) # pack à l'intérieur du frame_boutons

        btn_annuler = ttk.Button(frame_boutons, text="Annuler", command=self.master.destroy) # Ferme la fenêtre
        btn_annuler.pack(side="left")

        # --- Configuration de l'expansion (pour redimensionnement) ---
        # Donne la priorité d'expansion à la colonne 1 (où sont l'Entry et le Text)
        self.columnconfigure(1, weight=1)
        # Donne la priorité d'expansion à la ligne 2 (où est le ScrolledText)
        self.rowconfigure(2, weight=1)

    def sauvegarder(self):
        """Récupère les données modifiées et demande la sauvegarde au contrôleur."""
        nouveau_titre = self.entry_titre.get().strip()
        nouveau_contenu = self.text_contenu.get("1.0", tk.END).strip()

        if not nouveau_titre:
             messagebox.showwarning("Champ Requis", "Le titre ne peut pas être vide.", parent=self.master)
             return

        # Préparer le dictionnaire de données à envoyer au contrôleur
        donnees_maj = {
            'id_article': self.details_article['id_article'], # Utilise l'ID de l'article original !
            'titre': nouveau_titre,
            'contenu': nouveau_contenu,
            'chemin': self.details_article.get('chemin', None)
        }

        print(f"[VueEditionArticle] Tentative de sauvegarde pour l'article ID {donnees_maj['id_article']}")
        if self.controleur.sauvegarder_article(donnees_maj):
            print("[VueEditionArticle] Sauvegarde réussie signalée par le contrôleur. Fermeture fenêtre.")
            self.master.destroy()
        else:
            print("[VueEditionArticle] Échec de la sauvegarde signalé par le contrôleur. Fenêtre reste ouverte.")

# --- Fin de la classe VueEditionArticle ---

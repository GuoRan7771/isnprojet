# vues/vue_importation_article.py
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import os

class VueImportationArticle(tk.Toplevel):
    def __init__(self, parent, controleur):
        super().__init__(parent)
        self.controleur = controleur
        self.title("Importer un Nouvel Article")
        self.geometry("600x500")
        self.transient(parent)
        self.grab_set()

        self.resultat = None # Pour savoir si l'import a réussi

        # --- Widgets ---
        frame_principal = ttk.Frame(self, padding="10")
        frame_principal.pack(expand=True, fill="both")

        # Titre
        ttk.Label(frame_principal, text="Titre de l'article:").grid(row=0, column=0, sticky="w", pady=(0,5))
        self.entry_titre = ttk.Entry(frame_principal, width=60)
        self.entry_titre.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0,10))

        # Contenu (Text widget)
        ttk.Label(frame_principal, text="Contenu de l'article:").grid(row=2, column=0, sticky="nw", pady=(0,5))
        self.text_contenu = scrolledtext.ScrolledText(frame_principal, width=70, height=15, wrap=tk.WORD)
        self.text_contenu.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(0,10))

        # --- Boutons ---
        frame_boutons = ttk.Frame(frame_principal)
        frame_boutons.grid(row=4, column=0, columnspan=2, pady=10)

        btn_charger_fichier = ttk.Button(frame_boutons, text="Charger depuis fichier (.txt)", command=self.charger_fichier)
        btn_charger_fichier.pack(side="left", padx=5)

        btn_sauvegarder = ttk.Button(frame_boutons, text="Sauvegarder Article", command=self.sauvegarder)
        btn_sauvegarder.pack(side="left", padx=5)

        btn_annuler = ttk.Button(frame_boutons, text="Annuler", command=self.destroy)
        btn_annuler.pack(side="left", padx=5)

        # --- Configuration Grid ---
        frame_principal.columnconfigure(0, weight=1) # Ajuster si besoin
        frame_principal.rowconfigure(3, weight=1) # Permettre au Text de s'étendre

        self.entry_titre.focus_set()
        self.wait_window(self)

    def charger_fichier(self):
        """Ouvre une boîte de dialogue pour choisir un fichier .txt et charge son contenu."""
        filepath = filedialog.askopenfilename(
            title="Ouvrir un fichier texte",
            filetypes=[("Fichiers Texte", "*.txt"), ("Tous les fichiers", "*.*")],
            parent=self # Important pour la modalité
        )
        if not filepath:
            return # Utilisateur a annulé

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                contenu = f.read()
            self.text_contenu.delete("1.0", tk.END) # Effacer contenu précédent
            self.text_contenu.insert("1.0", contenu)
             # Essayer de définir le titre à partir du nom de fichier (sans extension)
            nom_fichier = os.path.basename(filepath)
            titre_suggere, _ = os.path.splitext(nom_fichier)
            self.entry_titre.delete(0, tk.END)
            self.entry_titre.insert(0, titre_suggere)

        except Exception as e:
            messagebox.showerror("Erreur de lecture", f"Impossible de lire le fichier:\n{e}", parent=self)

    def sauvegarder(self):
        """Récupère titre et contenu et demande au contrôleur de sauvegarder."""
        titre = self.entry_titre.get().strip()
        contenu = self.text_contenu.get("1.0", tk.END).strip()

        if not titre:
            messagebox.showwarning("Champ manquant", "Le titre de l'article est obligatoire.", parent=self)
            return
        if not contenu:
             messagebox.showwarning("Champ manquant", "Le contenu de l'article ne peut pas être vide.", parent=self)
             return

        # Appeler le contrôleur
        self.resultat = self.controleur.sauvegarder_article(titre, contenu)

        if self.resultat: # Si sauvegarde réussie
            self.destroy() # Fermer la fenêtre


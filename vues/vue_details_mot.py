import tkinter as tk
from tkinter import ttk, messagebox

class VueDetailsMot(tk.Toplevel): # Utiliser Toplevel pour une fenêtre séparée (Utiliser Toplevel pour une fenêtre séparée)
    """Fenêtre affichant les détails d'un mot et ses phrases d'exemple (Interface 2).
    (Fenêtre affichant les détails d'un mot et ses phrases d'exemple (Interface 2).)
    """
    def __init__(self, parent, controleur, details_mot):
        super().__init__(parent)
        self.controleur = controleur
        self.details_mot = details_mot # Les données du mot passées par le contrôleur (Les données du mot passées par le contrôleur)

        mot_anglais = self.details_mot.get("mot_anglais", "N/A")
        self.title(f"Détails pour '{mot_anglais}'") # Titre de la fenêtre (Titre de la fenêtre)
        self.geometry("400x300") # Taille initiale (Taille initiale)

        # Afficher les informations de base (Afficher les informations de base)
        tk.Label(self, text=f"Mot: {mot_anglais}").pack(pady=5)
        tk.Label(self, text=f"Phonétique: {self.details_mot.get('phonetique', '')}").pack()
        tk.Label(self, text=f"Chinois: {self.details_mot.get('traduction_chinois', '')}").pack()
        tk.Label(self, text=f"Français: {self.details_mot.get('traduction_francais', '')}").pack()

        # Afficher les phrases d'exemple (Afficher les phrases d'exemple)
        tk.Label(self, text="\nPhrases d'exemple :").pack()
        frame_phrases = ttk.Frame(self)
        frame_phrases.pack(expand=True, fill='both', padx=10, pady=5)

        listbox_phrases = tk.Listbox(frame_phrases)
        listbox_phrases.pack(side=tk.LEFT, expand=True, fill='both')

        scrollbar = ttk.Scrollbar(frame_phrases, orient=tk.VERTICAL, command=listbox_phrases.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        listbox_phrases.config(yscrollcommand=scrollbar.set)

        exemples = self.details_mot.get("exemples", [])
        if exemples:
            for ex in exemples:
                # Stocker l'id_article avec la phrase si on veut implémenter le clic
                # (Stocker l'id_article avec la phrase si on veut implémenter le clic)
                phrase = ex.get("phrase", "Phrase non disponible")
                id_article = ex.get("id_article", None)
                listbox_phrases.insert(tk.END, phrase)
                # Ajouter un tag ou un moyen de retrouver l'id_article au clic si nécessaire
                # (Ajouter un tag ou un moyen de retrouver l'id_article au clic si nécessaire)
        else:
            listbox_phrases.insert(tk.END, "Aucune phrase d'exemple trouvée.") # Aucune phrase trouvée (Aucune phrase trouvée)

        # Lier le double-clic pour (éventuellement) sauter à l'article
        # (Lier le double-clic pour (éventuellement) sauter à l'article)
        listbox_phrases.bind("<Double-Button-1>", self.on_phrase_double_clic)

        # Rendre la fenêtre modale (optionnel) (Rendre la fenêtre modale (optionnel))
        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)

    def on_phrase_double_clic(self, event):
        """Gère le double-clic sur une phrase. Tente d'ouvrir l'article associé.
        (Gère le double-clic sur une phrase. Tente d'ouvrir l'article associé.)
        """
        widget = event.widget
        selection_index = widget.curselection()
        if selection_index:
            index = selection_index[0]
            exemples = self.details_mot.get("exemples", [])
            if index < len(exemples):
                id_article = exemples[index].get("id_article")
                if id_article:
                    print(f"Double-clic sur phrase, demande d'ouverture de l'article ID: {id_article}") # Débogage (Débogage)
                    # Demander au contrôleur d'ouvrir la vue de l'article
                    # (Demander au contrôleur d'ouvrir la vue de l'article)
                    self.controleur.afficher_article(id_article)
                    self.destroy() # Fermer la fenêtre de détails (Fermer la fenêtre de détails)
                else:
                    messagebox.showinfo("Info", "Aucun article associé à cette phrase.") # Pas d'article lié (Pas d'article lié)

# --- Note sur le Contrôleur ---
# Le contrôleur (`controleur.py`) doit avoir une méthode `afficher_details_mot(id_mot)`:
# 1. Appelle `mod_vocab.obtenir_details_mot(id_mot)` pour obtenir les données.
# 2. Crée une instance de `VueDetailsMot(parent, self, details)`.
#
# Et une méthode `afficher_article(id_article)`:
# 1. Appelle `mod_vocab.obtenir_texte_article(id_article)` (ou une fonction similaire).
# 2. Crée et affiche une nouvelle vue pour l'article.
# (Le contrôleur (`controleur.py`) doit avoir une méthode `afficher_details_mot(id_mot)`:
# 1. Appelle `mod_vocab.obtenir_details_mot(id_mot)` pour obtenir les données.
# 2. Crée une instance de `VueDetailsMot(parent, self, details)`.
#
# Et une méthode `afficher_article(id_article)`:
# 1. Appelle `mod_vocab.obtenir_texte_article(id_article)` (ou une fonction similaire).
# 2. Crée et affiche une nouvelle vue pour l'article.)


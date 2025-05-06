import tkinter as tk
from tkinter import ttk, scrolledtext

class VueArticle(ttk.Frame):
    def __init__(self, parent, controleur, details_article):
        super().__init__(parent)
        self.controleur = controleur
        self.details_article = details_article
        self.id_article = details_article.get("id_article") # Stocker l'ID

        # --- Cadre principal ---
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(expand=True, fill="both")

        # --- Titre de l'article ---
        titre = self.details_article.get('titre', 'Article sans titre')
        lbl_titre = ttk.Label(main_frame, text=titre, style="Titre.TLabel", anchor="center")
        lbl_titre.pack(fill="x", pady=(0, 10))

        # --- Contenu de l'article (lecture seule) ---
        self.text_contenu = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=20, state=tk.DISABLED) # tk.DISABLED pour lecture seule
        self.text_contenu.pack(expand=True, fill="both", pady=(0, 10))

        # Insérer le contenu
        contenu = self.details_article.get('contenu', 'Contenu non disponible.')
        self.text_contenu.configure(state=tk.NORMAL) # Activer pour insertion
        self.text_contenu.insert("1.0", contenu)
        self.text_contenu.configure(state=tk.DISABLED) # Désactiver après insertion

        # --- Boutons d'action ---
        frame_boutons = ttk.Frame(main_frame)
        frame_boutons.pack(fill="x")

        btn_retour = ttk.Button(frame_boutons, text="Retour à la liste des articles", command=self.retour_liste_articles)
        btn_retour.pack(side="left", padx=5)

        # Futurs boutons : "Lancer étude pour cet article", "Extraire mots", etc.
        # btn_etude_article = ttk.Button(frame_boutons, text="Étudier les mots de cet article", command=self.lancer_etude_article)
        # btn_etude_article.pack(side="left", padx=5)


    def retour_liste_articles(self):
        """Demande au contrôleur de revenir à la vue liste des articles."""
        self.controleur.afficher_vue_liste_articles()

    # def lancer_etude_article(self):
    #    """ Demande au contrôleur de lancer une session d'étude pour cet article spécifique. """
    #    if self.id_article:
    #        self.controleur.afficher_vue_apprentissage(id_article=self.id_article)


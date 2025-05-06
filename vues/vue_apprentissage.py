# vues/vue_apprentissage.py
import tkinter as tk
from tkinter import ttk

class VueApprentissage(tk.Frame):
    """Vue pour le mode d'apprentissage par cartes mémoire (Flashcards)."""
    def __init__(self, parent, controleur):
        super().__init__(parent)
        self.parent = parent
        self.controleur = controleur
        self.nb_cartes_restantes = 0
        # Cartes restantes标签，内容更鼓励
        self.lbl_nb_cartes = ttk.Label(self, text="")
        self.lbl_nb_cartes.pack(pady=(10, 0))

        # Configuration du style (peut être partagée au niveau de l'app)

        # --- Widgets ---

        # Étiquette pour afficher le mot/la question (Label for prompt word/question)
        self.lbl_prompt = ttk.Label(self, text="Chargement...", style="Prompt.TLabel", anchor=tk.CENTER)
        self.lbl_prompt.pack(pady=20, fill=tk.X)

        # Cadre pour la réponse et les accents (Frame for answer and accents)
        frame_reponse = ttk.Frame(self)
        frame_reponse.pack(pady=10)

        # Champ de saisie pour la réponse (Entry field for the answer)
        self.entry_reponse = ttk.Entry(frame_reponse, font=('Segoe UI', 14), width=40)
        self.entry_reponse.pack()
        # Lier la touche Entrée à la vérification (Bind Enter key to check)
        self.entry_reponse.bind("<Return>", self.on_check_click)

        # Cadre pour les boutons d'accent (Frame for accent buttons)
        frame_accents = ttk.Frame(self)
        frame_accents.pack(pady=5)

        # Boutons pour les caractères accentués français (Buttons for French accented characters)
        accents = ['é', 'à', 'ç', 'è', 'ù', 'â', 'ê', 'î', 'ô', 'û', 'ë', 'ï', 'ü', 'œ']
        for i, accent in enumerate(accents):
            btn = ttk.Button(frame_accents, text=accent, width=3, style="Accent.TButton",
                             command=lambda char=accent: self.inserer_accent(char))
            # Organiser en grille pour une meilleure disposition (Arrange in a grid for better layout)
            btn.grid(row=i // 8, column=i % 8, padx=2, pady=2)

        # Étiquette pour afficher le feedback (correct/incorrect/réponse)
        self.lbl_feedback = ttk.Label(self, text="", style="Feedback.TLabel", anchor=tk.CENTER, wraplength=400)
        self.lbl_feedback.pack(pady=10, fill=tk.X)

        # Cadre pour les boutons d'action (Frame for action buttons)
        frame_actions = ttk.Frame(self)
        frame_actions.pack(pady=20)

        # Boutons d'action
        self.btn_verifier = ttk.Button(frame_actions, text="Vérifier", style="Action.TButton", command=self.on_check_click)
        self.btn_verifier.grid(row=0, column=0, padx=5)

        self.btn_montrer = ttk.Button(frame_actions, text="Montrer Réponse", style="Action.TButton", command=self.on_show_answer_click)
        self.btn_montrer.grid(row=0, column=1, padx=5)

        self.btn_facile = ttk.Button(frame_actions, text="Très Facile", style="Action.TButton", command=self.on_easy_click)
        self.btn_facile.grid(row=1, column=0, padx=5, pady=5)

        # Note: "Sauter Carte" pourrait avoir plusieurs interprétations.
        self.btn_next_card = ttk.Button(frame_actions, text="Carte suivante", style="Action.TButton", command=self.on_skip_click)
        self.btn_next_card.grid(row=1, column=1, padx=5, pady=5)

        # Bouton pour quitter le mode apprentissage (Button to exit learning mode)
        self.btn_quitter = ttk.Button(self, text="Quitter Apprentissage", command=self.controleur.retourner_a_liste)
        self.btn_quitter.pack(pady=10, side=tk.BOTTOM)

        # Voir la fiche按钮，初始不显示，后续动态添加
        self.btn_voir_fiche = None
        self.frame_actions = frame_actions
        self.reponse_correcte = ""
        self.details_mot = None
        self._bind_verifier()
        self._bind_facile_global()

    def inserer_accent(self, caractere):
        """Insère un caractère accentué dans le champ de réponse."""
        self.entry_reponse.insert(tk.INSERT, caractere)
        self.entry_reponse.focus()

    def afficher_carte(self, prompt_text, nb_restantes=None):
        if nb_restantes is not None:
            self.nb_cartes_restantes = nb_restantes
        # 顶部鼓励语
        self.lbl_nb_cartes.config(text=f"💪 加油！Cartes restantes : {self.nb_cartes_restantes}")
        self.lbl_prompt.config(text=prompt_text)
        self.entry_reponse.config(state=tk.NORMAL, background="white")
        self.entry_reponse.delete(0, tk.END)
        self.lbl_feedback.config(text="")
        self.btn_verifier.config(state=tk.NORMAL)
        self.btn_montrer.config(state=tk.NORMAL)
        self._remove_voir_fiche()
        self._bind_verifier()
        self._bind_facile_global()
        self.entry_reponse.focus()

    def afficher_feedback(self, message, est_correct=None, reponse_correcte=None, details_mot=None):
        if est_correct is True:
            self.entry_reponse.config(background="#b6fcb6", state=tk.DISABLED)
            self.lbl_feedback.config(text=f"Bravo ! Bonne réponse : {reponse_correcte}", foreground="green")
        elif est_correct is False:
            self.entry_reponse.config(background="#fcb6b6", state=tk.DISABLED)
            self.lbl_feedback.config(text=message, foreground="red")
        else:
            self.lbl_feedback.config(text=message, foreground="black")
        self.btn_verifier.config(state=tk.DISABLED)
        self.btn_montrer.config(state=tk.DISABLED)
        self._add_voir_fiche(details_mot)
        self._bind_sauter()
        self._bind_facile_global()

    # --- Méthodes déclenchées par les boutons (appellent le contrôleur) ---
    # --- Methods triggered by buttons (call the controller) ---

    def on_check_click(self, event=None):
        """Appelé quand le bouton 'Vérifier' est cliqué ou Entrée est pressée."""
        reponse = self.entry_reponse.get()
        self.controleur.verifier_reponse(reponse)

    def on_show_answer_click(self):
        """Appelé quand le bouton 'Montrer Réponse' est cliqué."""
        self.controleur.montrer_reponse()

    def on_easy_click(self):
        """Appelé quand le bouton 'Très Facile' est cliqué."""
        self.controleur.marquer_comme_facile()

    def on_skip_click(self, event=None):
        """Appelé quand le bouton 'Sauter Carte' est cliqué."""
        self.controleur.sauter_carte()

    def _add_voir_fiche(self, details_mot):
        self._remove_voir_fiche()
        mot_anglais = details_mot.get('mot_anglais', '') if details_mot else ''
        texte_bouton = f"Afficher {mot_anglais}" if mot_anglais else "Afficher la fiche"
        self.btn_voir_fiche = ttk.Button(self.frame_actions, text=texte_bouton, style="Action.TButton", width=20, command=lambda: self._popup_fiche(details_mot))
        self.btn_voir_fiche.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        self.entry_reponse.bind('<Shift-Return>', lambda e: self._popup_fiche(details_mot))

    def _remove_voir_fiche(self):
        if self.btn_voir_fiche:
            self.btn_voir_fiche.destroy()
            self.btn_voir_fiche = None
        self.entry_reponse.unbind('<Shift-Return>')

    def _popup_fiche(self, details_mot):
        if not details_mot:
            return
        top = tk.Toplevel(self)
        top.title("Détail du mot")
        top.configure(bg="#ffffcc")
        top.geometry("400x300")
        tk.Label(top, text=f"Mot anglais : {details_mot.get('mot_anglais','')}", bg="#ffffcc", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(top, text=f"Français : {details_mot.get('traduction_francais','')}", bg="#ffffcc").pack(pady=5)
        tk.Label(top, text=f"Chinois : {details_mot.get('traduction_chinois','')}", bg="#ffffcc").pack(pady=5)
        exemples = details_mot.get('exemples', [])
        if exemples:
            tk.Label(top, text="Exemples :", bg="#ffffcc").pack()
            for ex in exemples:
                tk.Label(top, text=ex.get('phrase',''), bg="#ffffcc").pack()
        tk.Button(top, text="Fermer", command=top.destroy).pack(pady=10)

    def _bind_verifier(self):
        self.entry_reponse.unbind("<Return>")
        self.entry_reponse.bind("<Return>", self.on_check_click)

    def _bind_sauter(self):
        self.entry_reponse.unbind("<Return>")
        self.entry_reponse.bind("<Return>", self.on_skip_click)

    def _bind_facile_global(self):
        self.entry_reponse.unbind('<Control-Return>')
        self.entry_reponse.bind('<Control-Return>', lambda e: self.on_easy_click())


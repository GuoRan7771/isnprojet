# 开发时间 : 2025/5/2 3:56
# vues/vue_vocabulaire.py
import tkinter as tk
from tkinter import ttk, messagebox

# Utiliser VOTRE classe existante !
class VueListeMotsAppris(ttk.Frame):
    def __init__(self, parent, controleur):
        super().__init__(parent) # Correct : Initialiser le Frame parent
        self.controleur = controleur

        # --- Cadre principal (Pas besoin si la classe est déjà un Frame, on ajoute directement à self) ---
        # main_frame = ttk.Frame(self) # Supprimer cette ligne
        # main_frame.pack(expand=True, fill="both", padx=10, pady=10) # Supprimer cette ligne

        # --- Titre ---
        # Les widgets sont ajoutés à 'self' car la classe est un Frame
        lbl_titre = ttk.Label(self, text="Liste des Mots Appris", style="Titre.TLabel")
        lbl_titre.pack(pady=(10, 10), padx=10) # Ajouter padx

        # --- Boutons d'action ---
        # Mettre les boutons dans un Frame interne pour les aligner
        frame_boutons_haut = ttk.Frame(self)
        frame_boutons_haut.pack(fill="x", pady=(0, 5), padx=10) # Ajouter padx

        btn_ajouter = ttk.Button(frame_boutons_haut, text="Ajouter Mot", command=self.ajouter_nouveau_mot)
        btn_ajouter.pack(side="left", padx=(0, 5))

        # --- AJOUTER LES NOUVEAUX BOUTONS ---
        btn_modifier = ttk.Button(frame_boutons_haut, text="Modifier Mot", command=self.modifier_mot_selectionne) # Lier à une méthode locale qui appelle le contrôleur
        btn_modifier.pack(side="left", padx=5)

        btn_supprimer = ttk.Button(frame_boutons_haut, text="Supprimer Mot", command=self.supprimer_mot_selectionne) # Lier à une méthode locale qui appelle lecontrôleur
        btn_supprimer.pack(side="left", padx=5)
        # --- FIN DES AJOUTS ---

        btn_demarrer = ttk.Button(frame_boutons_haut, text="Démarrer Session Étude", command=self.demarrer_session)
        btn_demarrer.pack(side="left", padx=5) # Consistance avec padx

        # --- Treeview pour afficher les mots ---
        # Créer un Frame pour le Treeview et les scrollbars pour un meilleur contrôle
        frame_treeview = ttk.Frame(self)
        frame_treeview.pack(expand=True, fill="both", padx=10, pady=(0, 10)) # Remplacer main_frame par self

        colonnes = ("id", "anglais", "francais", "chinois", "maitrise")
        # Le parent du Treeview est maintenant frame_treeview
        self.tree = ttk.Treeview(frame_treeview, columns=colonnes, show="headings", selectmode="browse")

        # Définir les en-têtes (inchangé)
        self.tree.heading("id", text="ID")
        self.tree.heading("anglais", text="Anglais")
        self.tree.heading("francais", text="Français")
        self.tree.heading("chinois", text="Chinois")
        self.tree.heading("maitrise", text="Maîtrise")

        # Configurer les largeurs de colonnes (inchangé)
        self.tree.column("id", width=40, anchor=tk.CENTER)
        self.tree.column("anglais", width=150)
        self.tree.column("francais", width=150)
        self.tree.column("chinois", width=150)
        self.tree.column("maitrise", width=80, anchor=tk.CENTER)

        # Ajouter des barres de défilement
        # Le parent des scrollbars est aussi frame_treeview
        scrollbar_y = ttk.Scrollbar(frame_treeview, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(frame_treeview, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Placer Treeview et Scrollbars DANS frame_treeview
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True) # Le treeview remplit l'espace restant


        # --- Charger les données initiales (inchangé) ---
        self.charger_liste_mots()

        # --- Lier double-clic ---
        self.tree.bind("<Double-1>", self.on_double_click) # Assurez-vous que cette ligne est présente

    def charger_liste_mots(self):
        """Récupère les mots depuis le contrôleur et les affiche dans le Treeview."""
        print("[Vue Vocabulaire] --- Début charger_liste_mots ---")
        try:
            mots = self.controleur.obtenir_mots_appris()
            print(f"[Vue Vocabulaire] {len(mots)} mots reçus. Remplissage du Treeview...")
            if not mots:
                print("[Vue Vocabulaire] Aucun mot à afficher.")
            else:
                for index, mot_dict in enumerate(mots, start=1):
                    if isinstance(mot_dict, dict):
                        real_id = mot_dict.get("id_mot")
                        if not real_id:
                            print(f"[Vue Vocabulaire] AVERTISSEMENT: Mot sans ID ignoré: {mot_dict}")
                            continue
                        print(f"[Debug Charger] Préparation insertion - iid attendu: {real_id} (Type: {type(real_id)}), Index affiché: {index}")
                        # 计算平均maitrise
                        m1 = mot_dict.get("maitrise_eng_fr", 0)
                        m2 = mot_dict.get("maitrise_fr_eng", 0)
                        maitrise_moyenne = int((m1 + m2) / 2)
                        values_tuple = (
                            index,
                            mot_dict.get("mot_anglais", ""),
                            mot_dict.get("traduction_francais", ""),
                            mot_dict.get("traduction_chinois", ""),
                            maitrise_moyenne
                        )
                        try:
                            self.tree.insert(
                                "", tk.END,
                                iid=str(real_id),
                                values=values_tuple
                            )
                        except Exception as e:
                            print(f"[Debug Charger] ERREUR lors de l'insertion pour ID {real_id}: {e}")
                    else:
                        print(f"[Vue Vocabulaire] AVERTISSEMENT: Format de mot inattendu ignoré: {mot_dict}")
        except Exception as e:
            print(f"[Vue Vocabulaire] ERREUR INATTENDUE dans charger_liste_mots: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erreur Inattendue", f"Une erreur imprévue est survenue lors du chargement des mots:\n{e}")
        print("[Vue Vocabulaire] --- Fin charger_liste_mots ---")


    def demarrer_session(self):
        """Demande au contrôleur de démarrer la session d'étude."""
        print("Bouton 'Démarrer Session Étude' cliqué.")
        self.controleur.demarrer_session_etude() # Appeler la méthode correcte du contrôleur

    def ajouter_nouveau_mot(self):
        """Ouvre la fenêtre d'ajout de mot via le contrôleur."""
        print("Bouton 'Ajouter Mot' cliqué.")
        self.controleur.afficher_vue_edition_mot()  # 不传参数，表示新增

    # --- NOUVELLES METHODES INTERMEDIAIRES pour boutons ---
    # (Optionnel mais propre : méthodes locales qui appellent le contrôleur)
    def modifier_mot_selectionne(self):
        """Lance le processus de modification du mot sélectionné."""
        # Commentaire en chinois: 启动修改选中单词的流程。
        print("[Vue Vocabulaire] Bouton 'Modifier Mot' cliqué.")
        selection = self.tree.selection() # 获取选中项的 iid (内部 ID, 也就是 UUID)
        if not selection:
            messagebox.showwarning("Sélection Requise", "Veuillez sélectionner un mot à modifier.")
            return

        # 假设一次只修改一个单词
        mot_id_a_modifier = selection[0] # iid 就是 UUID
        print(f"[Vue Vocabulaire] Tentative de modification du mot avec ID (iid): {mot_id_a_modifier}")

        # 应该调用控制器的方法来显示编辑视图
        # 假设控制器中用于显示编辑视图的方法叫做 afficher_vue_edition_mot
        nom_methode_controleur = 'afficher_vue_edition_mot' # <- 确认你的控制器里是这个名字!

        if hasattr(self.controleur, nom_methode_controleur):
            # 调用控制器方法，传递单词 ID，并指明是编辑模式
            self.controleur.afficher_vue_edition_mot(mot_id=mot_id_a_modifier, edition=True)
            print(f"[Vue Vocabulaire] Demande au contrôleur d'afficher la vue d'édition pour le mot ID: {mot_id_a_modifier}")
        else:
            print(f"[Vue Vocabulaire] ERREUR: La méthode '{nom_methode_controleur}' n'existe pas dans le contrôleur!")
            messagebox.showerror("Erreur Interne", f"Impossible de trouver la fonction d'édition ('{nom_methode_controleur}') dans le contrôleur.")

    def supprimer_mot_selectionne(self):
        print("Bouton 'Supprimer Mot' cliqué.")
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner un mot à supprimer.", parent=self)
            return
        mot_id_a_supprimer = selection[0]  # Treeview的iid就是id_mot
        self.controleur.supprimer_mot(mot_id_a_supprimer)
    # ---

    # --- Méthodes pour obtenir l'ID et gérer double-clic (DEJA PRESENTES DANS VOTRE CODE) ---
    def get_id_mot_selectionne(self):
        """Retourne l'ID du mot actuellement sélectionné dans le Treeview."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner un mot dans la liste.", parent=self) # Ajouter parent=self
            return None
        item = self.tree.item(selection[0])
        try:
            mot_id = int(item['values'][0])
            return mot_id
        except (IndexError, ValueError, TypeError):
             messagebox.showerror("Erreur ID", "Impossible de récupérer l'ID du mot sélectionné.", parent=self) # Ajouter parent=self
             return None

    def on_double_click(self, event):
        """Gère le double-clic sur un mot pour afficher ses détails dans une nouvelle fenêtre."""
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            print("Double-clic détecté, affichage des détails du mot.")
            selection = self.tree.selection()
            if selection:
                mot_id = selection[0]
                self.controleur.afficher_details_mot_par_id(mot_id)
        else:
            print("Double-clic hors cellule.")

    # --- Méthodes afficher/masquer (si utilisées par le contrôleur) ---
    # Puisque la classe est un Frame, afficher/masquer agit sur self
    def afficher(self):
        # Utiliser pack (ou grid/place selon votre layout global)
        self.pack(expand=True, fill="both")
        print("VueListeMotsAppris affichée.")

    def masquer(self):
        self.pack_forget()
        print("VueListeMotsAppris masquée.")


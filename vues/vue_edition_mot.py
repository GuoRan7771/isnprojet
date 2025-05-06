# vues/vue_edition_mot.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

class VueEditionMot:
    # 修改 __init__ 接受初始数据
    def __init__(self, parent, controleur, mot_initial=None):
        self.top = tk.Toplevel(parent)
        # 根据是否有 mot_initial 设置标题
        self.top.title("Modifier Mot" if mot_initial else "Ajouter un Nouveau Mot")
        self.controleur = controleur
        # 存储正在编辑的单词ID，如果是新增则为 None
        self.id_mot_a_modifier = mot_initial.get("id_mot") if mot_initial else None

        # --- Widgets (标签和输入框) ---
        # ... (创建 Label 和 Entry 的代码基本不变) ...
        ttk.Label(self.top, text="Mot Anglais:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_anglais = ttk.Entry(self.top, width=40)
        self.entry_anglais.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.top, text="Traduction Français:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_francais = ttk.Entry(self.top, width=40)
        self.entry_francais.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.top, text="Traduction Chinois:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_chinois = ttk.Entry(self.top, width=40)
        self.entry_chinois.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.top, text="Exemples (un par ligne):").grid(row=3, column=0, padx=5, pady=5, sticky="nw")
        self.text_exemples = scrolledtext.ScrolledText(self.top, width=40, height=5)
        self.text_exemples.grid(row=3, column=1, padx=5, pady=5)

        # --- Remplir les champs si mot_initial est fourni ---
        if mot_initial:
            self.entry_anglais.insert(0, mot_initial.get("mot_anglais", ""))
            self.entry_francais.insert(0, mot_initial.get("traduction_francais", ""))
            self.entry_chinois.insert(0, mot_initial.get("traduction_chinois", ""))
            exemples_str = "\n".join([ex.get("phrase", "") for ex in mot_initial.get("exemples", [])])
            self.text_exemples.insert("1.0", exemples_str)


        # --- Boutons ---
        btn_sauvegarder = ttk.Button(self.top, text="Sauvegarder", command=self.sauvegarder)
        btn_sauvegarder.grid(row=4, column=0, columnspan=2, pady=10)

        # Centrer la fenêtre popup (optionnel)
        self.top.transient(parent)
        self.top.grab_set()
        # ... (code pour centrer la fenêtre si besoin) ...


    def recuperer_donnees(self):
        """Récupère les données saisies dans le formulaire."""
        donnees = {
            "mot_anglais": self.entry_anglais.get().strip(),
            "traduction_francais": self.entry_francais.get().strip(),
            "traduction_chinois": self.entry_chinois.get().strip(),
            # 处理例句，过滤空行
            "exemples": [
                {"phrase": ligne.strip()} # 暂时不处理例句ID，保存时再生成或更新
                for ligne in self.text_exemples.get("1.0", tk.END).strip().split("\n")
                if ligne.strip() # 只保留非空行
            ]
        }
        # Si on est en mode modification, ajouter l'ID existant aux données
        if self.id_mot_a_modifier is not None:
            donnees["id_mot"] = self.id_mot_a_modifier
            # 保留之前的熟练度，或者让 contrôleur 决定如何处理
            # donnees["niveau_maitrise"] = ??? # 可能需要从 mot_initial 获取

        return donnees

    # 修改 sauvegarder 方法
    def sauvegarder(self):
        """Appelle le contrôleur pour sauvegarder les données."""
        donnees_mot = self.recuperer_donnees()
        # 基础验证：至少需要英文单词
        if not donnees_mot["mot_anglais"]:
            messagebox.showerror("Erreur", "Le champ 'Mot Anglais' est obligatoire.", parent=self.top)
            return

        # Demander au contrôleur de gérer la sauvegarde (ajout ou modification)
        success = self.controleur.sauvegarder_mot(donnees_mot)

        if success:
            # Le contrôleur devrait afficher le message de succès approprié
            self.top.destroy() # Fermer la fenêtre d'édition/ajout
        # else:
            # Le contrôleur devrait avoir affiché un message d'erreur


# 开发时间 : 2025/5/2 3:37
import tkinter as tk
from tkinter import ttk
from controleur import Controleur

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Apprentissage de Langues")
    root.geometry("800x600") # Taille de fenêtre initiale

    try:
        style = ttk.Style(root)
        # Essayer différents thèmes: 'clam', 'alt', 'default', 'classic'
        # Sur Windows, 'vista' ou 'xpnative' peuvent aussi être disponibles

        available_themes = style.theme_names()
        print(f"Thèmes disponibles : {available_themes}") # Voir les thèmes disponibles (See available themes)
        if 'clam' in available_themes:
             style.theme_use('clam')
        elif 'vista' in available_themes: # Pour Windows (For Windows)
            style.theme_use('vista')
    except Exception as e:
        print(f"Erreur lors de la configuration du thème ttk : {e}")


    app = Controleur(root) # Lancer l'application via le contrôleur
    app.afficher_vue_liste_mots()
    root.mainloop()

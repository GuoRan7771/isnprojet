# 开发时间 : 2025/5/2 3:55
from modeles.gestion_donnees import GestionDonnees
import os
import random
import traceback
import time
import uuid

CHEMIN_FICHIER_VOCAB = "donnees/vocabulaire.json"
# CHEMIN_ARTICLES = "donnees/articles.json" # Garder pour référence future

# --- Fonctions existantes (charger, sauvegarder, obtenir_details_mot) ---
# Assurez-vous qu'elles sont présentes et fonctionnelles.
# (Make sure they are present and functional.)

def charger_tout_vocabulaire():
    """Charge tout le vocabulaire depuis le fichier JSON."""
    print("--- Début de charger_tout_vocabulaire ---")
    try:
        donnees = GestionDonnees.charger_donnees(CHEMIN_FICHIER_VOCAB)
        if not isinstance(donnees, list):
            print(f"AVERTISSEMENT: Le contenu de {CHEMIN_FICHIER_VOCAB} n'est pas une liste valide. Type réel: {type(donnees)}. Initialisation à [].")
            # Tentative de sauvegarde d'une liste vide pour réparer ?
            sauvegarder_tout_vocabulaire([])
            return []
        print(f"--- Fin de charger_tout_vocabulaire (Succès) ---")
        return donnees
    except FileNotFoundError:
        print(f"ERREUR CRITIQUE: Fichier non trouvé - {CHEMIN_FICHIER_VOCAB}")
        print(f"Création d'un fichier vide.")
        sauvegarder_tout_vocabulaire([]) # Crée le fichier avec une liste vide
        return []
    except Exception as e:
        print(f"ERREUR CRITIQUE dans charger_tout_vocabulaire: {e}")
        import traceback
        traceback.print_exc()
        print(f"--- Fin de charger_tout_vocabulaire (Échec Exception Générale) ---")
        # Ne pas retourner None, retourner une liste vide en cas d'erreur grave
        return []

def sauvegarder_tout_vocabulaire(vocabulaire):
    """Sauvegarde la liste complète du vocabulaire dans le fichier JSON."""
    if not isinstance(vocabulaire, list):
        print(f"ERREUR: Tentative de sauvegarde de données qui ne sont pas une liste dans {CHEMIN_FICHIER_VOCAB}. Type: {type(vocabulaire)}")
        return False
    print(f"--- Début sauvegarde vocabulaire ({len(vocabulaire)} mots) ---")
    try:
        # 调用 gestion.sauvegarder_donnees，这个调用本身应该是正确的
        success = GestionDonnees.sauvegarder_donnees(CHEMIN_FICHIER_VOCAB, vocabulaire)
        if success:
            # 仅在 gestion.sauvegarder_donnees 返回 True 时打印成功
            print("--- Fin sauvegarde vocabulaire (via gestion: Succès) ---")
            return True
        else:
            # 如果 gestion.sauvegarder_donnees 返回 False
            print("--- Fin sauvegarde vocabulaire (via gestion: ÉCHEC reporté) ---")
            return False # 将失败状态传递回去

    except Exception as e: # 这个 except 可能不会被触发了，因为错误在 gestion_donnees 内部处理
        # 为了保险起见，还是保留，并确保返回 False
        print(f"ERREUR CRITIQUE (niveau vocabulaire) lors de la sauvegarde dans {CHEMIN_FICHIER_VOCAB}: {e}")
        traceback.print_exc()
        return False # *** 明确返回 False ***

def obtenir_details_mot(id_mot):
    """Retourne les détails complets d'un mot spécifique par son ID."""
    print(f"--- Début de obtenir_details_mot (ID: {id_mot}) ---")
    vocabulaire_complet = charger_tout_vocabulaire() # 只加载一次数据

    # 检查加载的数据是否有效
    if not isinstance(vocabulaire_complet, list):
         print(f"ERREUR dans obtenir_details_mot: charger_tout_vocabulaire n'a pas retourné une liste.")
         print("--- Fin de obtenir_details_mot (Échec Chargement) ---")
         return None # 如果加载失败，直接返回 None

    # 使用 try...except 处理查找过程中可能发生的意外错误
    try:
        # 遍历词汇列表查找匹配的 ID
        for mot in vocabulaire_complet:
            # 确保 'mot' 是字典并且有 'id_mot' 键，然后比较 ID
            if isinstance(mot, dict) and mot.get("id_mot") == id_mot:
                print(f"Mot trouvé : {mot.get('mot_anglais', '[Mot sans nom]')}")
                print("--- Fin de obtenir_details_mot (Trouvé) ---")
                return mot # 找到后返回该词典

        # 如果循环正常结束但没有找到匹配项
        print(f"Mot avec ID {id_mot} non trouvé.")
        print("--- Fin de obtenir_details_mot (Non trouvé) ---")
        return None # 没有找到，返回 None

    except Exception as e:
        # 处理查找过程中可能发生的其他异常
        print(f"ERREUR inattendue lors de la recherche dans obtenir_details_mot: {e}")
        traceback.print_exc()
        print("--- Fin de obtenir_details_mot (Échec Recherche) ---")
        return None # 发生异常，返回 None

# --- MODIFICATION de mettre_a_jour_maitrise ---
def mettre_a_jour_maitrise(id_mot, direction, action):
    """Met à jour le niveau de maîtrise pour une direction donnée (Eng->Fr ou Fr->Eng)."""
    print(f"--- Début mise à jour maîtrise (ID: {id_mot}, Direction: {direction}, Action: {action}) ---")
    vocabulaire = charger_tout_vocabulaire()
    if not isinstance(vocabulaire, list):
        print("ERREUR: Impossible de charger le vocabulaire pour màj.")
        return False

    mot_trouve = False
    for i, mot in enumerate(vocabulaire):
        if isinstance(mot, dict) and str(mot.get("id_mot")) == str(id_mot):
            if direction == 'Eng->Fr':
                cle_maitrise = "maitrise_eng_fr"
            elif direction == 'Fr->Eng':
                cle_maitrise = "maitrise_fr_eng"
            else:
                print(f"ERREUR: Direction de maîtrise inconnue '{direction}'")
                return False
            maitrise_actuelle = mot.get(cle_maitrise, 0)
            if action == 'correct':
                if 0 <= maitrise_actuelle < 20: nouvelle_maitrise = 20
                elif 20 <= maitrise_actuelle < 40: nouvelle_maitrise = 40
                elif 40 <= maitrise_actuelle < 60: nouvelle_maitrise = 60
                elif 60 <= maitrise_actuelle < 80: nouvelle_maitrise = 80
                elif 80 <= maitrise_actuelle < 95: nouvelle_maitrise = 95
                elif 95 <= maitrise_actuelle < 100: nouvelle_maitrise = 100
                else: nouvelle_maitrise = 100
            elif action == 'incorrect':
                nouvelle_maitrise = 20
            elif action == 'facile':
                nouvelle_maitrise = 100
            else:
                print(f"ERREUR: Action de maîtrise inconnue '{action}'")
                return False
            nouvelle_maitrise = max(0, min(100, nouvelle_maitrise))
            vocabulaire[i][cle_maitrise] = nouvelle_maitrise
            mot_trouve = True
            break
    if not mot_trouve:
        print(f"ERREUR: Mot avec ID {id_mot} non trouvé pour màj.")
        return False
    sauvegarder_tout_vocabulaire(vocabulaire)
    print("--- Fin mise à jour maîtrise ---")
    return True


# --- MODIFICATION de obtenir_cartes_pour_etude ---
# Note: Pour l'instant, on ignore id_article, mais le paramètre est là pour le futur.
# (For now, we ignore id_article, but the parameter is there for the future.)
def obtenir_cartes_pour_etude(id_article=None, max_maitrise=99):
    """Génère une liste de cartes à étudier pour chaque mot (anglais->français, français->anglais), chaque carte a sa propre maîtrise."""
    print(f"--- Début obtenir_cartes (Article: {id_article}, Max Maîtrise: {max_maitrise}) ---")
    vocabulaire = charger_tout_vocabulaire()
    cartes = []
    if not isinstance(vocabulaire, list):
        print("ERREUR: Impossible de charger le vocabulaire pour générer les cartes.")
        return []

    for mot in vocabulaire:
        if not isinstance(mot, dict):
            continue
        id_mot = mot.get("id_mot")
        if not id_mot:
            continue
        # 英->法
        maitrise_eng_fr = mot.get("maitrise_eng_fr", 0)
        if maitrise_eng_fr <= max_maitrise:
            cartes.append((id_mot, 'Eng->Fr', maitrise_eng_fr))
        # 法->英
        maitrise_fr_eng = mot.get("maitrise_fr_eng", 0)
        if maitrise_fr_eng <= max_maitrise:
            cartes.append((id_mot, 'Fr->Eng', maitrise_fr_eng))
    print(f"Nombre total de cartes éligibles générées : {len(cartes)}")
    print("--- Fin obtenir_cartes ---")
    return cartes

# --- Fonction obtenir_mots_appris reste inchangée pour l'instant ---
def obtenir_mots_appris():
    print("--- Début de obtenir_mots_appris ---")
    vocabulaire_complet = charger_tout_vocabulaire()
    if not isinstance(vocabulaire_complet, list):
         print(f"ERREUR dans obtenir_mots_appris: charger_tout_vocabulaire n'a pas retourné une liste.")
         return []
    try:
        mots_appris = [mot for mot in vocabulaire_complet if isinstance(mot, dict) and mot.get("niveau_maitrise", 0) >= 0] # Afficher tous les mots pour l'instant
        print(f"Nombre de mots trouvés pour la liste : {len(mots_appris)}")
        print("--- Fin de obtenir_mots_appris ---")
        return mots_appris
    except Exception as e:
        print(f"ERREUR lors du filtrage dans obtenir_mots_appris: {e}")
        import traceback
        traceback.print_exc()
        return []

def obtenir_prochain_id_mot():
    """ Trouve le prochain ID de mot disponible. """
    vocabulaire = charger_tout_vocabulaire()
    if not vocabulaire: # Si la liste est vide ou None
        return 1
    # Trouve l'ID maximum actuel et ajoute 1
    max_id = 0
    for mot in vocabulaire:
        if isinstance(mot, dict):
             id_actuel = mot.get("id_mot", 0)
             if isinstance(id_actuel, int) and id_actuel > max_id:
                 max_id = id_actuel
    return max_id + 1

# --- NOUVELLE FONCTION pour ajouter un mot ---
def ajouter_mot(mot_anglais, trad_francais, trad_chinois, exemples_phrases):
    """Ajoute un nouveau mot au vocabulaire."""
    print(f"--- Début ajouter_mot ({mot_anglais}) ---")
    vocabulaire = charger_tout_vocabulaire()
    if not isinstance(vocabulaire, list):
        print("ERREUR: Impossible de charger le vocabulaire pour ajouter.")
        return False

    nouvel_id = generer_id_unique(vocabulaire)

    exemples_struct = []
    if exemples_phrases: # 检查是否有例句传入
        for phrase in exemples_phrases:
             # 确保只处理非空字符串
             if isinstance(phrase, str) and phrase.strip():
                 id_ex = generer_id_exemple_unique(exemples_struct)
                 exemples_struct.append({"id_exemple": id_ex, "phrase": phrase.strip()})
             elif isinstance(phrase, dict) and phrase.get("phrase","").strip(): # 如果传入的是字典
                  id_ex = phrase.get("id_exemple") or generer_id_exemple_unique(exemples_struct)
                  exemples_struct.append({"id_exemple": id_ex, "phrase": phrase["phrase"].strip()})


    nouveau_mot = {
        "id_mot": nouvel_id,
        "mot_anglais": mot_anglais,
        "traduction_francais": trad_francais,
        "traduction_chinois": trad_chinois,
        "niveau_maitrise": 0,  # Niveau initial
        "exemples": exemples_struct
    }
    vocabulaire.append(nouveau_mot)

    if sauvegarder_tout_vocabulaire(vocabulaire):
        print(f"Mot '{mot_anglais}' ajouté avec succès (ID: {nouvel_id}).")
        print("--- Fin ajouter_mot (Succès) ---")
        return True
    else:
        print(f"ERREUR: Échec de la sauvegarde après tentative d'ajout du mot '{mot_anglais}'.")
        # Tentative de rollback (recharger l'ancien état?) - complexe
        print("--- Fin ajouter_mot (Échec Sauvegarde) ---")
        return False


def generer_id_unique(vocabulaire):
    """Génère un ID unique pour un nouveau mot."""
    if not vocabulaire: # Si la liste est vide
        return 1
    # Obtient tous les IDs existants
    ids_existants = {mot.get("id_mot") for mot in vocabulaire if isinstance(mot, dict) and mot.get("id_mot") is not None}
    if not ids_existants: # Si aucun mot n'a d'ID valide
        return 1
    # Trouve le max ID existant et ajoute 1
    nouvel_id = max(ids_existants) + 1
    return nouvel_id

def generer_id_exemple_unique(exemples):
    """Génère un ID unique pour un nouvel exemple dans une liste d'exemples."""
    if not exemples:
        return 1
    ids_existants = {ex.get("id_exemple") for ex in exemples if isinstance(ex, dict) and ex.get("id_exemple") is not None}
    if not ids_existants:
        return 1
    return max(ids_existants) + 1

def modifier_mot(donnees_mot_modifie):
    """Modifie un mot existant dans le vocabulaire."""
    id_a_modifier = donnees_mot_modifie.get("id_mot")
    if id_a_modifier is None:
        print("ERREUR dans modifier_mot: ID manquant.")
        return False

    print(f"--- Début modifier_mot (ID: {id_a_modifier}) ---")
    vocabulaire = charger_tout_vocabulaire()
    if not isinstance(vocabulaire, list):
        print("ERREUR: Impossible de charger le vocabulaire pour modifier.")
        return False

    mot_trouve = False
    index_mot = -1
    for i, mot in enumerate(vocabulaire):
        if isinstance(mot, dict) and mot.get("id_mot") == id_a_modifier:
            mot_trouve = True
            index_mot = i
            break

    if not mot_trouve:
        print(f"ERREUR: Mot avec ID {id_a_modifier} non trouvé pour modification.")
        print("--- Fin modifier_mot (Non trouvé) ---")
        return False

    # Mettre à jour les champs du mot trouvé
    # Garder l'ancien niveau de maitrise si non fourni dans les nouvelles données
    niveau_maitrise_actuel = vocabulaire[index_mot].get("niveau_maitrise", 0)
    vocabulaire[index_mot]["mot_anglais"] = donnees_mot_modifie.get("mot_anglais", vocabulaire[index_mot].get("mot_anglais",""))
    vocabulaire[index_mot]["traduction_francais"] = donnees_mot_modifie.get("traduction_francais", vocabulaire[index_mot].get("traduction_francais",""))
    vocabulaire[index_mot]["traduction_chinois"] = donnees_mot_modifie.get("traduction_chinois", vocabulaire[index_mot].get("traduction_chinois",""))
    vocabulaire[index_mot]["niveau_maitrise"] = donnees_mot_modifie.get("niveau_maitrise", niveau_maitrise_actuel) # Conserve l'ancien niveau par défaut

    # Mettre à jour les exemples (remplacement complet basé sur les nouvelles données)
    nouveaux_exemples_struct = []
    exemples_entree = donnees_mot_modifie.get("exemples", [])
    if exemples_entree:
        for ex_data in exemples_entree:
             # Si l'exemple vient du formulaire, c'est un dict avec juste "phrase"
             if isinstance(ex_data, dict) and "phrase" in ex_data and ex_data["phrase"].strip():
                 id_ex = generer_id_exemple_unique(nouveaux_exemples_struct) # Génère un nouvel ID pour l'exemple
                 nouveaux_exemples_struct.append({"id_exemple": id_ex, "phrase": ex_data["phrase"].strip()})
             # Gérer d'autres formats si nécessaire

    vocabulaire[index_mot]["exemples"] = nouveaux_exemples_struct

    if sauvegarder_tout_vocabulaire(vocabulaire):
        print(f"Mot ID {id_a_modifier} modifié avec succès.")
        print("--- Fin modifier_mot (Succès) ---")
        return True
    else:
        print(f"ERREUR: Échec de la sauvegarde après tentative de modification du mot ID {id_a_modifier}.")
        print("--- Fin modifier_mot (Échec Sauvegarde) ---")
        return False

# --- 新增：删除单词 ---
def supprimer_mot(id_mot):
    """Supprime un mot du vocabulaire par son ID (str ou int)."""
    if id_mot is None:
        print("ERREUR dans supprimer_mot: ID manquant.")
        return False

    print(f"--- Début supprimer_mot (ID: {id_mot}) ---")
    vocabulaire = charger_tout_vocabulaire()
    if not isinstance(vocabulaire, list):
        print("ERREUR: Impossible de charger le vocabulaire pour supprimer.")
        return False

    taille_avant = len(vocabulaire)
    # 转为字符串比对
    vocabulaire_filtre = [mot for mot in vocabulaire if not (isinstance(mot, dict) and str(mot.get("id_mot")) == str(id_mot))]
    taille_apres = len(vocabulaire_filtre)

    if taille_avant == taille_apres:
        print(f"AVERTISSEMENT: Mot avec ID {id_mot} non trouvé pour suppression.")
        print("--- Fin supprimer_mot (Non trouvé) ---")
        return False

    if sauvegarder_tout_vocabulaire(vocabulaire_filtre):
        print(f"Mot ID {id_mot} supprimé avec succès.")
        print("--- Fin supprimer_mot (Succès) ---")
        return True
    else:
        print(f"ERREUR: Échec de la sauvegarde après tentative de suppression du mot ID {id_mot}.")
        print("--- Fin supprimer_mot (Échec Sauvegarde) ---")
        return False

def charger_mots():
    """Charge la liste complète des mots depuis le fichier."""
    print("[mod_vocab] Chargement des mots depuis:", CHEMIN_FICHIER_VOCAB)
    mots = GestionDonnees.charger_donnees(CHEMIN_FICHIER_VOCAB)
    # Assurez-vous que les données sont bien une liste de dictionnaires
    if not isinstance(mots, list):
        print(f"[mod_vocab] AVERTISSEMENT: Les données chargées ne sont pas une liste (type: {type(mots)}). Retourne une liste vide.")
        return []
    return mots

def ajouter_ou_modifier_mot(donnees_mot):
    """
    Ajoute un nouveau mot ou modifie un mot existant dans la source de données.
    :param donnees_mot: Un dictionnaire contenant les informations du mot.
                        Si 'id_mot' est présent et non None, c'est une modification.
                        Sinon, c'est un ajout.
    :return: True si l'opération a réussi, False sinon.
    """
    print(f"[mod_vocab] Tentative d'ajout/modification avec données: {donnees_mot}")
    try:
        mots = charger_mots() # Charger la liste actuelle des mots
        id_a_traiter = donnees_mot.get("id_mot") # Vérifier si un ID existe

        if id_a_traiter:
            # --- Modification ---
            mot_trouve = False
            for i, mot in enumerate(mots):
                if mot.get("id_mot") == id_a_traiter:
                    # Mettre à jour les champs du mot existant
                    # Attention: Ne pas écraser l'ID original
                    mots[i].update({k: v for k, v in donnees_mot.items() if k != "id_mot"})
                    # S'assurer que l'ID est bien dans le dict mis à jour au cas où update le supprimerait (peu probable)
                    mots[i]["id_mot"] = id_a_traiter
                    mot_trouve = True
                    print(f"[mod_vocab] Mot ID {id_a_traiter} mis à jour.")
                    break
            if not mot_trouve:
                print(f"[mod_vocab] ERREUR: Mot ID {id_a_traiter} non trouvé pour modification.")
                return False
        else:
            # --- Ajout ---
            # Générer un nouvel ID unique (par exemple, avec UUID)
            nouvel_id = str(uuid.uuid4())
            donnees_mot["id_mot"] = nouvel_id
             # Initialiser les compteurs de maîtrise si nécessaire
            donnees_mot.setdefault("maitrise_eng_fr", 0)
            donnees_mot.setdefault("maitrise_fr_eng", 0)
            donnees_mot.setdefault("maitrise_eng_ch", 0)
            # Ajouter d'autres maîtrises si besoin...
            mots.append(donnees_mot)
            print(f"[mod_vocab] Nouveau mot ajouté avec ID {nouvel_id}.")

        # Sauvegarder la liste mise à jour
        success = GestionDonnees.sauvegarder_donnees(CHEMIN_FICHIER_VOCAB, mots)
        if success:
            print("[mod_vocab] Liste de mots sauvegardée avec succès.")
            return True
        else:
            print("[mod_vocab] ERREUR lors de la sauvegarde de la liste de mots.")
            return False

    except Exception as e:
        print(f"[mod_vocab] ERREUR dans ajouter_ou_modifier_mot: {e}")
        import traceback
        traceback.print_exc() # Imprimer la trace pour le débogage
        return False
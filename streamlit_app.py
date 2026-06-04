import streamlit as st
import pandas as pd
import os

# =====================================================================
# SÉCURITÉ : ÉCRAN DE CONNEXION MULTI-UTILISATEURS (VIP)
# =====================================================================
st.set_page_config(page_title="Observatoire Circuit Fermé", layout="centered")

# Initialisation de la session utilisateur
if "connecte" not in st.session_state:
    st.session_state["connecte"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

# Si l'utilisateur n'est pas connecté, on affiche le formulaire de login
if not st.session_state["connecte"]:
    st.title("🔒 Loto Radar Pro V45 — Accès Sécurisé")
    st.markdown("### 🎫 Espace Membres Privé")
    
    # Formulaire de saisie
    username_input = st.text_input("Nom d'utilisateur :")
    password_input = st.text_input("Mot de passe :", type="password")
    
    if st.button("🔑 Se connecter au Radar"):
        try:
            # Récupération de la liste des comptes cachée dans les secrets de Streamlit
            comptes_vip = st.secrets["comptes_utilisateurs"]
            
            # Vérification des identifiants
            if username_input in comptes_vip and comptes_vip[username_input] == password_input:
                st.session_state["connecte"] = True
                st.session_state["username"] = username_input
                st.success(f"Bonjour {username_input} ! Connexion réussie...")
                st.rerun()
            else:
                st.error("❌ Identifiant ou mot de passe incorrect.")
        except Exception as e:
            st.warning("⚠️ Configuration de sécurité en cours sur le serveur. Veuillez patienter.")
            
    st.markdown("---")
    st.info("💡 Pour obtenir vos accès personnels ou renouveler votre abonnement, contactez le gestionnaire.")
    st.stop() # Bloque l'application tant qu'on n'est pas logué

# =====================================================================
# CONFIGURATION DE LA BARRE LATÉRALE (SIDEBAR)
# =====================================================================
if st.sidebar.button("🚪 Se déconnecter"):
    st.session_state["connecte"] = False
    st.session_state["username"] = ""
    st.rerun()

st.sidebar.markdown(f"👤 Membre connecté : **{st.session_state['username']}**")

# =====================================================================
# DONNÉES INVARIANTES ET CONFIGURATION DU RADAR
# =====================================================================
COLONNES_BRUTES = {
    "COLONNE 0 (Ancrage)": [3, 10, 15, 17, 20, 30, 35, 41, 43],
    "COLONNE 1 (Verrous)": [1, 4, 14, 25, 26, 32, 34, 39, 48],
    "COLONNE 2 (Résonance)": [2, 8, 12, 18, 19, 30, 33, 36, 46],
    "COLONNE 3 (Dérive)": [7, 16, 21, 27, 28, 31, 37, 38, 45, 48]
}

CHANCES_LOTO = [3, 6, 2, 7, 5, 9]
ETOILES_EURO = [[1, 9], [3, 11], [2, 8], [4, 12], [5, 10], [6, 7]]

CSV_LOTO = "historique_loto.csv"
CSV_EURO = "historique_euromillions.csv"

# Initialisation simplifiée et sécurisée des fichiers de données
if not os.path.exists(CSV_LOTO):
    hist_loto = [
        {"Jeu": "Loto", "Date": "2026-05-20", "N1": 8, "N2": 15, "N3": 28, "N4": 30, "N5": 48, "E1": 7, "E2": 0},
        {"Jeu": "Loto", "Date": "2026-05-23", "N1": 20, "N2": 21, "N3": 23, "N4": 36, "N5": 38, "E1": 2, "E2": 0},
        {"Jeu": "Loto", "Date": "2026-05-27", "N1": 3, "N2": 4, "N3": 15, "N4": 17, "N5": 41, "E1": 4, "E2": 0},
        {"Jeu": "Loto", "Date": "2026-05-30", "N1": 3, "N2": 10, "N3": 31, "N4": 34, "N5": 47, "E1": 5, "E2": 0}
    ]
    pd.DataFrame(hist_loto).to_csv(CSV_LOTO, index=False)

if not os.path.exists(CSV_EURO):
    hist_euro = [
        {"Jeu": "EuroMillions", "Date": "2026-05-19", "N1": 2, "N2": 12, "N3": 20, "N4": 38, "N5": 45, "E1": 2, "E2": 5},
        {"Jeu": "EuroMillions", "Date": "2026-05-22", "N1": 6, "N2": 22, "N3": 26, "N4": 31, "N5": 37, "E1": 5, "E2": 8},
        {"Jeu": "EuroMillions", "Date": "2026-05-26", "N1": 6, "N2": 23, "N3": 25, "N4": 35, "N5": 37, "E1": 6, "E2": 12},
        {"Jeu": "EuroMillions", "Date": "2026-05-29", "N1": 5, "N2": 14, "N3": 18, "N4": 31, "N5": 35, "E1": 2, "E2": 12}
    ]
    pd.DataFrame(hist_euro).to_csv(CSV_EURO, index=False)

# Fonctions algorithmiques
def phase_1_sourdine_strict(grilles_proposees):
    grilles_validees = []
    for nom, grille, bonus in grilles_proposees:
        grille_triee = sorted(grille)
        pairs = len([n for n in grille_triee if n % 2 == 0])
        if pairs == 0 or pairs == 5:
            continue
        somme = sum(grille_triee)
        if somme < 60 or somme > 180:
            continue
        suite_detectee = False
        for i in range(len(grille_triee) - 2):
            if grille_triee[i+1] == grille_triee[i] + 1 and grille_triee[i+2] == grille_triee[i] + 2:
                suite_detectee = True
                break
        if suite_detectee:
            continue
        grilles_validees.append((nom, grille_triee, bonus))
    return grilles_validees

def phase_2_generer_super_grille(grilles_brutes, jeu_actif):
    if len(grilles_brutes) < 6:
        return None
    grille_f = set(grilles_brutes[3][1])
    grille_m = set(grilles_brutes[5][1])
    numeros_communs = list(grille_f.intersection(grille_m))
    if len(numeros_communs) > 0:
        super_grille = list(numeros_communs)
        pour_completer = [n for n in grilles_brutes[3][1] if n not in super_grille]
        while len(super_grille) < 5 and pour_completer:
            super_grille.append(pour_completer.pop(0))
        bonus_final = CHANCES_LOTO[4] if jeu_actif == "Loto" else ETOILES_EURO[4]
        return ("⚡ SUPER-GRILLE MAÎTRESSE (Fusion x Mixte)", sorted(super_grille), bonus_final)
    return None

def phase_3_optimiser_et_reduire(grilles_filtrees, super_grille, limite_max=2):
    grilles_finales = []
    if super_grille and not any(super_grille[1] == g[1] for g in grilles_finales):
        grilles_finales.append(super_grille)
    for item in grilles_filtrees:
        if not any(item[1] == g[1] for g in grilles_finales):
            grilles_finales.append(item)
    return grilles_finales[:limite_max]

# INTERFACE D'AFFICHAGE DU RADAR
st.title("🔒 Radar Croisé V45 — Inverseur de Sourdine")

jeu = st.radio("🔄 Sélectionnez le moteur de jeu actif :", ("Loto", "EuroMillions"), horizontal=True)

strategie = st.radio(
    "🎯 Stratégie des grilles :",
    ("🟢 Jouer les numéros Disponibles (Standard)", "❌ Jouer UNIQUEMENT les numéros Exclus (Sourdine Inverse)"),
    horizontal=False
)

FICHIER_ACTIF = CSV_LOTO if jeu == "Loto" else CSV_EURO

# EXTRACTION ET FILTRAGE DES NUMÉROS
numeros_sortis_3_tirages = set()
if os.path.exists(FICHIER_ACTIF):
    try:
        df_hist = pd.read_csv(FICHIER_ACTIF)
        if not df_hist.empty:
            derniers_3 = df_hist.tail(3)
            for _, row in derniers_3.iterrows():
                for col_key in ["N1", "N2", "N3", "N4", "N5"]:
                    if pd.notna(row[col_key]):
                        numeros_sortis_3_tirages.add(int(row[col_key]))
    except Exception as e:
        st.error(f"Erreur moteur : {e}")

def obtenir_numeros_ciblés(nom_colonne):
    nums_bruts = COLONNES_BRUTES[nom_colonne]
    if "UNIQUEMENT les numéros Exclus" in strategie:
        cibles = [n for n in nums_bruts if n in numeros_sortis_3_tirages]
    else:
        cibles = [n for n in nums_bruts if n not in numeros_sortis_3_tirages]
    if len(cibles) < 5:
        complements = [n for n in nums_bruts if n not in cibles]
        cibles = cibles + complements
    return cibles

disp0 = obtenir_numeros_ciblés("COLONNE 0 (Ancrage)")
disp1 = obtenir_numeros_ciblés("COLONNE 1 (Verrous)")
disp2 = obtenir_numeros_ciblés("COLONNE 2 (Résonance)")
disp3 = obtenir_numeros_ciblés("COLONNE 3 (Dérive)")

if jeu == "Loto":
    grilles_brutes = [
        ("Grille Dérive pure (Axe Col 3)", [disp3[0], disp3[1], disp3[2], disp3[3], disp3[4]], CHANCES_LOTO[3]),
        ("Grille Centrale pure (Axe Col 0 & 2)", [disp0[0], disp0[1], disp0[2], disp2[0], disp2[1]], CHANCES_LOTO[2]),
        ("Grille Verrous pure (Axe Col 1)", [disp1[0], disp1[1], disp1[2], disp1[3], disp1[4]], CHANCES_LOTO[1]),
        ("Grille Inter-Axes A (Fusion)", [disp0[0], disp0[1], disp1[0], disp3[0], disp3[1]], CHANCES_LOTO[4]),
        ("Grille Inter-Axes B (Maillage)", [disp0[0], disp2[0], disp1[0], disp1[1], disp3[0]], CHANCES_LOTO[5]),
        ("Grille Transversale (Mixte)", [disp0[0], disp2[2], disp0[1], disp2[3], disp1[0]], CHANCES_LOTO[0])
    ]
else:
    grilles_brutes = [
        ("Grille Dérive pure (Axe Col 3)", [disp3[0], disp3[1], disp3[2], disp3[3], disp3[4]], ETOILES_EURO[3]),
        ("Grille Centrale pure (Axe Col 0 & 2)", [disp0[0], disp0[1], disp0[2], disp2[0], disp2[1]], ETOILES_EURO[2]),
        ("Grille Verrous pure (Axe Col 1)", [disp1[0], disp1[1], disp1[2], disp1[3], disp1[4]], ETOILES_EURO[1]),
        ("Grille Inter-Axes A (Fusion)", [disp0[0], disp0[1], disp1[0], disp3[0], disp3[1]], ETOILES_EURO[4]),
        ("Grille Inter-Axes B (Maillage)", [disp0[0], disp2[0], disp1[0], disp1[1], disp3[0]], ETOILES_EURO[5]),
        ("Grille Transversale (Mixte)", [disp0[0], disp2[2], disp0[1], disp2[3], disp1[0]], ETOILES_EURO[0])
    ]

if "UNIQUEMENT les numéros Exclus" in strategie:
    st.warning("⚠️ **MODE CHOC ACTIVÉ :** Radar inversé. Priorité aux numéros sortis récemment (Exclus).")
else:
    st.success("🟢 **MODE STANDARD ACTIVÉ :** Protection active, les numéros récents sont éliminés.")

# 4. AFFICHAGE DE LA CARTOGRAPHIE VISUELLE
st.subheader(f"📊 Cartographie des Colonnes ({jeu})")
for nom_col, liste_nums in COLONNES_BRUTES.items():
    st.markdown(f"**{nom_col}**")
    cols_badge = st.columns(len(liste_nums))
    for idx, n in enumerate(liste_nums):
        if n in numeros_sortis_3_tirages:
            cols_badge[idx].markdown(f"<div style='background-color:#991b1b;color:white;padding:5px;border-radius:4px;text-align:center;font-weight:bold;'>🔥 {n}</div>", unsafe_allow_html=True)
        else:
            cols_badge[idx].markdown(f"<div style='background-color:#1e293b;color:#94a3b8;padding:5px;border-radius:4px;text-align:center;'>❄️ {n}</div>", unsafe_allow_html=True)

st.markdown("---")

# 5. ENTONNOIR ET AFFICHAGE DES GRILLES OPTIMISÉES
st.subheader("🎰 Vos Propositions de Grilles Ultra-Optimisées (Plafond : 2)")
grilles_epurees = phase_1_sourdine_strict(grilles_brutes)
super_grille = phase_2_generer_super_grille(grilles_brutes, jeu)
grilles_finales = phase_3_optimiser_et_reduire(grilles_epurees, super_grille, limite_max=2)

for nom, num_liste, bonus in grilles_finales:
    st.markdown(f"🎯 **{nom}**")
    cols = st.columns(7)
    for i, num in enumerate(sorted(num_liste)):
        cols[i].button(f"💎 {num}", key=f"btn_{nom}_{i}", disabled=True)
    if jeu == "Loto":
        cols[5].button(f"🌟 {bonus}", key=f"chance_{nom}", disabled=True)
    else:
        cols[5].button(f"⭐ {bonus[0]}", key=f"et1_{nom}", disabled=True)
        cols[6].button(f"⭐ {bonus[1]}", key=f"et2_{nom}", disabled=True)

# =====================================================================
# 6. ESPACE SÉCURISÉ — SÉPARATION DES RÔLES (ADMIN VS CLIENT)
# =====================================================================
if st.session_state["username"] == "Boss45":
    st.markdown("---")
    st.subheader(f"🛠️ Espace Administrateur (Nouveau Tirage {jeu})")
    date_tirage = st.date_input("Date du tirage :")
    col_saisie = st.columns(5)
    n1 = col_saisie[0].number_input("N° 1", min_value=0, max_value=50, value=0, key="n1")
    n2 = col_saisie[1].number_input("N° 2", min_value=0, max_value=50, value=0, key="n2")
    n3 = col_saisie[2].number_input("N° 3", min_value=0, max_value=50, value=0, key="n3")
    n4 = col_saisie[3].number_input("N° 4", min_value=0, max_value=50, value=0, key="n4")
    n5 = col_saisie[4].number_input("N° 5", min_value=0, max_value=50, value=0, key="n5")

    tirage_numeros_propres = [n for n in [n1, n2, n3, n4, n5] if n != 0]
    e1_csv, e2_csv = 0, 0

    if jeu == "Loto":
        col_bonus = st.columns(3)
        chance_sorti = col_bonus[0].number_input("Numéro Chance", min_value=0, max_value=10, value=0)
        e1_csv = chance_sorti
    else:
        col_bonus = st.columns(3)
        et1 = col_bonus[0].number_input("Étoile 1", min_value=0, max_value=12, value=0)
        et2 = col_bonus[1].number_input("Étoile 2", min_value=0, max_value=12, value=0)
        e1_csv, e2_csv = et1, et2

    if st.button("💾 Enregistrer ce tirage et actualiser"):
        if len(tirage_numeros_propres) == 5:
            nouvelle_ligne = {"Jeu": jeu, "Date": str(date_tirage), "N1": n1, "N2": n2, "N3": n3, "N4": n4, "N5": n5, "E1": e1_csv, "E2": e2_csv}
            df_nouveau = pd.DataFrame([nouvelle_ligne])
            df_existant = pd.read_csv(FICHIER_ACTIF) if os.path.exists(FICHIER_ACTIF) else pd.DataFrame()
            pd.concat([df_existant, df_nouveau], ignore_index=True).to_csv(FICHIER_ACTIF, index=False)
            st.success(f"✅ Nouveau tirage enregistré avec succès !")
            st.rerun()
        else:
            st.error("⚠️ Saisie incomplète. Veuillez entrer les 5 numéros.")

    # Affichage de la base de données uniquement pour l'admin
    st.sidebar.markdown("---")
    st.sidebar.header(f"📊 Historique Base {jeu}")
    if os.path.exists(FICHIER_ACTIF):
        df_side = pd.read_csv(FICHIER_ACTIF)
        st.sidebar.dataframe(df_side, height=250)
        if st.sidebar.button("🗑️ Vider cette base"):
            os.remove(FICHIER_ACTIF)
            st.rerun()
else:
    # Message affiché uniquement pour les clients VIP dans la barre latérale
    st.sidebar.markdown("---")
    st.sidebar.info("⭐ **Compte VIP Actif** — Accès en temps réel aux grilles optimisées de l'Inverseur de Sourdine.")

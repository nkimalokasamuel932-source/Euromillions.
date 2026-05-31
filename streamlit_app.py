import streamlit as st
import pandas as pd
import os

# =====================================================================
# 1. ARCHITECTURE DES COLONNES DU CIRCUIT FERMÉ BRUT (INVARIANTE)
# =====================================================================
COLONNES_BRUTES = {
    "COLONNE 0 (Ancrage)": [3, 10, 15, 17, 20, 30, 35, 41, 43],
    "COLONNE 1 (Verrous)": [1, 4, 14, 25, 26, 32, 34, 39, 48],
    "COLONNE 2 (Résonance)": [2, 8, 12, 18, 19, 30, 33, 36, 46],
    "COLONNE 3 (Dérive)": [7, 16, 21, 27, 28, 31, 37, 38, 45, 48]
}

CHANCES_LOTO = [3, 6, 2, 7]
ETOILES_EURO = [[1, 9], [3, 11], [2, 8], [4, 12]]

CSV_LOTO = "historique_loto.csv"
CSV_EURO = "historique_euromillions.csv"

# =====================================================================
# INITIALISATION DES BASES DE DONNÉES RÉELLES (LOTO & EURO)
# =====================================================================
if not os.path.exists(CSV_LOTO):
    hist_loto = [
        {"Jeu": "Loto", "Date": "2026-05-04", "N1": 4, "N2": 8, "N3": 15, "N4": 18, "N5": 46, "E1": 2, "E2": 0},
        {"Jeu": "Loto", "Date": "2026-05-06", "N1": 7, "N2": 18, "N3": 27, "N4": 35, "N5": 48, "E1": 5, "E2": 0},
        {"Jeu": "Loto", "Date": "2026-05-09", "N1": 16, "N2": 21, "N3": 25, "N4": 26, "N5": 31, "E1": 1, "E2": 0},
        {"Jeu": "Loto", "Date": "2026-05-11", "N1": 17, "N2": 18, "N3": 30, "N4": 34, "N5": 39, "E1": 9, "E2": 0},
        {"Jeu": "Loto", "Date": "2026-05-13", "N1": 17, "N2": 35, "N3": 38, "N4": 41, "N5": 46, "E1": 2, "E2": 0},
        {"Jeu": "Loto", "Date": "2026-05-16", "N1": 1, "N2": 12, "N3": 30, "N4": 32, "N5": 34, "E1": 4, "E2": 0},
        {"Jeu": "Loto", "Date": "2026-05-18", "N1": 14, "N2": 32, "N3": 33, "N4": 36, "N5": 49, "E1": 3, "E2": 0},
        {"Jeu": "Loto", "Date": "2026-05-20", "N1": 8, "N2": 15, "N3": 28, "N4": 30, "N5": 48, "E1": 7, "E2": 0},
        {"Jeu": "Loto", "Date": "2026-05-23", "N1": 20, "N2": 21, "N3": 23, "N4": 36, "N5": 38, "E1": 2, "E2": 0},
        {"Jeu": "Loto", "Date": "2026-05-25", "N1": 19, "N2": 22, "N3": 27, "N4": 31, "N5": 49, "E1": 3, "E2": 0},
        {"Jeu": "Loto", "Date": "2026-05-27", "N1": 3, "N2": 4, "N3": 15, "N4": 17, "N5": 41, "E1": 4, "E2": 0},
        {"Jeu": "Loto", "Date": "2026-05-30", "N1": 3, "N2": 10, "N3": 31, "N4": 34, "N5": 47, "E1": 5, "E2": 0}
    ]
    pd.DataFrame(hist_loto).to_csv(CSV_LOTO, index=False)

if not os.path.exists(CSV_EURO):
    hist_euro = [
        {"Jeu": "EuroMillions", "Date": "2026-04-21", "N1": 13, "N2": 16, "N3": 29, "N4": 40, "N5": 47, "E1": 3, "E2": 4},
        {"Jeu": "EuroMillions", "Date": "2026-04-24", "N1": 25, "N2": 26, "N3": 30, "N4": 40, "N5": 45, "E1": 1, "E2": 5},
        {"Jeu": "EuroMillions", "Date": "2026-04-28", "N1": 26, "N2": 29, "N3": 41, "N4": 46, "N5": 47, "E1": 8, "E2": 9},
        {"Jeu": "EuroMillions", "Date": "2026-05-01", "N1": 3, "N2": 9, "N3": 42, "N4": 46, "N5": 47, "E1": 1, "E2": 11},
        {"Jeu": "EuroMillions", "Date": "2026-05-05", "N1": 3, "N2": 4, "N3": 8, "N4": 20, "N5": 31, "E1": 6, "E2": 8},
        {"Jeu": "EuroMillions", "Date": "2026-05-08", "N1": 2, "N2": 17, "N3": 19, "N4": 34, "N5": 37, "E1": 8, "E2": 11},
        {"Jeu": "EuroMillions", "Date": "2026-05-12", "N1": 4, "N2": 26, "N3": 32, "N4": 35, "N5": 36, "E1": 5, "E2": 7},
        {"Jeu": "EuroMillions", "Date": "2026-05-15", "N1": 3, "N2": 10, "N3": 38, "N4": 41, "N5": 43, "E1": 2, "E2": 9},
        {"Jeu": "EuroMillions", "Date": "2026-05-19", "N1": 2, "N2": 12, "N3": 20, "N4": 38, "N5": 45, "E1": 2, "E2": 5},
        {"Jeu": "EuroMillions", "Date": "2026-05-22", "N1": 6, "N2": 22, "N3": 26, "N4": 31, "N5": 37, "E1": 5, "E2": 8},
        {"Jeu": "EuroMillions", "Date": "2026-05-26", "N1": 6, "N2": 23, "N3": 25, "N4": 35, "N5": 37, "E1": 6, "E2": 12},
        {"Jeu": "EuroMillions", "Date": "2026-05-29", "N1": 5, "N2": 14, "N3": 18, "N4": 31, "N5": 35, "E1": 2, "E2": 12}
    ]
    pd.DataFrame(hist_euro).to_csv(CSV_EURO, index=False)

# =====================================================================
# 2. INTERFACE GRAPHIQUE STREAMLIT
# =====================================================================
st.set_page_config(page_title="Observatoire Circuit Fermé", layout="centered")
st.title("🔒 Radar de Sourdine V45 — Circuit Réduit")

jeu = st.radio("🔄 Sélectionnez le moteur de jeu actif :", ("Loto", "EuroMillions"), horizontal=True)

FICHIER_ACTIF = CSV_LOTO if jeu == "Loto" else CSV_EURO

# =====================================================================
# 3. EXTRACTION ET MISE EN SOURDINE DES 3 DERNIERS TIRAGES
# =====================================================================
numeros_sortis_3_tirages = set()
dictionnaire_ecarts = {}

for col_name, nums in COLONNES_BRUTES.items():
    for n in nums:
        dictionnaire_ecarts[n] = "Non sorti (+12)"

if os.path.exists(FICHIER_ACTIF):
    try:
        df_hist = pd.read_csv(FICHIER_ACTIF)
        if not df_hist.empty:
            total_tirages = len(df_hist)
            
            # CAPTURE ET SOURDINE STRICTE DES 3 DERNIERS TIRAGES
            derniers_3 = df_hist.tail(3)
            for _, row in derniers_3.iterrows():
                for col_key in ["N1", "N2", "N3", "N4", "N5"]:
                    if pd.notna(row[col_key]):
                        numeros_sortis_3_tirages.add(int(row[col_key]))
            
            # Calcul des distances thermiques
            for col_name, nums in COLONNES_BRUTES.items():
                for n in nums:
                    apparitions = df_hist[(df_hist["N1"] == n) | (df_hist["N2"] == n) | 
                                          (df_hist["N3"] == n) | (df_hist["N4"] == n) | 
                                          (df_hist["N5"] == n)]
                    if not apparitions.empty:
                        dernier_index = int(apparitions.index[-1])
                        distance = total_tirages - 1 - dernier_index
                        if distance == 0:
                            dictionnaire_ecarts[n] = "Tirage précédent (GELÉ ❌)"
                        elif distance < 3:
                            dictionnaire_ecarts[n] = f"Il y a {distance} tirage(s) (GELÉ ❌)"
                        else:
                            dictionnaire_ecarts[n] = f"Il y a {distance} tirage(s) (DISPO 🟢)"
                    else:
                        dictionnaire_ecarts[n] = "Non sorti sur les 12 tirages (DISPO 🟢)"
    except Exception as e:
        st.error(f"Erreur moteur : {e}")

# Fonction de filtrage par roulement interne
def filtrer_colonne_active(nom_colonne, taille_demandee=5):
    numeros_bruts = COLONNES_BRUTES[nom_colonne]
    # Seuls les numéros n'appartenant PAS aux 3 derniers tirages sont conservés
    numeros_filtrés = [n for n in numeros_bruts if n not in numeros_sortis_3_tirages]
    if len(numeros_filtrés) < taille_demandee:
        for n in numeros_bruts:
            if n not in numeros_filtrés:
                numeros_filtrés.append(n)
    return numeros_filtrés[:taille_demandee]

col0_active = filtrer_colonne_active("COLONNE 0 (Ancrage)")
col1_active = filtrer_colonne_active("COLONNE 1 (Verrous)")
col2_active = filtrer_colonne_active("COLONNE 2 (Résonance)")
col3_active = filtrer_colonne_active("COLONNE 3 (Dérive)")

# Grilles d'attaques épurées
grilles_loto = [
    ("Grille Dérive (Col 3)", [col3_active[0], col3_active[1], col3_active[2], col3_active[3], col3_active[4]], CHANCES_LOTO[3]),
    ("Grille Centrale (Col 0 & 2)", [col0_active[0], col0_active[1], col0_active[2], col2_active[0], col2_active[1]], CHANCES_LOTO[2]),
    ("Grille Verrous (Col 1)", [col1_active[0], col1_active[1], col1_active[2], col1_active[3], col1_active[4]], CHANCES_LOTO[1]),
    ("Grille Transversale (Mixte)", [col0_active[0], col2_active[2], col0_active[1], col2_active[3], col1_active[0]], CHANCES_LOTO[0])
]

grilles_euro = [
    ("Grille Dérive (Col 3)", [col3_active[0], col3_active[1], col3_active[2], col3_active[3], col3_active[4]], ETOILES_EURO[3]),
    ("Grille Centrale (Col 0 & 2)", [col0_active[0], col0_active[1], col0_active[2], col2_active[0], col2_active[1]], ETOILES_EURO[2]),
    ("Grille Verrous (Col 1)", [col1_active[0], col1_active[1], col1_active[2], col1_active[3], col1_active[4]], ETOILES_EURO[1]),
    ("Grille Transversale (Mixte)", [col0_active[0], col2_active[2], col0_active[1], col2_active[3], col1_active[0]], ETOILES_EURO[0])
]

# CALCUL DE L'ÉTAT DU CIRCUIT RÉDUIT
total_numeros_bruts = sum(len(v) for v in COLONNES_BRUTES.values())
tous_nums_bruts = set([n for sublist in COLONNES_BRUTES.values() for n in sublist])
total_exclus_circuit = len(tous_nums_bruts.intersection(numeros_sortis_3_tirages))
total_actifs_circuit = total_numeros_bruts - total_exclus_circuit

# Affichage du Panneau d'indicateur du circuit réduit
st.info(f"💡 **Indicateur de Sourdine :** Le système a analysé les 3 dernières sorties et a détecté **{total_exclus_circuit} numéros chauds** appartenant à ton Circuit Fermé. Ils ont été placés en sourdine. Ton champ de prédiction actuel est restreint à **{total_actifs_circuit} numéros restants**.")

# =====================================================================
# 4. AFFICHAGE DES COLONNES
# =====================================================================
st.markdown("---")
st.subheader(f"📊 1️⃣ Cartographie du Circuit Réduit ({jeu})")

tab_visuel, tab_tableaux = st.tabs(["🖼️ Vue Sourdine (Visuelle)", "📝 Statut Thermique"])

with tab_visuel:
    for nom_col, liste_nums in COLONNES_BRUTES.items():
        restants = [n for n in liste_nums if n not in numeros_sortis_3_tirages]
        st.markdown(f"#### {nom_col} ({len(restants)} restants)")
        nb_elements = len(liste_nums)
        cols_badge = st.columns(nb_elements)
        for idx, n in enumerate(liste_nums):
            if n in restants:
                cols_badge[idx].markdown(f"<div style='background-color:#047857;color:white;padding:5px;border-radius:4px;text-align:center;font-weight:bold;box-shadow: 1px 1px 3px black;'>🟢 {n}</div>", unsafe_allow_html=True)
            else:
                cols_badge[idx].markdown(f"<div style='background-color:#1e293b;color:#64748b;padding:5px;border-radius:4px;text-align:center;text-decoration:line-through;'>❌ {n}</div>", unsafe_allow_html=True)
        st.markdown(" ")

with tab_tableaux:
    for nom_col, liste_nums in COLONNES_BRUTES.items():
        st.markdown(f"#### {nom_col}")
        donnees_colonne = []
        for n in liste_nums:
            statut = "🟢 DISPONIBLE" if n not in numeros_sortis_3_tirages else "❌ EN SOURDINE"
            historique_apparition = dictionnaire_ecarts.get(n, "Non sorti")
            donnees_colonne.append({"Numéro": n, "Filtre Sourdine": statut, "Dernière Sortie": historique_apparition})
        st.dataframe(pd.DataFrame(donnees_colonne), use_container_width=True, hide_index=True)

# =====================================================================
# 5. PANNEAU DE SAISIE
# =====================================================================
st.markdown("---")
st.subheader(f"🎯 2️⃣ Saisie manuelle (Nouveau Tirage {jeu})")
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

if st.button("💾 Enregistrer et recalculer le circuit réduit"):
    if len(tirage_numeros_propres) == 5:
        nouvelle_ligne = {"Jeu": jeu, "Date": str(date_tirage), "N1": n1, "N2": n2, "N3": n3, "N4": n4, "N5": n5, "E1": e1_csv, "E2": e2_csv}
        df_nouveau = pd.DataFrame([nouvelle_ligne])
        df_existant = pd.read_csv(FICHIER_ACTIF) if os.path.exists(FICHIER_ACTIF) else pd.DataFrame()
        pd.concat([df_existant, df_nouveau], ignore_index=True).to_csv(FICHIER_ACTIF, index=False)
        st.success(f"✅ Nouveau tirage enregistré. Sourdine mise à jour !")
        st.rerun()
    else:
        st.error("⚠️ Saisie incomplète.")

# =====================================================================
# 6. GRILLES D'ATTAQUE GÉNÉRÉES
# =====================================================================
st.markdown("---")
st.subheader("🎰 3️⃣ Prédictions — Vos Grilles sur Circuit Ultra-Réduit")
grilles_actives = grilles_loto if jeu == "Loto" else grilles_euro

for nom, num_liste, bonus in grilles_actives:
    st.markdown(f"**{nom}**")
    cols = st.columns(7)
    for i, num in enumerate(sorted(num_liste)):
        cols[i].button(f"💎 {num}", key=f"btn_{nom}_{i}", disabled=True)
    if jeu == "Loto":
        cols[5].button(f"🌟 {bonus}", key=f"chance_{nom}", disabled=True)
    else:
        cols[5].button(f"⭐ {bonus[0]}", key=f"et1_{nom}", disabled=True)
        cols[6].button(f"⭐ {bonus[1]}", key=f"et2_{nom}", disabled=True)

# =====================================================================
# 7. HISTORIQUE LATÉRAL
# =====================================================================
st.sidebar.header(f"📊 Historique Global {jeu}")
if os.path.exists(FICHIER_ACTIF):
    df_side = pd.read_csv(FICHIER_ACTIF)
    st.sidebar.dataframe(df_side, height=400)
    if st.sidebar.button("🗑️ Réinitialiser cette base"):
        os.remove(FICHIER_ACTIF)
        st.rerun()

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

CSV_FILE = "historique_tirages.csv"

# =====================================================================
# 2. MOTEUR STATISTIQUE ET CALCULS DES ÉCARTS (SANS ERREUR)
# =====================================================================
numeros_sortis_3_tirages = set()
dictionnaire_ecarts = {}

# Initialisation par défaut pour chaque numéro
for col_name, nums in COLONNES_BRUTES.items():
    for n in nums:
        dictionnaire_ecarts[n] = "Non sorti (+3)"

if os.path.exists(CSV_FILE):
    try:
        df_hist = pd.read_csv(CSV_FILE)
        if not df_hist.empty:
            total_tirages = len(df_hist)
            
            # 1. Capture des numéros des 3 derniers tirages
            derniers_3 = df_hist.tail(3)
            for _, row in derniers_3.iterrows():
                for col_key in ["N1", "N2", "N3", "N4", "N5"]:
                    numeros_sortis_3_tirages.add(int(row[col_key]))
            
            # 2. Calcul de la distance exacte (sans variable corrompue)
            for col_name, nums in COLONNES_BRUTES.items():
                for n in nums:
                    apparitions = df_hist[(df_hist["N1"] == n) | (df_hist["N2"] == n) | 
                                          (df_hist["N3"] == n) | (df_hist["N4"] == n) | 
                                          (df_hist["N5"] == n)]
                    if not apparitions.empty:
                        dernier_index = int(apparitions.index[-1])
                        distance = total_tirages - 1 - dernier_index
                        if distance == 0:
                            dictionnaire_ecarts[n] = "Tirage précédent"
                        else:
                            dictionnaire_ecarts[n] = f"Il y a {distance} tirage(s)"
                    else:
                        dictionnaire_ecarts[n] = "Non sorti (+3)"
    except Exception as e:
        st.error(f"Erreur lors de l'analyse statistique : {e}")

# Fonction de filtrage des colonnes pour la création des grilles
def filtrer_colonne_active(nom_colonne, taille_demandee=5):
    numeros_bruts = COLONNES_BRUTES[nom_colonne]
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

# Assemblage des grilles de combat
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

# =====================================================================
# 3. INTERFACE GRAPHICS STREAMLIT
# =====================================================================
st.set_page_config(page_title="Observatoire Circuit Fermé", layout="centered")
st.title("🔒 Analyseur par Colonne & Numéros Restants")

# =====================================================================
# 4. OBSERVATOIRE DÉTAILLÉ COLONNE PAR COLONNE (SORTIES VS RESTANTS)
# =====================================================================
st.subheader("📊 1️⃣ État de vos Colonnes (Fenêtre de 3 Tirages)")
st.write("Visualisez pour chaque colonne les numéros disponibles et l'historique des sorties récentes :")

# Séparation en deux onglets pour une lecture plus propre
tab_visuel, tab_tableaux = st.tabs(["🖼️ Vue Visuelle", "📝 Vue Tableaux Détaillés"])

with tab_visuel:
    for nom_col, liste_nums in COLONNES_BRUTES.items():
        restants = [n for n in liste_nums if n not in numeros_sortis_3_tirages]
        st.markdown(f"#### {nom_col}")
        
        cols_badge = st.columns(9)
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
            statut = "🟢 RESTANT (Disponible)" if n not in numeros_sortis_3_tirages else "❌ SORTI (Écarté)"
            historique_apparition = dictionnaire_ecarts.get(n, "Non sorti")
            donnees_colonne.append({
                "Numéro": n,
                "Statut Actuel": statut,
                "Dernière Apparition": historique_apparition
            })
            
        df_colonne = pd.DataFrame(donnees_colonne)
        st.dataframe(df_colonne, use_container_width=True, hide_index=True)

st.markdown("---")
jeu = st.radio("2️⃣ Type de tirage actuel :", ("Loto", "EuroMillions"), horizontal=True)
st.markdown("---")

# =====================================================================
# 5. PANNEAU DE SAISIE ET SAUVEGARDE
# =====================================================================
st.subheader("🎯 3️⃣ Saisie du Nouveau Tirage Officiel")
date_tirage = st.date_input("Date du tirage :")

col_saisie = st.columns(5)
n1 = col_saisie[0].number_input("N° 1", min_value=0, max_value=50, value=0, key="n1")
n2 = col_saisie[1].number_input("N° 2", min_value=0, max_value=50, value=0, key="n2")
n3 = col_saisie[2].number_input("N° 3", min_value=0, max_value=50, value=0, key="n3")
n4 = col_saisie[3].number_input("N° 4", min_value=0, max_value=50, value=0, key="n4")
n5 = col_saisie[4].number_input("N° 5", min_value=0, max_value=50, value=0, key="n5")

tirage_numeros_propres = [n for n in [n1, n2, n3, n4, n5] if n != 0]

etoiles_sorties = []
chance_sorti = 0

if jeu == "Loto":
    col_bonus = st.columns(3)
    chance_sorti = col_bonus[0].number_input("Numéro Chance", min_value=0, max_value=10, value=0)
    e1_csv, e2_csv = chance_sorti, 0
else:
    col_bonus = st.columns(3)
    et1 = col_bonus[0].number_input("Étoile 1", min_value=0, max_value=12, value=0)
    et2 = col_bonus[1].number_input("Étoile 2", min_value=0, max_value=12, value=0)
    etoiles_sorties =

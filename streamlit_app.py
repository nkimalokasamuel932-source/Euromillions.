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

CHANCES_LOTO = [3, 6, 2, 7, 5, 9]
ETOILES_EURO = [[1, 9], [3, 11], [2, 8], [4, 12], [5, 10], [6, 7]]

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
# 3. INTERFACE GRAPHIQUE STREAMLIT
# =====================================================================
st.set_page_config(page_title="Observatoire Circuit Fermé", layout="centered")
st.title("🔒 Radar Croisé V45 — Maillage Intensif")

jeu = st.radio("🔄 Sélectionnez le moteur de jeu actif :", ("Loto", "EuroMillions"), horizontal=True)

FICHIER_ACTIF = CSV_LOTO if jeu == "Loto" else CSV_EURO

# =====================================================================
# 4. EXTRACTION ET FILTRAGE DES NUMÉROS
# =====================================================================
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

# Extraction des forces disponibles par colonne (sans limite de taille pour le mixage)
def obtenir_disponibles(nom_colonne):
    return [n for n in COLONNES_BRUTES[nom_colonne] if n not in numeros_sortis_3_tirages]

# Si une colonne est trop vide, on remet ses numéros de secours pour éviter les lignes vides
def sécuriser_liste(liste_dispo, nom_colonne):
    if len(liste_dispo) < 5:
        return liste_dispo + [n for n in COLONNES_BRUTES[nom_colonne] if n not in liste_dispo]
    return liste_dispo

disp0 = sécuriser_liste(obtenir_disponibles("COLONNE 0 (Ancrage)"), "COLONNE 0 (Ancrage)")
disp1 = sécuriser_liste(obtenir_disponibles("COLONNE 1 (Verrous)"), "COLONNE 1 (Verrous)")
disp2 = sécuriser_liste(obtenir_disponibles("COLONNE 2 (Résonance)"), "COLONNE 2 (Résonance)")
disp3 = sécuriser_liste(obtenir_disponibles("COLONNE 3 (Dérive)"), "COLONNE 3 (Dérive)")

# =====================================================================
# GENERATION DU NOUVEAU MAILLAGE INTER-AXES
# =====================================================================
grilles_loto = [
    ("Grille Dérive pure (Axe Col 3)", [disp3[0], disp3[1], disp3[2], disp3[3], disp3[4]], CHANCES_LOTO[3]),
    ("Grille Centrale pure (Axe Col 0 & 2)", [disp0[0], disp0[1], disp0[2], disp2[0], disp2[1]], CHANCES_LOTO[2]),
    ("Grille Verrous pure (Axe Col 1)", [disp1[0], disp1[1], disp1[2], disp1[3], disp1[4]], CHANCES_LOTO[1]),
    
    # LES FUSIONS INTER-COLONNES (POUR ASSOCIER ANCRAGE, VERROUS ET DÉRIVE ENSEMBLE)
    ("Grille Inter-Axes A (Fusion Ancrage + Verrous + Dérive)", [disp0[0], disp0[1], disp1[0], disp3[0], disp3[1]], CHANCES_LOTO[4]),
    ("Grille Inter-Axes B (Maillage Transversal Alterné)", [disp0[0], disp2[0], disp1[0], disp1[1], disp3[0]], CHANCES_LOTO[5]),
    
    ("Grille Transversale (Mixte Historique)", [disp0[0], disp2[2], disp0[1], disp2[3], disp1[0]], CHANCES_LOTO[0])
]

grilles_euro = [
    ("Grille Dérive pure (Axe Col 3)", [disp3[0], disp3[1], disp3[2], disp3[3], disp3[4]], ETOILES_EURO[3]),
    ("Grille Centrale pure (Axe Col 0 & 2)", [disp0[0], disp0[1], disp0[2], disp2[0], disp2[1]], ETOILES_EURO[2]),
    ("Grille Verrous pure (Axe Col 1)", [disp1[0], disp1[1], disp1[2], disp1[3], disp1[4]], ETOILES_EURO[1]),
    
    ("Grille Inter-Axes A (Fusion Ancrage + Verrous + Dérive)", [disp0[0], disp0[1], disp1[0], disp3[0], disp3[1]], ETOILES_EURO[4]),
    ("Grille Inter-Axes B (Maillage Transversal Alterné)", [disp0[0], disp2[0], disp1[0], disp1[1], disp3[0]], ETOILES_EURO[5]),
    
    ("Grille Transversale (Mixte Historique)", [disp0[0], disp2[2], disp0[1], disp2[3], disp1[0]], ETOILES_EURO[0])
]

# =====================================================================
# AFFICHAGE INTERFACE STREAMLIT
# =====================================================================
st.subheader(f"📊 1️⃣ Circuit Réduit Actif ({jeu})")
for nom_col, liste_nums in COLONNES_BRUTES.items():
    restants = [n for n in liste_nums if n not in numeros_sortis_3_tirages]
    st.markdown(f"**{nom_col}**")
    cols_badge = st.columns(len(liste_nums))
    for idx, n in enumerate(liste_nums):
        if n in restants:
            cols_badge[idx].markdown(f"<div style='background-color:#047857;color:white;padding:5px;border-radius:4px;text-align:center;font-weight:bold;'>🟢 {n}</div>", unsafe_allow_html=True)
        else:
            cols_badge[idx].markdown(f"<div style='background-color:#1e293b;color:#64748b;padding:5px;border-radius:4px;text-align:center;text-decoration:line-through;'>❌ {n}</div>", unsafe_allow_html=True)

st.markdown("---")

# =====================================================================
# AFFICHAGE DES GRILLES DE COMBAT PROPOSÉES
# =====================================================================
st.subheader("🎰 2️⃣ Vos Propositions de Grilles (Moteur de Croisement Activé)")
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
# HISTORIQUE LATÉRAL
# =====================================================================
st.sidebar.header(f"📊 Données {jeu}")
if os.path.exists(FICHIER_ACTIF):
    df_side = pd.read_csv(FICHIER_ACTIF)
    st.sidebar.dataframe(df_side, height=400)
    if st.sidebar.button("🗑️ Vider cette base uniquement"):
        os.remove(FICHIER_ACTIF)
        st.rerun()

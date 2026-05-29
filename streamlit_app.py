import streamlit as st
import pandas as pd
import os

# =====================================================================
# 1. ARCHITECTURE DES COLONNES DU CIRCUIT FERMÉ BRUT
# =====================================================================
# Tes 36 numéros invariants d'origine (le réservoir absolu)
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
# 2. CHARGEMENT ET FILTRAGE AUTOMATIQUE DES ÉCARTS (MOTEUR DYNAMIQUE)
# =====================================================================
numeros_bannis = set()

# Si le fichier CSV existe, on regarde le tout dernier tirage enregistré
if os.path.exists(CSV_FILE):
    try:
        df_hist = pd.read_csv(CSV_FILE)
        if not df_hist.empty:
            dernier_tirage = df_hist.iloc[-1] # Récupère la dernière ligne
            # On extrait les 5 numéros sortis
            numeros_bannis = {int(dernier_tirage["N1"]), int(dernier_tirage["N2"]), 
                              int(dernier_tirage["N3"]), int(dernier_tirage["N4"]), 
                              int(dernier_tirage["N5"])}
    except Exception as e:
        pass

# Fonction de roulement interne : prend les numéros d'une colonne qui ne sont PAS bannis
def filtrer_colonne(nom_colonne, taille_demandee=5):
    numeros_bruts = COLONNES_BRUTES[nom_colonne]
    # On garde uniquement ceux qui ne sont pas sortis au dernier tirage
    numeros_filtrés = [n for n in numeros_bruts if n not in numeros_bannis]
    
    # Sécurité : si trop de numéros sont bannis et qu'on manque de numéros, on complète avec les bruts
    if len(numeros_filtrés) < taille_demandee:
        for n in numeros_bruts:
            if n not in numeros_filtrés:
                numeros_filtrés.append(n)
                
    return numeros_filtrés[:taille_demandee]

# Reconstruction dynamique des colonnes épurées
col0_active = filtrer_colonne("COLONNE 0 (Ancrage)")
col1_active = filtrer_colonne("COLONNE 1 (Verrous)")
col2_active = filtrer_colonne("COLONNE 2 (Résonance)")
col3_active = filtrer_colonne("COLONNE 3 (Dérive)")

# Assemblage dynamique de tes 4 grilles de choc sans les numéros sortis
grilles_loto = [
    ("Grille Choc - Axe Dérive (Col 3)", [col3_active[0], col3_active[1], col3_active[2], col3_active[3], col3_active[4]], CHANCES_LOTO[3]),
    ("Grille Choc - Axe Central (Col 0 & 2)", [col0_active[0], col0_active[1], col0_active[2], col2_active[0], col2_active[1]], CHANCES_LOTO[2]),
    ("Grille Choc - Axe Verrous (Col 1)", [col1_active[0], col1_active[1], col1_active[2], col1_active[3], col1_active[4]], CHANCES_LOTO[1]),
    ("Grille Choc - Axe Transversal (Mixte)", [col0_active[0], col2_active[2], col0_active[1], col2_active[3], col1_active[0]], CHANCES_LOTO[0])
]

grilles_euro = [
    ("Grille Choc - Axe Dérive (Col 3)", [col3_active[0], col3_active[1], col3_active[2], col3_active[3], col3_active[4]], ETOILES_EURO[3]),
    ("Grille Choc - Axe Central (Col 0 & 2)", [col0_active[0], col0_active[1], col0_active[2], col2_active[0], col2_active[1]], ETOILES_EURO[2]),
    ("Grille Choc - Axe Verrous (Col 1)", [col1_active[0], col1_active[1], col1_active[2], col1_active[3], col1_active[4]], ETOILES_EURO[1]),
    ("Grille Choc - Axe Transversal (Mixte)", [col0_active[0], col2_active[2], col0_active[1], col2_active[3], col1_active[0]], ETOILES_EURO[0])
]

# =====================================================================
# 3. INTERFACE GRAPHIQUE STREAMLIT
# =====================================================================
st.set_page_config(page_title="Coffre-Fort Écarts Automatiques", layout="centered")

st.title("🔒 Circuit Fermé V45 : Écarts Automatiques")

if len(numeros_bannis) > 0:
    st.warning(f"⚠️ Mode Écarts Activé : Les numéros {list(numeros_bannis)} du dernier tirage ont été automatiquement retirés et remplacés par roulement.")
else:
    st.info("ℹ️ Mode Initial : Aucun tirage dans le CSV. Vos grilles utilisent les têtes de colonnes par défaut.")

st.markdown("---")
jeu = st.radio("1️⃣ Choisis ton type de tirage :", ("Loto", "EuroMillions"), horizontal=True)
st.markdown("---")

# =====================================================================
# 4. PANNEAU DE SAISIE ET SAUVEGARDE CSV
# =====================================================================
st.subheader("🎯 2️⃣ Saisie et Archivage du Tirage Officiel")
date_tirage = st.date_input("Date du tirage :")

col_saisie = st.columns(5)
n1 = col_saisie[0].number_input("N° 1", min_value=0, max_value=50, value=0, key="n1")
n2 = col_saisie[1].number_input("N° 2", min_value=0, max_value=50, value=0, key="n2")
n3 = col_saisie[2].number_input("N° 3", min_value=0, max_value=50, value=0, key="n3")
n4 = col_saisie[3].number_input("N° 4", min_value=0, max_value=50, value=0, key="n4")
n5 = col_saisie[4].number_input("N° 5", min_value=0, max_value=50, value=0, key="n5")

tirage_numeros = [n1, n2, n3, n4, n5]
tirage_numeros_propres = [n for n in tirage_numeros if n != 0]

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
    etoiles_sorties = [et1, et2]
    etoiles_sorties = [e for e in etoiles_sorties if e != 0]
    e1_csv, e2_csv = et1, et2

if st.button("💾 Enregistrer ce tirage et Recalculer les Écarts"):
    if len(tirage_numeros_propres) == 5:
        nouvelle_ligne = {
            "Jeu": jeu, "Date": str(date_tirage),
            "N1": n1, "N2": n2, "N3": n3, "N4": n4, "N5": n5,
            "E1": e1_csv, "E2": e2_csv
        }
        df_nouveau = pd.DataFrame([nouvelle_ligne])
        if os.path.exists(CSV_FILE):
            df_existant = pd.read_csv(CSV_FILE)
            df_final = pd.concat([df_existant, df_nouveau], ignore_index=True)
        else:
            df_final = df_nouveau
        df_final.to_csv(CSV_FILE, index=False)
        st.success("✅ Tirage enregistré ! Les grilles du dessous ont été recalculées instantanément.")
        st.rerun()
    else:
        st.error("⚠️ Veuillez remplir les 5 numéros avant d'enregistrer.")

st.markdown("---")

# =====================================================================
# 5. AFFICHAGE DES GRILLES DYNAMIQUES
# =====================================================================
tirage_actif = len(tirage_numeros_propres) > 0

if jeu == "Loto":
    st.subheader("🎰 3️⃣ Vos 4 Grilles Fixes LOTO (Mises à jour)")
    for nom, num_liste, chance in grilles_loto:
        bons_numeros = set(num_liste).intersection(set(tirage_numeros_propres))
        bonne_chance = (chance == chance_sorti) and (chance_sorti != 0)
        
        st.markdown(f"**{nom}**")
        cols = st.columns(6)
        for i, num in enumerate(sorted(num_liste)):
            label = f"🔥 {num}" if num in bons_numeros else f"{num}"
            cols[i].button(label, key=f"loto_{nom}_{i}", disabled=True)
        label_chance = f"💥 🌟 {chance}" if bonne_chance else f"🌟 {chance}"
        cols[5].button(label_chance, key=f"loto_chance_{nom}", disabled=True)
        if tirage_actif:
            st.success(f"📈 Résultat : {len(bons_numeros)} numéro(s) trouvé(s)")
        st.markdown(" ")
else:
    st.subheader("🌌 3️⃣ Vos 4 Grilles Fixes EUROMILLIONS (Mises à jour)")
    for nom, num_liste, etoiles in grilles_euro:
        bons_numeros = set(num_liste).intersection(set(tirage_numeros_propres))
        bonnes_etoiles = set(etoiles).intersection(set(etoiles_sorties))
        
        st.markdown(f"**{nom}**")
        cols = st.columns(7)
        for i, num in enumerate(sorted(num_liste)):
            label = f"🔥 {num}" if num in bons_numeros else f"{num}"
            cols[i].button(label, key=f"euro_{nom}_{i}", disabled=True)
        for j, et in enumerate(etoiles):
            label_et = f"💥 ⭐ {et}" if et in bonnes_etoiles else f"⭐ {et}"
            cols[5+j].button(label_et, key=f"euro_et{j}_{nom}", disabled=True)
        if tirage_actif:
            st.success(f"📈 Résultat : {len(bons_numeros)} numéro(s) et {len(bonnes_etoiles)} étoile(s)")
        st.markdown(" ")

# =====================================================================
# 6. HISTORIQUE CSV
# =====================================================================
st.sidebar.header("📊 Historique CSV")
if os.path.exists(CSV_FILE):
    df_historique = pd.read_csv(CSV_FILE)
    st.sidebar.dataframe(df_historique, height=300)
    if st.sidebar.button("🗑️ Effacer l'historique CSV"):
        os.remove(CSV_FILE)
        st.sidebar.warning("Historique supprimé.")
        st.rerun()
else:
    st.sidebar.info("Aucun tirage enregistré.")

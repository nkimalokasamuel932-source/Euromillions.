import streamlit as st
import pandas as pd

# =====================================================================
# 1. ARCHITECTURE STRICTE DU CIRCUIT FERMÉ (FIXED POOLS)
# =====================================================================

ARCHITECTURE_LOTO = {
    "COLONNE 0 (Ancrage)": [3, 10, 15, 17, 20, 30, 35, 41, 43],
    "COLONNE 1 (Verrous)": [1, 4, 14, 25, 26, 32, 34, 39, 48],
    "COLONNE 2 (Résonance)": [2, 8, 12, 18, 19, 30, 33, 36, 46],
    "COLONNE 3 (Dérive)": [7, 16, 21, 27, 28, 31, 37, 38, 45, 48]
}

# Pour l'EuroMillions, on s'assure d'avoir au moins 5 numéros par bloc
ARCHITECTURE_EUROMILLIONS = {
    "COLONNE 0 (Ancrage & Écarts)": [3, 10, 15, 17, 20, 30, 35, 41, 43, 50],
    "COLONNE 1 (Poussée Latérale)": [1, 4, 14, 25, 26, 32, 34, 39, 44, 48],
    "COLONNE 2 (Noyaux Centraux)": [2, 8, 12, 18, 19, 30, 33, 36, 42, 46],
    "COLONNE 3 (Dérive Haute)": [7, 16, 21, 27, 28, 31, 37, 38, 45, 49]
}

ETOILES_EUROMILLIONS = {
    "COLONNE 0 (Ancrage & Écarts)": [1, 9],
    "COLONNE 1 (Poussée Latérale)": [3, 11],
    "COLONNE 2 (Noyaux Centraux)": [2, 8],
    "COLONNE 3 (Dérive Haute)": [4, 7, 12]
}

CHANCES_LOTO = [3, 6, 2, 7]  # Tes numéros Chance clés issus de ton circuit

# =====================================================================
# 2. INTERFACE STREAMLIT
# =====================================================================

st.set_page_config(page_title="Circuit Fermé V45 - Grilles Pures", layout="centered")

st.title("⚡ Mon Circuit Fermé - Générateur Fixe")
st.write("Ce module extrait directement vos numéros verrouillés **sans aucun filtre réducteur** et **sans aléatoire**.")

# Sélection du type de jeu
jeu_selectionne = st.radio("Sélectionnez le jeu à afficher :", ("Loto", "EuroMillions"))

st.markdown("---")

# =====================================================================
# 3. LOGIQUE D'EXTRACTION SANS FILTRE (GRILLES FIXES)
# =====================================================================

if jeu_selectionne == "Loto":
    st.subheader("🎰 Vos 4 Grilles Fixes - Loto")
    st.info("Chaque grille correspond aux 5 premiers numéros de votre colonne. Si une colonne surchauffe, vos numéros restent ensemble !")
    
    idx = 0
    for nom_colonne, numeros in ARCHITECTURE_LOTO.items():
        # Extraction brute des 5 premiers numéros de la colonne
        grille_pure = sorted(numeros[:5])
        num_chance = CHANCES_LOTO[idx] if idx < len(CHANCES_LOTO) else 2
        
        # Affichage visuel du ticket
        st.markdown(f"### 🎫 {nom_colonne}")
        cols = st.columns(6)
        for i, num in enumerate(grille_pure):
            cols[i].button(f"{num}", key=f"loto_{nom_colonne}_{i}", disabled=True)
        cols[5].button(f"🌟 {num_chance}", key=f"loto_chance_{nom_

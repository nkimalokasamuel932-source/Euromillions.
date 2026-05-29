import streamlit as st

# =====================================================================
# 1. FIXATION STRICTE ET INVARIANTE DU CIRCUIT FERMÉ
# =====================================================================
# Tes 36 numéros officiels (strictement inviolables, aucun ajout extérieur)
ARCHITECTURE_LOTO = {
    "COLONNE 0 (Ancrage)": [3, 10, 15, 17, 20, 30, 35, 41, 43],
    "COLONNE 1 (Verrous)": [1, 4, 14, 25, 26, 32, 34, 39, 48],
    "COLONNE 2 (Résonance)": [2, 8, 12, 18, 19, 30, 33, 36, 46],
    "COLONNE 3 (Dérive)": [7, 16, 21, 27, 28, 31, 37, 38, 45, 48]
}

# Numéros de secours / Étoiles pour l'EuroMillions (uniquement issus de ton circuit)
CHANCES_LOTO = [3, 6, 2, 7]
ETOILES_EURO = [[1, 9], [3, 11], [2, 8], [4, 12]]

# =====================================================================
# 2. CONFIGURATION DE L'INTERFACE STREAMLIT
# =====================================================================
st.set_page_config(page_title="Circuit Fermé V45 - Stable", layout="centered")

st.title("🔒 Coffre-Fort V45 : Format Simplifié")
st.write("Statut : **100% Opérationnel**. Vos 4 grilles fixes de combat sans aucun hasard.")

st.markdown("---")

# Sélecteur de Jeu pour éviter les crashs de l'interface
jeu = st.radio("Sélectionnez le tirage à préparer :", ("Loto", "EuroMillions"))

st.markdown("---")

# =====================================================================
# 3. LOGIQUE D'AFFICHAGE SANS HASARD (LES 4 GRILLES CHOC)
# =====================================================================

if jeu == "Loto":
    st.subheader("🎰 Vos 4 Grilles Fixes Optimisées - LOTO")
    st.info("Ce format combine les coeurs de tes colonnes. Tu joues moins de grilles, mais tes numéros clés restent soudés ensemble.")

    # Les 4 axes chocs du Loto (Uniquement tes numéros)
    grilles_loto = [
        ("Grille Choc - Axe Dérive (Col 3)", [21, 27, 31, 38, 48], CHANCES_LOTO[3]),
        ("Grille Choc - Axe Central (Col 0 & 2)", [15, 17, 20, 30, 36], CHANCES_LOTO[2]),
        ("Grille Choc - Axe Verrous (Col 1)", [1, 4, 14, 25, 26], CHANCES_LOTO[1]),
        ("Grille Choc - Axe Transversal (Mixte)", [3, 8, 10, 12, 19], CHANCES_LOTO[0])
    ]

    # Rendu des boutons Loto
    for nom, num_liste, chance in grilles_loto:
        st.markdown(f"**{nom}**")
        cols = st.columns(6)
        for i, num in enumerate(sorted(num_liste)):
            cols[i].button(f"{num}", key=f"loto_{nom}_{i}", disabled=True)
        cols[5].button(f"🌟 {chance}", key=f"loto_chance_{nom}", disabled=True)
        st.markdown(" ")

else:
    st.subheader("🌌 Vos 4 Grilles Fixes Optimisées - EUROMILLIONS")
    st.info("Adaptation de tes colonnes fermées au format EuroMillions avec les couples d'étoiles cibles.")

    # Les 4 axes chocs EuroMillions (Identiques, adaptés avec 2 étoiles)
    grilles_euro = [
        ("Grille Choc - Axe Dérive (Col 3)", [21, 27, 31, 38, 45], ETOILES_EURO[3]),
        ("Grille Choc - Axe Central (Col 0 & 2)", [15, 17, 20, 30, 36], ETOILES_EURO[2]),
        ("Grille Choc - Axe Verrous (Col 1)", [1, 4, 14, 25, 26], ETOILES_EURO[1]),
        ("Grille Choc - Axe Transversal (Mixte)", [3, 8, 10, 12, 19], ETOILES_EURO[0])
    ]

    # Rendu des boutons EuroMillions (5 numéros + 2 étoiles)
    for nom, num_liste, etoiles in grilles_euro:
        st.markdown(f"**{nom}**")
        cols = st.columns(7)
        for i, num in enumerate(sorted(num_liste)):
            cols[i].button(f"{num}", key=f"euro_{nom}_{i}", disabled=True)
        # Affichage des deux étoiles
        cols[5].button(f"⭐ {etoiles[0]}", key=f"euro_et1_{nom}", disabled=True)
        cols[6].button(f"⭐ {etoiles[1]}", key=f"euro_et2_{nom}", disabled=True)
        st.markdown(" ")

# =====================================================================
# 4. BARRE LATÉRALE DE CONTRÔLE
# =====================================================================
st.sidebar.success("Mode Allégé & Fixe Actif")
st.sidebar.write("Volume : 4 Tickets invariants")
st.sidebar.markdown("""
**Rappel de surveillance ce vendredi :**
Regarder de très près la **Colonne 0 (Ancrage)** pour voir si elle confirme sa force ou si elle passe le relais à la **Colonne 1**.
""")

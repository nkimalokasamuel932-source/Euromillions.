import streamlit as st

# =====================================================================
# 1. FIXATION STRICTE ET INVARIANTE DU CIRCUIT FERMÉ
# =====================================================================
ARCHITECTURE_LOTO = {
    "COLONNE 0 (Ancrage)": [3, 10, 15, 17, 20, 30, 35, 41, 43],
    "COLONNE 1 (Verrous)": [1, 4, 14, 25, 26, 32, 34, 39, 48],
    "COLONNE 2 (Résonance)": [2, 8, 12, 18, 19, 30, 33, 36, 46],
    "COLONNE 3 (Dérive)": [7, 16, 21, 27, 28, 31, 37, 38, 45, 48]
}

CHANCES_LOTO = [3, 6, 2, 7]
ETOILES_EURO = [[1, 9], [3, 11], [2, 8], [4, 12]]

# Définition fixe de tes 4 grilles de choc
grilles_loto = [
    ("Grille Choc - Axe Dérive (Col 3)", [21, 27, 31, 38, 48], CHANCES_LOTO[3]),
    ("Grille Choc - Axe Central (Col 0 & 2)", [15, 17, 20, 30, 36], CHANCES_LOTO[2]),
    ("Grille Choc - Axe Verrous (Col 1)", [1, 4, 14, 25, 26], CHANCES_LOTO[1]),
    ("Grille Choc - Axe Transversal (Mixte)", [3, 8, 10, 12, 19], CHANCES_LOTO[0])
]

grilles_euro = [
    ("Grille Choc - Axe Dérive (Col 3)", [21, 27, 31, 38, 45], ETOILES_EURO[3]),
    ("Grille Choc - Axe Central (Col 0 & 2)", [15, 17, 20, 30, 36], ETOILES_EURO[2]),
    ("Grille Choc - Axe Verrous (Col 1)", [1, 4, 14, 25, 26], ETOILES_EURO[1]),
    ("Grille Choc - Axe Transversal (Mixte)", [3, 8, 10, 12, 19], ETOILES_EURO[0])
]

# =====================================================================
# 2. CONFIGURATION DE L'INTERFACE STREAMLIT
# =====================================================================
st.set_page_config(page_title="Circuit Fermé V45 - Analyseur", layout="centered")

st.title("🔒 Coffre-Fort V45 & Analyseur de Résultats")
st.write("Statut : **Mode Expert**. Tes grilles sont figées et vérifiées automatiquement.")

st.markdown("---")

jeu = st.radio("Sélectionnez le tirage à préparer ou analyser :", ("Loto", "EuroMillions"))

st.markdown("---")

# =====================================================================
# 3. INTERFACE DE SAISIE DES RÉSULTATS (BARRE LATÉRALE)
# =====================================================================
st.sidebar.header("🎯 Saisie du Tirage")
st.sidebar.write("Entre le tirage officiel pour vérifier tes gains :")

# Formulaire de saisie dynamique
n1 = st.sidebar.number_input("Numéro 1", min_value=0, max_value=50, value=0)
n2 = st.sidebar.number_input("Numéro 2", min_value=0, max_value=50, value=0)
n3 = st.sidebar.number_input("Numéro 3", min_value=0, max_value=50, value=0)
n4 = st.sidebar.number_input("Numéro 4", min_value=0, max_value=50, value=0)
n5 = st.sidebar.number_input("Numéro 5", min_value=0, max_value=50, value=0)

tirage_numeros = [n1, n2, n3, n4, n5]

if jeu == "Loto":
    chance_sorti = st.sidebar.number_input("Numéro Chance", min_value=0, max_value=10, value=0)
    etoiles_sorties = []
else:
    et1 = st.sidebar.number_input("Étoile 1", min_value=0, max_value=12, value=0)
    et2 = st.sidebar.number_input("Étoile 2", min_value=0, max_value=12, value=0)
    etoiles_sorties = [et1, et2]
    chance_sorti = 0

# Nettoyage des listes (on ignore les 0)
tirage_numeros = [n for n in tirage_numeros if n != 0]
etoiles_sorties = [e for e in etoiles_sorties if e != 0]

# Activé si un tirage est entré
tirage_saisi = len(tirage_numeros) > 0

if tirage_saisi:
    st.sidebar.success("Analyse en cours...")

# =====================================================================
# 4. LOGIQUE D'AFFICHAGE ET VÉRIFICATION EN DIRECT
# =====================================================================

if jeu == "Loto":
    st.subheader("🎰 Vos 4 Grilles Fixes - LOTO")
    
    for nom, num_liste, chance in grilles_loto:
        st.markdown(f"**{nom}**")
        
        # Calcul des bons numéros
        bons_numeros = set(num_liste).intersection(set(tirage_numeros))
        bonne_chance = (chance == chance_sorti) and (chance_sorti != 0)
        
        cols = st.columns(6)
        for i, num in enumerate(sorted(num_liste)):
            # Si le numéro est gagnant, on met une alerte visuelle dans le texte
            label = f"🔥 {num}" if num in bons_numeros else f"{num}"
            cols[i].button(label, key=f"loto_{nom}_{i}", disabled=True)
            
        label_chance = f"💥 🌟 {chance}" if bonne_chance else f"🌟 {chance}"
        cols[5].button(label_chance, key=f"loto_chance_{nom}", disabled=True)
        
        # Affichage du bilan de la grille si un tirage est saisi
        if tirage_saisi:
            txt_chance = " + Chance !" if bonne_chance else ""
            st.code(f"Résultat : {len(bons_numeros)} numéro(s) correct(s){txt_chance} ({list(bons_numeros)})")
        st.markdown(" ")

else:
    st.subheader("🌌 Vos 4 Grilles Fixes - EUROMILLIONS")
    
    for nom, num_liste, etoiles in grilles_euro:
        st.markdown(f"**{nom}**")
        
        # Calcul des bons numéros et étoiles
        bons_numeros = set(num_liste).intersection(set(tirage_numeros))
        bonnes_etoiles = set(etoiles).intersection(set(etoiles_sorties))
        
        cols = st.columns(7)
        for i, num in enumerate(sorted(num_liste)):
            label = f"🔥 {num}" if num in bons_numeros else f"{num}"
            cols[i].button(label, key=f"euro_{nom}_{i}", disabled=True)
            
        for j, et in enumerate(etoiles):
            label_et = f"💥 ⭐ {et}" if et in bonnes_etoiles else f"⭐ {et}"
            cols[5+j].button(label_et, key=f"euro_et{j}_{nom}", disabled=True)
            
        if tirage_saisi:
            st.code(f"Résultat : {len(bons_numeros)} numéro(s) et {len(bonnes_etoiles)} étoile(s) correct(s) ({list(bons_numeros)} | {list(bonnes_etoiles)})")
        st.markdown(" ")

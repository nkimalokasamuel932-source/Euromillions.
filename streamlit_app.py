import streamlit as st

# =====================================================================
# 1. ARCHITECTURE INVARIANTE DU CIRCUIT FERMÉ
# =====================================================================
ARCHITECTURE_LOTO = {
    "COLONNE 0 (Ancrage)": [3, 10, 15, 17, 20, 30, 35, 41, 43],
    "COLONNE 1 (Verrous)": [1, 4, 14, 25, 26, 32, 34, 39, 48],
    "COLONNE 2 (Résonance)": [2, 8, 12, 18, 19, 30, 33, 36, 46],
    "COLONNE 3 (Dérive)": [7, 16, 21, 27, 28, 31, 37, 38, 45, 48]
}

CHANCES_LOTO = [3, 6, 2, 7]
ETOILES_EURO = [[1, 9], [3, 11], [2, 8], [4, 12]]

# Définition stricte de tes 4 grilles de choc (uniquement tes numéros)
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
# 2. INTERFACE GRAPHIQUE STREAMLIT
# =====================================================================
st.set_page_config(page_title="Analyseur Circuit Fermé", layout="centered")

st.title("🔒 Coffre-Fort V45 & Détecteur de Gains")
st.write("Statut : **Actif**. Saisis un tirage ci-dessous pour tester tes 4 grilles fixes.")

st.markdown("---")

# Étape 1 : Choix du mode
jeu = st.radio("1️⃣ Choisis ton type de tirage :", ("Loto", "EuroMillions"), horizontal=True)

st.markdown("---")

# =====================================================================
# 3. PANNEAU DE SAISIE CENTRAL DES RÉSULTATS (IMPOSSIBLE À RATER)
# =====================================================================
st.subheader("🎯 2️⃣ Saisie du Tirage Officiel")
st.write("Entre les numéros sortis pour lancer la vérification automatique :")

# Alignement des cases de saisie sur une seule ligne pour plus de clarté
col_saisie = st.columns(5)
n1 = col_saisie[0].number_input("N° 1", min_value=0, max_value=50, value=0, key="n1")
n2 = col_saisie[1].number_input("N° 2", min_value=0, max_value=50, value=0, key="n2")
n3 = col_saisie[2].number_input("N° 3", min_value=0, max_value=50, value=0, key="n3")
n4 = col_saisie[3].number_input("N° 4", min_value=0, max_value=50, value=0, key="n4")
n5 = col_saisie[4].number_input("N° 5", min_value=0, max_value=50, value=0, key="n5")

# Gestion de la Chance ou des Étoiles juste en dessous
tirage_numeros = [n1, n2, n3, n4, n5]
tirage_numeros = [n for n in tirage_numeros if n != 0] # On filtre les cases vides

etoiles_sorties = []
chance_sorti = 0

if jeu == "Loto":
    col_bonus = st.columns(3)
    chance_sorti = col_bonus[0].number_input("Numéro Chance", min_value=0, max_value=10, value=0)
else:
    col_bonus = st.columns(3)
    et1 = col_bonus[0].number_input("Étoile 1", min_value=0, max_value=12, value=0)
    et2 = col_bonus[1].number_input("Étoile 2", min_value=0, max_value=12, value=0)
    etoiles_sorties = [et1, et2]
    etoiles_sorties = [e for e in etoiles_sorties if e != 0]

st.markdown("---")

# =====================================================================
# 4. AFFICHAGE DES GRILLES AVEC MARQUAGE DES GAINS
# =====================================================================
tirage_actif = len(tirage_numeros) > 0

if jeu == "Loto":
    st.subheader("🎰 3️⃣ Vos 4 Grilles Fixes LOTO")
    
    for nom, num_liste, chance in grilles_loto:
        # Calcul des intersections mathématiques
        bons_numeros = set(num_liste).intersection(set(tirage_numeros))
        bonne_chance = (chance == chance_sorti) and (chance_sorti != 0)
        
        st.markdown(f"**{nom}**")
        cols = st.columns(6)
        
        for i, num in enumerate(sorted(num_liste)):
            # Si le numéro est dans le tirage saisi, on lui met une flamme !
            label = f"🔥 {num}" if num in bons_numeros else f"{num}"
            cols[i].button(label, key=f"loto_{nom}_{i}", disabled=True)
            
        label_chance = f"💥 🌟 {chance}" if bonne_chance else f"🌟 {chance}"
        cols[5].button(label_chance, key=f"loto_chance_{nom}", disabled=True)
        
        # Affichage du rapport direct sous le ticket
        if tirage_actif:
            txt_chance = " + NUMÉRO CHANCE !" if bonne_chance else ""
            st.success(f"📈 Résultat : {len(bons_numeros)} numéro(s) trouvé(s){txt_chance} 🎯 Trouvé(s) : {list(bons_numeros)}")
        st.markdown(" ")

else:
    st.subheader("🌌 3️⃣ Vos 4 Grilles Fixes EUROMILLIONS")
    
    for nom, num_liste, etoiles in grilles_euro:
        bons_numeros = set(num_liste).intersection(set(tirage_numeros))
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
            st.success(f"📈 Résultat : {len(bons_numeros)} numéro(s) et {len(bonnes_etoiles)} étoile(s) 🎯 Trouvé(s) : Numéros {list(bons_numeros)} | Étoiles {list(bonnes_etoiles)}")
        st.markdown(" ")

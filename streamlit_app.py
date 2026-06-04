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
# 2. INTERFACE GRAPHIQUE STREAMLIT
# =====================================================================
st.set_page_config(page_title="Observatoire Circuit Fermé", layout="centered")
st.title("🔒 Radar Croisé V45 — Inverseur de Sourdine")

jeu = st.radio("🔄 Sélectionnez le moteur de jeu actif :", ("Loto", "EuroMillions"), horizontal=True)

strategie = st.radio(
    "🎯 Stratégie des grilles :",
    ("🟢 Jouer les numéros Disponibles (Standard)", "❌ Jouer UNIQUEMENT les numéros Exclus (Sourdine Inverse)"),
    horizontal=False
)

FICHIER_ACTIF = CSV_LOTO if jeu == "Loto" else CSV_EURO

# =====================================================================
# 3. EXTRACTION ET FILTRAGE DES NUMÉROS
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

# =====================================================================
# GENERATION DU MAILLAGE DYNAMIQUE
# =====================================================================
grilles_loto = [
    ("Grille Dérive pure (Axe Col 3)", [disp3[0], disp3[1], disp3[2], disp3[3], disp3[4]], CHANCES_LOTO[3]),
    ("Grille Centrale pure (Axe Col 0 & 2)", [disp0[0], disp0[1], disp0[2], disp2[0], disp2[1]], CHANCES_LOTO[2]),
    ("Grille Verrous pure (Axe Col 1)", [disp1[0], disp1[1], disp1[2], disp1[3], disp1[4]], CHANCES_LOTO[1]),
    ("Grille Inter-Axes A (Fusion)", [disp0[0], disp0[1], disp1[0], disp3[0], disp3[1]], CHANCES_LOTO[4]),
    ("Grille Inter-Axes B (Maillage)", [disp0[0], disp2[0], disp1[0], disp1[1], disp3[0]], CHANCES_LOTO[5]),
    ("Grille Transversale (Mixte)", [disp0[0], disp2[2], disp0[1], disp2[3], disp1[0]], CHANCES_LOTO[0])
]

grilles_euro = [
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

# =====================================================================
# 4. AFFICHAGE DE LA CARTOGRAPHIE VISUELLE
# =====================================================================
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

# =====================================================================
# 5. FORMULAIRE DE SAISIE MANUELLE (LE BLOC COMPLÉTÉ)
# =====================================================================
st.subheader(f"🎯 Saisie manuelle (Nouveau Tirage {jeu})")
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

st.markdown("---")

# =====================================================================
# 6. AFFICHAGE DES GRILLES DE COMBAT PROPOSÉES
# =====================================================================
st.subheader("🎰 Vos Propositions de Grilles Dynamiques")
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
# ZONE 0 : TES ALGORITHMES ACTUELS (REPRÉSENTATION CHRONOLOGIQUE)
# =====================================================================

def obtenir_grilles_existantes():
    """
    Cette fonction représente ce que ton application génère déjà.
    Elle simule les 6 grilles brutes issues du Circuit Fermé V45,
    de la Fusion et du Mixte que tu as testées.
    """
    # Ici, on retrouve tes deux grilles gagnantes et tes autres grilles de test
    grille_fusion = [1, 7, 16, 20, 30]      # Grille Inter-Axes A (2 bons numéros)
    grille_mixte = [1, 2, 18, 20, 30]       # Grille Transversale (2 bons numéros)
    grille_3 = [4, 12, 17, 18, 45]          # Exemple de grille avec suite stricte
    grille_4 = [2, 8, 16, 24, 40]           # Exemple de grille 100% paire
    grille_5 = [5, 15, 25, 35, 45]          # Exemple de grille hors limites de somme
    grille_6 = [3, 9, 14, 22, 31]
    
    return [grille_fusion, grille_mixte, grille_3, grille_4, grille_5, grille_6]


# =====================================================================
# PHASE 1 : LA SOURDINE INVERSÉE STRICTE (FILTRAGE STATISTIQUE)
# =====================================================================

def phase_1_sourdine_strict(grilles_proposees):
    """
    Analyse les grilles et élimine celles qui n'ont presque aucune 
    chance mathématique de sortir (100% paires/impaires, suites longues, etc.).
    """
    grilles_validees = []
    
    for grille in grilles_proposees:
        grille_triee = sorted(grille)
        
        # 1. Filtre Parité : On rejette si 100% Pair (5) ou 100% Impair (0)
        pairs = len([n for n in grille_triee if n % 2 == 0])
        if pairs == 0 or pairs == 5:
            continue
            
        # 2. Filtre Somme : La somme au Loto se situe historiquement entre 60 et 180
        somme = sum(grille_triee)
        if somme < 60 or somme > 180:
            continue
            
        # 3. Filtre Suites : On refuse s'il y a 3 numéros consécutifs (ex: 16-17-18)
        suite_detectee = False
        for i in range(len(grille_triee) - 2):
            if grille_triee[i+1] == grille_triee[i] + 1 and grille_triee[i+2] == grille_triee[i] + 2:
                suite_detectee = True
                break
        if suite_detectee:
            continue
            
        # La grille est validée par la Sourdine
        grilles_validees.append(grille_triee)
        
    return grilles_validees


# =====================================================================
# PHASE 2 : L'INTERSECTION CRITIQUE (LA SUPER-GRILLE FUSION / MIXTE)
# =====================================================================

def phase_2_generer_super_grille(grilles_brutes):
    """
    Analyse le comportement de la Fusion et du Mixte (les 2 premières grilles).
    Identifie les numéros en commun pour isoler une Grille Maîtresse Prioritaire.
    """
    if len(grilles_brutes) < 2:
        return None
        
    grille_f = set(grilles_brutes[0])
    grille_m = set(grilles_brutes[1])
    
    # Trouver les numéros identiques dans les deux stratégies
    numeros_communs = list(grille_f.intersection(grille_m)) # ex: [1, 20, 30]
    
    # Si on a des numéros communs, on construit la Super-Grille autour
    if len(numeros_communs) > 0:
        super_grille = list(numeros_communs)
        # On complète la grille jusqu'à 5 numéros avec les meilleurs éléments restants de la Fusion
        pour_completer = [n for n in grilles_brutes[0] if n not in super_grille]
        
        while len(super_grille) < 5 and pour_completer:
            super_grille.append(pour_completer.pop(0))
            
        return sorted(super_grille)
    
    return None


# =====================================================================
# PHASE 3 : LE SYSTEME REDUIT (COUVERTURE ET REDUCTION FINALE)
# =====================================================================

def phase_3_optimiser_et_reduire(grilles_filtrees, super_grille, limite_max=2):
    """
    Prend toutes les grilles épurées, place la Super-Grille en tête
    et applique une limite stricte pour réduire drastiquement le coût du joueur.
    """
    grilles_finales = []
    
    # Étape A : On place la Super-Grille en priorité absolue si elle existe
    if super_grille and super_grille not in grilles_finales:
        grilles_finales.append(super_grille)
        
    # Étape B : On ajoute les grilles filtrées par la Sourdine (sans doublons)
    for g in grilles_filtrees:
        if g not in grilles_finales:
            grilles_finales.append(g)
            
    # Étape C : Application du plafond strict (Ex: maximum 2 grilles à jouer)
    return grilles_finales[:limite_max]


# =====================================================================
# POINT D'ENTRÉE : L'ENTREMÊLEMENT DES 3 PHASES
# =====================================================================

if __name__ == "__main__":
    print("--- LANCEMENT DU PROGRAMME LOTO RADAR PRO (OPTIMISÉ) ---")
    
    # 0. Récupération des grilles de ton algorithme actuel
    grilles_initiales = obtenir_grilles_existantes()
    print(f"\n[Initial] Nombre de grilles générées par ton code : {len(grilles_initiales)}")
    print(f"Grilles brutes : {grilles_initiales}")
    
    # 1. Application de la Phase 1 (Sourdine Inversée)
    grilles_epurees = phase_1_sourdine_strict(grilles_initiales)
    print(f"\n[Phase 1] Grilles après filtrage Sourdine Strict : {len(grilles_epurees)}")
    print(f"Grilles restantes : {grilles_epurees}")
    
    # 2. Application de la Phase 2 (Création de la Super-Grille Inter-Axes / Mixte)
    super_grille = phase_2_generer_super_grille(grilles_initiales)
    print(f"\n[Phase 2] Super-Grille Maîtresse calculée : {super_grille}")
    
    # 3. Application de la Phase 3 (Système Réduit à 2 grilles maximum au lieu de 6)
    grilles_finales_a_jouer = phase_3_optimiser_et_reduire(grilles_epurees, super_grille, limite_max=2)
    
    # =====================================================================
    # AFFICHAGE FINAL POUR L'UTILISATEUR
    # =====================================================================
    print("\n==================================================")
    print(f"🎯 CONFIGURATION FINALE : {len(grilles_finales_a_jouer)} GRILLES OPTIMISÉES À JOUER")
    print("==================================================")
    for index, grille in enumerate(grilles_finales_a_jouer, 1):
        print(f" Grille {index} : {grille}")
    print("==================================================")
# =====================================================================
# 7. HISTORIQUE LATÉRAL
# =====================================================================
st.sidebar.header(f"📊 Données {jeu}")
if os.path.exists(FICHIER_ACTIF):
    df_side = pd.read_csv(FICHIER_ACTIF)
    st.sidebar.dataframe(df_side, height=300)
    if st.sidebar.button("🗑️ Vider cette base"):
        os.remove(FICHIER_ACTIF)
        st.rerun()

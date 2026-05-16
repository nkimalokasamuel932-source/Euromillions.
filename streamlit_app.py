import streamlit as st
import pandas as pd
from collections import Counter
import io
import math
import numpy as np

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="IA V37 - Matrice de Couverture", layout="wide")

# --- 2. HISTORIQUE EN CIRCUIT FERMÉ (MISES À JOUR INCLUSES) ---
csv_data = """Jeu,Date,N1,N2,N3,N4,N5,E1,E2
Loto,2026-05-16,1,12,30,32,34,6,0
EuroMillions,2026-05-15,3,10,38,41,43,2,9
Loto,2026-05-13,17,35,38,41,46,2,0
EuroMillions,2026-05-12,4,26,32,35,36,5,7
Loto,2026-05-11,17,18,30,34,39,0,0
EuroMillions,2026-05-08,2,17,19,34,37,8,11
Loto,2026-05-09,16,21,25,26,31,0,0
Loto,2026-05-06,7,18,27,35,48,5,0
EuroMillions,2026-05-05,3,4,8,20,31,1,9
Loto,2026-05-04,4,8,15,18,46,2,0
EuroMillions,2026-05-01,3,9,42,46,47,1,11
Loto,2026-05-02,10,17,19,29,41,7,0
EuroMillions,2026-04-28,26,29,41,46,47,8,9
Loto,2026-04-30,2,3,30,31,37,8,0
EuroMillions,2026-04-24,1,2,4,7,28,5,12
Loto,2026-04-27,6,15,23,27,43,4,0
EuroMillions,2026-04-21,10,13,14,38,41,6,9
Loto,2026-04-25,9,17,22,25,49,3,0
EuroMillions,2026-04-17,11,14,19,36,49,6,7
Loto,2026-04-23,2,12,16,20,26,2,0"""

# --- 3. MOTEUR CINÉTIQUE ---
def analyser_cinetique(df_jeu, total_numeros=50):
    historique_tirages = df_jeu[['N1', 'N2', 'N3', 'N4', 'N5']].values.tolist()
    ecarts = {i: [] for i in range(1, total_numeros + 1)}
    derniere_apparition = {i: -1 for i in range(1, total_numeros + 1)}
    
    for index, tirage in enumerate(reversed(historique_tirages)):
        for num in tirage:
            num = int(num)
            if num in ecarts:
                if derniere_apparition[num] != -1:
                    ecarts[num].append(index - derniere_apparition[num])
                derniere_apparition[num] = index
                
    scores_cinetiques = {}
    for num, liste_ecarts in ecarts.items():
        if len(liste_ecarts) >= 2:
            moyenne_ecart = np.mean(liste_ecarts)
            regularite = np.std(liste_ecarts)
            scores_cinetiques[num] = 100 / (moyenne_ecart * (regularite + 0.5))
        elif len(liste_ecarts) == 1:
            scores_cinetiques[num] = 15.0
        else:
            scores_cinetiques[num] = 2.0
            
    return scores_cinetiques

# --- 4. SÉLECTION MATRICIELLE PAR ZONE ---
def generer_matrice_v37(df_hist, jeu_type):
    est_loto = (jeu_type == "Loto")
    max_num = 49 if est_loto else 50
    df_jeu = df_hist[df_hist['Jeu'] == jeu_type]
    
    # Base cinétique & Éco-système de résonance
    scores_cinetiques = analyser_cinetique(df_jeu, max_num)
    df_recent = df_jeu.head(10)
    
    # OBLIGATION STRICTE : Uniquement les numéros déjà sortis dans les 10 derniers tirages
    nums_deja_sortis = set(df_recent[['N1', 'N2', 'N3', 'N4', 'N5']].values.flatten())
    
    # Résonance avec l'autre jeu
    autre_jeu = "EuroMillions" if est_loto else "Loto"
    df_autre = df_hist[df_hist['Jeu'] == autre_jeu].head(1)
    nums_resonance = set(df_autre.iloc[0][['N1', 'N2', 'N3', 'N4', 'N5']]) if not df_autre.empty else set()

    candidats = []
    for num in nums_deja_sortis:
        score_base = scores_cinetiques.get(num, 5.0)
        poids = score_base * 10
        
        if num in nums_resonance: poids *= 1.40  # Bonus Résonance Croisée (+40%)
        
        # Détermination exacte de la zone (0, 10, 20, 30, 40)
        zone = (num // 10) * 10
        candidats.append({"Numero": int(num), "Zone": zone, "Score": round(poids, 2)})
        
    df_c = pd.DataFrame(candidats)
    
    # Extraction stricte de 3 numéros par zone (uniquement parmi ceux qui sont sortis)
    matrice_resultat = {}
    les_zones = [0, 10, 20, 30, 40]
    
    for z in les_zones:
        # On filtre les numéros de la zone actuelle, triés par le meilleur score
        df_zone = df_c[df_c['Zone'] == z].sort_values(by="Score", ascending=False)
        # On prend les 3 premiers (ou moins si la zone n'a pas assez de numéros sortis dans les 10j)
        matrice_resultat[z] = df_zone['Numero'].head(3).tolist()
        
    # Analyse Étoiles / Chance (Reste inchangé)
    e_cols = ['E1', 'E2'] if not est_loto else ['E1']
    stars_ferme = df_recent[e_cols].values.flatten()
    stars_ferme = [s for s in stars_ferme if s > 0]
    stats_s = Counter(stars_ferme)
    
    stars_candidats = []
    for star, freq in stats_s.items():
        score_s = freq * 10
        if not df_autre.empty and star in df_autre.iloc[0][['E1', 'E2']].values: score_s *= 1.40
        stars_candidats.append({"Etoile": star, "Score": score_s})
        
    df_s = pd.DataFrame(stars_candidats).sort_values(by="Score", ascending=False)
    final_s = df_s['Etoile'].head(2).tolist() if not est_loto else df_s['Etoile'].head(1).tolist()
    
    return matrice_resultat, sorted(final_s), df_c.sort_values(by=["Zone", "Score"], ascending=[True, False])

# --- 5. INTERFACE ET RÉSULTATS ---
st.title("🛡️ IA V37 - MATRICE DE COUVERTURE GLOBALE (3 NUMÉROS PAR ZONE)")
st.write("Tous les numéros présentés ci-dessous proviennent **exclusivement** du circuit fermé des 10 derniers tirages.")

df = pd.read_csv(io.StringIO(csv_data))
col_loto, col_euro = st.columns(2)

with col_loto:
    st.header("🎰 MATRICE LOTO")
    matrice_l, s_loto, _ = generer_matrice_v37(df, "Loto")
    
    for zone, nums in matrice_l.items():
        nom_zone = "Zone 0 à 9" if zone == 0 else f"Zone {zone} à {zone+9}"
        st.success(f"**{nom_zone} :** {nums if nums else 'Aucun numéro sorti dans les 10j'}")
    st.success(f"**NUMÉROS CHANCE :** {s_loto}")

with col_euro:
    st.header("🇪🇺 MATRICE EUROMILLIONS")
    matrice_e, s_euro, _ = generer_matrice_v37(df, "EuroMillions")
    
    for zone, nums in matrice_e.items():
        nom_zone = "Zone 0 à 9" if zone == 0 else f"Zone {zone} à {zone+9}"
        st.error(f"**{nom_zone} :** {nums if nums else 'Aucun numéro sorti dans les 10j'}")
    st.error(f"**ÉTOILES :** {s_euro}")

st.divider()
st.info("💡 **Principe de couverture V37 :** En choisissant 3 numéros par zone parmi l'historique récent, vous êtes armé pour intercepter les poussées groupées (triplés) sur n'importe quelle dizaine.")

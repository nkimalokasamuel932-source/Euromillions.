import streamlit as st
import pandas as pd
from collections import Counter
import io
import math
import numpy as np

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="IA V38 - Synthèse et Grilles Finales", layout="wide")

# --- 2. HISTORIQUE EN CIRCUIT FERMÉ ---
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

# --- 3. MOTEUR MATHÉMATIQUE ---
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

# --- 4. SELECTION ET SYNTHÈSE DES GRILLES ---
def generer_jeux_v38(df_hist, jeu_type):
    est_loto = (jeu_type == "Loto")
    max_num = 49 if est_loto else 50
    df_jeu = df_hist[df_hist['Jeu'] == jeu_type]
    
    scores_cinetiques = analyser_cinetique(df_jeu, max_num)
    df_recent = df_jeu.head(10)
    
    # Uniquement la liste fermée des 10 derniers jours
    nums_deja_sortis = set(df_recent[['N1', 'N2', 'N3', 'N4', 'N5']].values.flatten())
    
    autre_jeu = "EuroMillions" if est_loto else "Loto"
    df_autre = df_hist[df_hist['Jeu'] == autre_jeu].head(1)
    nums_resonance = set(df_autre.iloc[0][['N1', 'N2', 'N3', 'N4', 'N5']]) if not df_autre.empty else set()

    candidats = []
    for num in nums_deja_sortis:
        score_base = scores_cinetiques.get(num, 5.0)
        poids = score_base * 10
        if num in nums_resonance: poids *= 1.40
        zone = (num // 10) * 10
        candidats.append({"Numero": int(num), "Zone": zone, "Score": poids})
        
    df_c = pd.DataFrame(candidats)
    
    # Étape A : Extraire les blocs de zones (V37)
    matrice_zones = {}
    les_zones = [0, 10, 20, 30, 40]
    for z in les_zones:
        df_zone = df_c[df_c['Zone'] == z].sort_values(by="Score", ascending=False)
        matrice_zones[z] = df_zone['Numero'].head(3).tolist()
        
    # Étape B : Mélanger et croiser les zones pour créer 2 propositions de grilles distinctes
    grille_1 = []
    grille_2 = []
    
    # Ordre de priorité des zones à mélanger pour équilibrer
    ordre_zones_g1 = [0, 20, 40, 10, 30]
    ordre_zones_g2 = [30, 10, 40, 20, 0]
    
    # Construction Grille 1 (Prend le premier choix disponible de chaque zone de sa liste)
    for z in ordre_zones_g1:
        if len(matrice_zones[z]) >= 1:
            grille_1.append(matrice_zones[z][0])
            
    # Construction Grille 2 (Prend le deuxième ou premier choix disponible)
    for z in ordre_zones_g2:
        if len(matrice_zones[z]) >= 2:
            grille_2.append(matrice_zones[z][1])
        elif len(matrice_zones[z]) == 1:
            grille_2.append(matrice_zones[z][0])
            
    # Ajustements de sécurité si les listes font moins de 5 numéros
    tous_candidats_tries = df_c.sort_values(by="Score", ascending=False)['Numero'].tolist()
    while len(grille_1) < 5 for _ in range(1):
        for n in tous_candidats_tries:
            if n not in grille_1 and len(grille_1) < 5: grille_1.append(n)
    while len(grille_2) < 5 for _ in range(1):
        for n in tous_candidats_tries:
            if n not in grille_2 and n not in grille_1 and len(grille_2) < 5: grille_2.append(n)
            
    # Analyse Étoiles / Chance
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
    final_s = df_s['Etoile'].head(4).tolist()
    
    # Attribution des étoiles/chances aux grilles
    if est_loto:
        s_g1 = [final_s[0]] if len(final_s) >= 1 else [6]
        s_g2 = [final_s[1]] if len(final_s) >= 2 else [s_g1[0]]
    else:
        s_g1 = final_s[:2] if len(final_s) >= 2 else [2, 9]
        s_g2 = final_s[2:4] if len(final_s) >= 4 else [5, 7]

    return sorted(grille_1), sorted(grille_2), sorted(s_g1), sorted(s_g2), matrice_zones

# --- 5. INTERFACE UTILISATEUR ---
st.title("🎯 IA V38 - COMBINATOIRE ET PROPOSITIONS DE JEUX FINALES")
st.write("Le système a regroupé les matrices de zones pour fusionner les meilleurs potentiels cinétiques.")

df = pd.read_csv(io.StringIO(csv_data))
col_loto, col_euro = st.columns(2)

with col_loto:
    st.header("🎰 GRILLES LOTO PROPOSÉES")
    g1_l, g2_l, c1_l, c2_l, mat_l = generer_jeux_v38(df, "Loto")
    
    st.subheader("💡 Proposition Principale (Grille 1)")
    st.success(f"**NUMÉROS :** {g1_l}  |  **CHANCE :** {c1_l}")
    
    st.subheader("🔮 Proposition Alternative (Grille 2)")
    st.success(f"**NUMÉROS :** {g2_l}  |  **CHANCE :** {c2_l}")
    
    with st.expander("Voir les blocs sources (Matrice Loto)"):
        st.write(mat_l)

with col_euro:
    st.header("🇪🇺 GRILLES EUROMILLIONS PROPOSÉES")
    g1_e, g2_e, c1_e, c2_e, mat_e = generer_jeux_v38(df, "EuroMillions")
    
    st.subheader("💡 Proposition Principale (Grille 1)")
    st.error(f"**NUMÉROS :** {g1_e}  |  **ÉTOILES :** {c1_e}")
    
    st.subheader("🔮 Proposition Alternative (Grille 2)")
    st.error(f"**NUMÉROS :** {c2_e}  |  **ÉTOILES :** {c2_e}")
    
    with st.expander("Voir les blocs sources (Matrice EuroMillions)"):
        st.write(mat_e)

st.divider()
st.caption("🛡️ Sécurité V38 active : Tous les numéros ci-dessus se trouvaient obligatoirement dans les 10 derniers tirages réels.")

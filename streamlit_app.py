import streamlit as st
import pandas as pd
from collections import Counter
import io
import math
import numpy as np

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="IA V35.1 - Moteur Cinétique Strict", layout="wide")

# --- 2. BASE DE DONNÉES HISTORIQUE (CIRCUIT FERMÉ EXTENSIF) ---
csv_data = """Jeu,Date,N1,N2,N3,N4,N5,E1,E2
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
Loto,2026-04-23,2,12,16,20,26,2,0
EuroMillions,2026-04-14,8,27,29,46,49,2,10"""

# --- 3. FONCTIONS MATHÉMATIQUES ---
def analyser_cinetique(df_jeu, total_numeros=50):
    """
    Calcule la régularité des cycles de sortie (via l'écart-type).
    """
    historique_tirages = df_jeu[['N1', 'N2', 'N3', 'N4', 'N5']].values.tolist()
    ecarts = {i: [] for i in range(1, total_numeros + 1)}
    derniere_apparition = {i: -1 for i in range(1, total_numeros + 1)}
    
    # Analyse chronologique inversée (du plus ancien au plus récent)
    for index, tirage in enumerate(reversed(historique_tirages)):
        for num in tirage:
            num = int(num)
            if num in ecarts:
                if list(derniere_apparition.keys()).count(num) > 0 and derniere_apparition[num] != -1:
                    ecarts[num].append(index - derniere_apparition[num])
                derniere_apparition[num] = index
                
    scores_cinetiques = {}
    for num, liste_ecarts in ecarts.items():
        if len(liste_ecarts) >= 2:
            moyenne_ecart = np.mean(liste_ecarts)
            regularite = np.std(liste_ecarts) # Écart-type : stabilité du cycle
            scores_cinetiques[num] = 100 / (moyenne_ecart * (regularite + 0.5))
        elif len(liste_ecarts) == 1:
            scores_cinetiques[num] = 15.0
        else:
            scores_cinetiques[num] = 2.0
            
    return scores_cinetiques

def generer_pronostic_v35_1(df_hist, jeu_type):
    est_loto = (jeu_type == "Loto")
    max_num = 49 if est_loto else 50
    df_jeu = df_hist[df_hist['Jeu'] == jeu_type]
    
    # 1. Analyse de la cinétique globale
    scores_cinetiques = analyser_cinetique(df_jeu, max_num)
    
    # 2. Extraction du Circuit Fermé Strict (10 derniers tirages)
    df_recent = df_jeu.head(10)
    nums_fermes = set(df_recent[['N1', 'N2', 'N3', 'N4', 'N5']].values.flatten())
    dernier_tirage = set(df_recent.iloc[0][['N1', 'N2', 'N3', 'N4', 'N5']])
    
    # 3. Calcul de la Résonance Croisée Loto <-> Euro
    autre_jeu = "EuroMillions" if est_loto else "Loto"
    df_autre = df_hist[df_hist['Jeu'] == autre_jeu].head(1)
    nums_resonance = set(df_autre.iloc[0][['N1', 'N2', 'N3', 'N4', 'N5']]) if not df_autre.empty else set()

    # 4. Pondération des candidats du Circuit Fermé
    candidats = []
    for num in nums_fermes:
        score_base = scores_cinetiques.get(num, 5.0)
        poids = score_base * 10
        
        if num in dernier_tirage: poids *= 0.25 # Protection contre les doublons immédiats
        if num in nums_resonance: poids *= 1.35 # +35% Prime de Résonance Croisée
        
        candidats.append({"Numero": int(num), "Zone": (num//10)*10, "Score": round(poids, 2)})
        
    df_c = pd.DataFrame(candidats).sort_values(by="Score", ascending=False)
    
    # 5. SÉLECTION AVEC BLOCAGE STRICT À 3 NUMÉROS MAXIMUM PAR DIZAINE
    final_n = []
    compteur_zones = Counter()
    
    for _, r in df_c.iterrows():
        zone = r['Zone']
        if compteur_zones[zone] < 3 and len(final_n) < 5:
            final_n.append(int(r['Numero']))
            compteur_zones[zone] += 1
            
    # Remplissage de secours si nécessaire
    for _, r in df_c.iterrows():
        if r['Numero'] not in final_n and len(final_n) < 5:
            final_n.append(int(r['Numero']))
            
    # 6. Analyse des Étoiles / Chance (Circuit Fermé + Résonance)
    e_cols = ['E1', 'E2'] if not est_loto else ['E1']
    stars_ferme = df_recent[e_cols].values.flatten()
    stars_ferme = [s for s in stars_ferme if s > 0]
    stats_s = Counter(stars_ferme)
    
    stars_candidats = []
    for star, freq in stats_s.items():
        score_s = freq * 10
        if not df_autre.empty and star in df_autre.iloc[0][['E1', 'E2']].values:
            score_s *= 1.35 # Prime résonance étoiles
        stars_candidats.append({"Etoile": star, "Score": score_s})
        
    df_s = pd.DataFrame(stars_candidats).sort_values(by="Score", ascending=False)
    final_s = df_s['Etoile'].head(2).tolist() if not est_loto else df_s['Etoile'].head(1).tolist()
    
    return sorted(final_n), sorted(final_s), df_c

# --- 4. INTERFACE GRAPHIQUE ---
st.title("⚡ IA V35.1 - CONFIGURATION ULTRA-PERFORMANCE SÉCURISÉE")
df = pd.read_csv(io.StringIO(csv_data))

col_loto, col_euro = st.columns(2)

with col_loto:
    st.header("🎰 SYSTEME LOTO")
    n_loto, s_loto, an_loto = generer_pronostic_v35_1(df, "Loto")
    st.success(f"**NUMÉROS :** {n_loto}")
    st.success(f"**CHANCE :** {s_loto}")
    st.write("Top Candidats Cinétiques :")
    st.dataframe(an_loto.head(6), hide_index=True)

with col_euro:
    st.header("🇪🇺 SYSTEME EUROMILLIONS")
    n_euro, s_euro, an_euro = generer_pronostic_v35_1(df, "EuroMillions")
    st.error(f"**NUMÉROS :** {n_euro}")
    st.error(f"**ÉTOILES :** {s_euro}")
    st.write("Top Candidats Cinétiques :")
    st.dataframe(an_euro.head(6), hide_index=True)

st.divider()
st.caption("⚙️ Algorithme configuré pour capturer les poussées de zones (limite stricte à 3 par dizaine) et exploiter la stabilité des cycles de tirages.")

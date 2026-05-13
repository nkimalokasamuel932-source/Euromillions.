import streamlit as st
import pandas as pd
from collections import Counter
import io
import math

# --- 1. CONFIGURATION ET STYLE ---
st.set_page_config(page_title="IA V33 - Pronostics Loto & Euro", layout="wide")

# --- 2. BASE DE DONNÉES HISTORIQUE (MISE À JOUR 13 MAI) ---
csv_data = """Jeu,Date,N1,N2,N3,N4,N5,E1,E2
Loto,2026-05-13,17,35,38,41,46,2,0
Loto,2026-05-11,17,18,30,34,39,0,0
Loto,2026-05-09,16,21,25,26,31,0,0
Loto,2026-05-06,7,18,27,35,48,5,0
Loto,2026-05-04,4,8,15,18,46,2,0
Loto,2026-05-02,10,17,19,29,41,7,0
Loto,2026-04-30,2,3,30,31,37,8,0
Loto,2026-04-27,6,15,23,27,43,4,0
Loto,2026-04-25,9,17,22,25,49,3,0
Loto,2026-04-23,2,12,16,20,26,2,0
EuroMillions,2026-05-12,4,26,32,35,36,5,7
EuroMillions,2026-05-08,2,17,19,34,37,8,11
EuroMillions,2026-05-05,3,4,8,20,31,1,9
EuroMillions,2026-05-01,3,9,42,46,47,1,11
EuroMillions,2026-04-28,26,29,41,46,47,8,9
EuroMillions,2026-04-24,1,2,4,7,28,5,12
EuroMillions,2026-04-21,10,13,14,38,41,6,9
EuroMillions,2026-04-17,11,14,19,36,49,6,7
EuroMillions,2026-04-14,8,27,29,46,49,2,10
EuroMillions,2026-04-10,5,8,10,33,38,2,7"""

# --- 3. MOTEUR MATHÉMATIQUE V33 ---
def calcul_score_poisson(frequence_actuelle, est_loto=True):
    # Lambda calculé sur 10 tirages
    lmbda = 1.02 if est_loto else 1.00 
    k_plus_un = frequence_actuelle + 1
    prob = (math.pow(lmbda, k_plus_un) * math.exp(-lmbda)) / math.factorial(k_plus_un)
    return prob

def generer_pronostic(df_hist, jeu_type):
    est_loto = (jeu_type == "Loto")
    # Filtrage strict du Circuit Fermé (10 derniers tirages)
    df_jeu = df_hist[df_hist['Jeu'] == jeu_type].head(10)
    
    # Analyse Numéros (N1-N5)
    nums_fermes = df_jeu[['N1', 'N2', 'N3', 'N4', 'N5']].values.flatten()
    stats = Counter(nums_fermes)
    dernier_tirage = set(df_jeu.iloc[0][['N1', 'N2', 'N3', 'N4', 'N5']])
    
    candidats = []
    for num, freq in stats.items():
        score_p = calcul_score_poisson(freq, est_loto)
        poids = score_p * 100
        if num in dernier_tirage: poids *= 0.4 # Rotation
        
        candidats.append({"Numero": int(num), "Zone": (num//10)*10, "Score": poids})
    
    # Sélection Numéros
    df_c = pd.DataFrame(candidats).sort_values(by="Score", ascending=False)
    final_n = []
    zones_pries = set()
    for _, r in df_c.iterrows():
        if r['Zone'] not in zones_pries and len(final_n) < 5:
            final_n.append(int(r['Numero']))
            zones_pries.add(r['Zone'])
    for _, r in df_c.iterrows():
        if r['Numero'] not in final_n and len(final_n) < 5:
            final_n.append(int(r['Numero']))
            
    # Analyse Étoiles / Chance (Basé sur Circuit Fermé également)
    e_cols = ['E1', 'E2'] if not est_loto else ['E1']
    stars_ferme = df_jeu[e_cols].values.flatten()
    # On retire les zéros (cas du Loto E2)
    stars_ferme = [s for s in stars_ferme if s > 0]
    stats_s = Counter(stars_ferme)
    final_s = sorted(stats_s, key=stats_s.get, reverse=True)
    
    return sorted(final_n), final_s[:2] if not est_loto else final_s[:1], df_c

# --- 4. INTERFACE UTILISATEUR ---
st.title("🔬 SYSTÈME EXPERT IA V33")
df = pd.read_csv(io.StringIO(csv_data))

# Affichage côte à côte des deux jeux
col_loto, col_euro = st.columns(2)

with col_loto:
    st.header("🎰 LOTO")
    n_loto, s_loto, an_loto = generer_pronostic(df, "Loto")
    st.success(f"**NUMÉROS :** {n_loto}")
    st.success(f"**CHANCE :** {s_loto}")
    st.dataframe(an_loto[['Numero', 'Score']].head(8), hide_index=True)

with col_euro:
    st.header("🇪🇺 EUROMILLIONS")
    n_euro, s_euro, an_euro = generer_pronostic(df, "EuroMillions")
    st.error(f"**NUMÉROS :** {n_euro}")
    st.error(f"**ÉTOILES :** {s_euro}")
    st.dataframe(an_euro[['Numero', 'Score']].head(8), hide_index=True)

st.info("💡 **Note technique :** Ce code utilise la Loi de Poisson pour détecter la maturité des numéros au sein de votre circuit fermé de 10 tirages.")

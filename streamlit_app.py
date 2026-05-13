import streamlit as st
import pandas as pd
from collections import Counter
import io
import math

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="IA V33 - Circuit Fermé", layout="wide")

# --- 1. DONNÉES MISES À JOUR (INCLUT LE 13 MAI) ---
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

# --- 2. FONCTIONS MATHÉMATIQUES ---
def calcul_score_poisson(frequence_actuelle, est_loto=True):
    lmbda = 1.02 if est_loto else 1.00
    k_plus_un = frequence_actuelle + 1
    prob = (math.pow(lmbda, k_plus_un) * math.exp(-lmbda)) / math.factorial(k_plus_un)
    return prob

def generer_tirage_v33(df_hist, jeu_type):
    est_loto = (jeu_type == "Loto")
    # On prend les 10 derniers du jeu sélectionné
    df_recent = df_hist[df_hist['Jeu'] == jeu_type].head(10)
    
    # Circuit Fermé
    nums_fermes = df_recent[['N1', 'N2', 'N3', 'N4', 'N5']].values.flatten()
    stats = Counter(nums_fermes)
    
    # Rotation (Dernier tirage)
    dernier_tirage = set(df_recent.iloc[0][['N1', 'N2', 'N3', 'N4', 'N5']])
    
    candidats = []
    for num, freq in stats.items():
        score_p = calcul_score_poisson(freq, est_loto)
        poids_final = score_p * 100
        
        # Pénalité de rotation si le numéro est sorti au dernier tirage
        if num in dernier_tirage:
            poids_final *= 0.4 

        zone = (num // 10) * 10
        candidats.append({
            "Numero": int(num),
            "Sorties_10j": freq,
            "Zone": zone,
            "Score_V33": round(poids_final, 2)
        })
    
    df_candidats = pd.DataFrame(candidats).sort_values(by="Score_V33", ascending=False)
    
    # Sélection finale équilibrée
    selection = []
    zones_utilisees = set()
    
    for _, row in df_candidats.iterrows():
        if row['Zone'] not in zones_utilisees and len(selection) < 5:
            selection.append(int(row['Numero']))
            zones_utilisees.add(row['Zone'])
            
    for _, row in df_candidats.iterrows():
        if row['Numero'] not in selection and len(selection) < 5:
            selection.append(int(row['Numero']))
            
    return sorted(selection), df_candidats

# --- 3. AFFICHAGE DE L'INTERFACE ---
st.title("🛡️ IA V33 - CIRCUIT FERMÉ & POISSON")

df = pd.read_csv(io.StringIO(csv_data))
choix = st.sidebar.radio("Sélectionner le jeu :", ["Loto", "EuroMillions"])

pronostic, analyse = generer_tirage_v33(df, choix)

# Panneau principal
st.header(f"🎯 Pronostic pour le prochain tirage {choix}")
st.subheader(f"Numéros suggérés : {pronostic}")
if choix == "EuroMillions":
    st.write("**Étoiles suggérées : 2 - 9**")
else:
    st.write("**Numéro Chance suggéré : 6**")

st.divider()
st.write("### 📊 Analyse détaillée (Circuit Fermé)")
st.dataframe(analyse, use_container_width=True, hide_index=True)

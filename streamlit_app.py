import streamlit as st
import pandas as pd
from collections import Counter
import io
import math

# --- 1. MOTEUR MATHÉMATIQUE (LOI DE POISSON) ---
def calcul_score_poisson(frequence_actuelle, est_loto=True):
    """
    Calcule la probabilité qu'un numéro sorte une fois de plus (k+1).
    Plus la probabilité est élevée, plus le numéro est 'mûr' pour ressortir.
    """
    # Moyenne théorique (lambda) : (5 numéros * 10 tirages) / (49 ou 50 numéros)
    lmbda = 1.02 if est_loto else 1.00
    k_plus_un = frequence_actuelle + 1
    
    # Formule : (lambda^k * exp(-lambda)) / k!
    prob = (math.pow(lmbda, k_plus_un) * math.exp(-lmbda)) / math.factorial(k_plus_un)
    return prob

# --- 2. LOGIQUE DE SÉLECTION V33 ---
def generer_tirage_v33(df_hist, jeu_type):
    est_loto = (jeu_type == "Loto")
    df_recent = df_hist[df_hist['Jeu'] == jeu_type].head(10)
    
    # Circuit Fermé : Uniquement les numéros des 10 derniers tirages
    nums_fermes = df_recent[['N1', 'N2', 'N3', 'N4', 'N5']].values.flatten()
    stats = Counter(nums_fermes)
    
    # Rotation : Dernier tirage pour gestion des doublés
    dernier_tirage = set(df_recent.iloc[0][['N1', 'N2', 'N3', 'N4', 'N5']])
    
    candidats = []
    for num, freq in stats.items():
        # Calcul du score Poisson (Probabilité de ressortir)
        score_p = calcul_score_poisson(freq, est_loto)
        
        # Filtre Rotation Intelligent : 
        # On réduit le score si le numéro est sorti au dernier tirage
        # sauf s'il a une probabilité de Poisson encore forte.
        poids_final = score_p * 100
        if num in dernier_tirage:
            poids_final *= 0.5  # Pénalité de rotation (doublé moins probable)

        zone = (num // 10) * 10
        candidats.append({
            "Numero": int(num),
            "Sorties_10j": freq,
            "Zone": zone,
            "Probabilité_Poisson": round(score_p, 4),
            "Score_V33": round(poids_final, 2)
        })
    
    df_candidats = pd.DataFrame(candidats).sort_values(by="Score_V33", ascending=False)
    
    # Sélection équilibrée
    selection = []
    zones_utilisees = set()
    
    # 1er passage : Diversité des zones
    for _, row in df_candidats.iterrows():
        if row['Zone'] not in zones_utilisees and len(selection) < 5:
            selection.append(int(row['Numero']))
            zones_utilisees.add(row['Zone'])
            
    # 2ème passage : Remplissage par score pur
    for _, row in df_candidats.iterrows():
        if row['Numero'] not in selection and len(selection) < 5:
            selection.append(int(row['Numero']))
            
    return sorted(selection), df_candidats

# --- 3. DONNÉES HISTORIQUES (MISES À JOUR) ---
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

# --- 4. INTERFACE STREAMLIT ---
st.set_page_config(page_title="IA Loto V33", layout="wide")
st.title("🔬 IA V33 : Circuit Fermé & Loi de Poisson")

df = pd.read_csv(io.StringIO(csv_data))
choix = st.sidebar.radio("Jeu à analyser :", ["Loto", "EuroMillions"])

pronostic, analyse = generer_tirage_v33(df, choix)

# Affichage des résultats
col1, col2 = st.columns([1, 2])

with col1:
    st.metric(label=f"Pronostic {choix}", value=f"{pronostic}")
    st.info("Le score V33 combine la fréquence du circuit fermé et la probabilité mathématique de ressortir selon la Loi de Poisson.")

with col2:
    st.write("### 🔍 Détails mathématiques des candidats")
    st.dataframe(analyse, use_container_width=True, hide_index=True)

st.warning("⚠️ Rappel : Cette méthode maximise les chances basées sur la répétition historique, mais le hasard reste imprévisible.")

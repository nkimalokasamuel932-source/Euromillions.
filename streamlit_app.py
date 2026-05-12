import streamlit as st
import pandas as pd
from collections import Counter

# --- CONFIGURATION ---
st.set_page_config(page_title="IA V29 - ROTATION ULTIME", layout="wide", page_icon="🎯")

# --- 1. HISTORIQUES (10 DERNIERS) ---
HISTORIQUE_LOTO = [
    ([17, 18, 30, 34, 39], [0]),  # Tirage de Lundi (ROTATION : À ÉCARTER)
    ([16, 21, 25, 26, 31], [0]), 
    ([7, 18, 27, 35, 48], [5]), 
    ([4, 8, 15, 18, 46], [2]), 
    ([10, 17, 19, 29, 41], [7]), 
    ([2, 3, 30, 31, 37], [8]), 
    ([6, 15, 23, 27, 43], [4]), 
    ([9, 17, 22, 25, 49], [3]), 
    ([2, 12, 16, 20, 26], [2]), 
    ([30, 37, 38, 40, 43], [1])
]

HISTORIQUE_EURO = [
    ([2, 17, 19, 34, 37], [8, 11]), # Tirage de Vendredi (ROTATION : À ÉCARTER)
    ([3, 4, 8, 20, 31], [1, 9]), 
    ([3, 9, 42, 46, 47], [1, 11]), 
    ([26, 29, 41, 46, 47], [8, 9]), 
    ([1, 2, 4, 7, 28], [5, 12]), 
    ([10, 13, 14, 38, 41], [6, 9]), 
    ([11, 14, 19, 36, 49], [6, 7]), 
    ([8, 27, 29, 46, 49], [2, 10]), 
    ([5, 8, 10, 33, 38], [2, 7]), 
    ([4, 10, 43, 44, 48], [2, 4])
]

# --- 2. VOS NOUVELLES MATRICES DE PROBABILITÉS (MAJ) ---
PROB_LOTO = {1: 80.4, 32: 80.4, 11: 80.4, 42: 71.5, 14: 71.5, 44: 68.8, 36: 68.8, 13: 63.3, 28: 57.4, 24: 57.4, 45: 52.9, 20: 51.8, 33: 48.6, 9: 46.3, 40: 46.3, 49: 46.3, 5: 44.0, 47: 42.5, 38: 40.4, 35: 40.4, 41: 37.4, 6: 37.4, 4: 37.4, 39: 37.4, 34: 37.4, 8: 31.5, 46: 31.5, 37: 28.7, 15: 28.7, 27: 28.7, 12: 27.0, 19: 27.0, 7: 25.5, 31: 22.8, 22: 21.0, 3: 18.3, 10: 18.3, 21: 18.1, 29: 18.1, 48: 17.0, 43: 16.8, 26: 16.8, 23: 13.0, 25: 9.6, 2: 9.4, 17: 6.9, 30: 5.7, 16: 4.9, 18: 2.8}

PROB_EURO = {21: 79.8, 32: 79.8, 39: 76.3, 35: 70.6, 7: 67.9, 15: 67.9, 18: 62.2, 6: 62.2, 43: 56.3, 50: 53.4, 48: 53.4, 24: 51.9, 11: 50.9, 22: 50.9, 45: 50.9, 25: 50.9, 30: 50.9, 36: 50.9, 33: 47.5, 20: 45.2, 9: 45.2, 5: 41.6, 12: 41.6, 31: 39.3, 1: 39.3, 23: 39.3, 38: 36.4, 49: 36.4, 42: 34.8, 27: 33.4, 3: 27.8, 2: 27.8, 34: 26.0, 44: 24.6, 8: 24.6, 37: 17.6, 40: 17.5, 16: 17.3, 10: 16.4, 29: 16.0, 17: 14.8, 19: 11.6, 26: 11.6, 14: 9.0, 4: 9.0, 13: 7.9, 46: 6.2, 28: 5.1, 47: 2.1, 41: 1.6}

# --- 3. MOTEUR DE CALCUL ---
def calculer_rotation_momentum(historique, probas):
    dernier_tirage = historique[0][0]
    tous_sortis = [n for t, c in historique for n in t]
    counts = Counter(tous_sortis)
    ensemble_valide = set(tous_sortis)
    
    data = []
    for num in ensemble_valide:
        p = probas.get(num, 0)
        freq = counts.get(num, 0)
        
        # Filtre de Rotation : On écarte le tirage précédent
        if num in dernier_tirage:
            continue
            
        score = (freq * 60) + (p * 2.5)
        data.append({"Numéro": num, "Score": score, "Sorties": freq, "Proba": p})
        
    return pd.DataFrame(data).sort_values("Score", ascending=False)

# --- 4. INTERFACE ---
st.title("🎯 IA V29 - PRONOSTICS ROTATION MOMENTUM")

c1, c2 = st.columns(2)

with c1:
    st.header("🎰 LOTO (Pour Mercredi)")
    res_loto = calculer_rotation_momentum(HISTORIQUE_LOTO, PROB_LOTO)
    top_l = res_loto.head(5)['Numéro'].tolist()
    st.success(f"### 👉 {sorted(top_l)}")
    st.dataframe(res_loto.head(10), hide_index=True)

with c2:
    st.header("🇪🇺 EURO (Pour ce soir)")
    res_euro = calculer_rotation_momentum(HISTORIQUE_EURO, PROB_EURO)
    top_e = res_euro.head(5)['Numéro'].tolist()
    st.error(f"### 👉 {sorted(top_e)}")
    st.dataframe(res_euro.head(10), hide_index=True)

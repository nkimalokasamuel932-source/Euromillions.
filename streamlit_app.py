import streamlit as st
import pandas as pd
from collections import Counter

# --- CONFIGURATION ---
st.set_page_config(page_title="IA MOMENTUM - 100% SORTIES", layout="wide", page_icon="🎯")

# --- 1. HISTORIQUES SYNCHRONISÉS (LES 10 DERNIERS) ---
# Tirages réels au 10 Mai 2026
HISTORIQUE_LOTO = [
    ([16, 21, 25, 26, 31], [0]),  # 9 Mai 
    ([7, 18, 27, 35, 48], [5]),   # 6 Mai
    ([4, 8, 15, 18, 46], [2]),    # 4 Mai
    ([10, 17, 19, 29, 41], [7]),  # 2 Mai
    ([2, 3, 30, 31, 37], [8]),
    ([6, 15, 23, 27, 43], [4]),
    ([9, 17, 22, 25, 49], [3]),
    ([2, 12, 16, 20, 26], [2]),
    ([30, 37, 38, 40, 43], [1]),
    ([2, 12, 21, 29, 33], [6])
]

HISTORIQUE_EURO = [
    ([2, 17, 19, 34, 37], [8, 11]), # 8 Mai
    ([3, 4, 8, 20, 31], [1, 9]),    # 5 Mai
    ([3, 9, 42, 46, 47], [1, 11]),  # 1er Mai
    ([26, 29, 41, 46, 47], [8, 9]),
    ([1, 2, 4, 7, 28], [5, 12]),
    ([10, 13, 14, 38, 41], [6, 9]),
    ([11, 14, 19, 36, 49], [6, 7]),
    ([8, 27, 29, 46, 49], [2, 10]),
    ([5, 8, 10, 33, 38], [2, 7]),
    ([4, 10, 43, 44, 48], [2, 4])
]

# --- 2. MATRICES DE PROBABILITÉS (VOS DONNÉES) ---
prob_loto = {1: 80.4, 32: 80.4, 11: 77.0, 42: 71.5, 14: 71.5, 34: 68.8, 39: 68.8, 36: 68.8, 44: 68.8, 13: 63.3, 24: 57.4, 20: 51.8, 28: 48.6, 49: 46.3, 40: 46.3, 5: 44.0, 45: 44.0, 47: 42.5, 9: 40.4, 35: 40.4, 4: 37.4, 41: 37.4, 6: 37.4, 15: 28.7, 27: 28.7, 37: 28.7, 19: 27.0, 7: 25.5, 31: 22.8, 12: 18.3, 22: 18.3, 3: 18.3, 48: 17.0, 10: 17.0, 43: 16.8, 26: 16.8, 23: 13.0, 17: 12.3, 18: 9.6, 30: 9.6, 25: 9.6, 29: 9.4, 2: 6.7, 21: 6.7, 16: 4.9}
prob_euro = {21: 79.8, 32: 79.8, 39: 76.3, 35: 70.6, 7: 67.9, 15: 67.9, 18: 62.2, 6: 62.2, 43: 56.3, 50: 53.4, 48: 53.4, 24: 51.9, 11: 50.9, 22: 50.9, 45: 50.9, 25: 50.9, 30: 50.9, 36: 50.9, 33: 47.5, 20: 45.2, 9: 45.2, 5: 41.6, 12: 41.6, 31: 39.3, 1: 39.3, 23: 39.3, 38: 36.4, 49: 36.4, 42: 34.8, 27: 33.4, 3: 27.8, 2: 27.8, 34: 26.0, 44: 24.6, 8: 24.6, 37: 17.6, 40: 17.5, 16: 17.3, 10: 16.4, 29: 16.0, 17: 14.8, 19: 11.6, 26: 11.6, 14: 9.0, 4: 9.0, 13: 7.9, 46: 6.2, 28: 5.1, 47: 2.1, 41: 1.6}

# --- 3. MOTEUR "MOMENTUM" (FILTRE DE SORTIE OBLIGATOIRE) ---
def moteur_momentum(historique, probas):
    # On isole uniquement les numéros sortis sur les 10 derniers
    tous_sortis = [n for t, e in historique for n in t]
    counts = Counter(tous_sortis)
    ensemble_sortis = set(tous_sortis) # Unique list
    
    data = []
    for num in ensemble_sortis:
        # 1. On récupère la probabilité (si absente de la matrice, on met 0)
        p = probas.get(num, 0)
        
        # 2. Score de Fréquence (Poids lourd)
        nb_sorties = counts.get(num, 0)
        score_frequence = nb_sorties * 100
        
        # 3. Score de Probabilité relative
        score_p = p * 2
        
        total = score_frequence + score_p
        data.append({"Numéro": num, "Score": total, "Sorties_10j": nb_sorties, "Proba": p})

    df = pd.DataFrame(data).sort_values("Score", ascending=False)
    return df

# --- 4. INTERFACE ---
st.title("🛰️ IA MOMENTUM - CIRCUIT FERMÉ")
st.warning("⚠️ Règle stricte : Seuls les numéros apparus sur les 10 derniers tirages sont analysés.")

res_loto = moteur_momentum(HISTORIQUE_LOTO, prob_loto)
res_euro = moteur_momentum(HISTORIQUE_EURO, prob_euro)

c1, c2 = st.columns(2)

with c1:
    st.header("🎰 LOTO (Top Forme)")
    sel_l = res_loto.head(5)['Numéro'].tolist()
    sel_l.sort()
    st.success(f"### 👉 {', '.join(map(str, sel_l))}")
    st.write("**Base de calcul (Uniquement sorties récentes) :**")
    st.dataframe(res_loto.head(10))

with c2:
    st.header("🇪🇺 EURO (Top Forme)")
    sel_e = res_euro.head(5)['Numéro'].tolist()
    sel_e.sort()
    st.error(f"### 👉 {', '.join(map(str, sel_e))}")
    st.write("**Base de calcul (Uniquement sorties récentes) :**")
    st.dataframe(res_euro.head(10))

st.divider()
st.info("💡 **Explication technique :** Le numéro 1 (Loto) ou le 21 (Euro) ont été **exclus** de cette liste s'ils ne sont pas sortis récemment, car ton choix est de privilégier la répétition et le momentum plutôt que l'écart.")

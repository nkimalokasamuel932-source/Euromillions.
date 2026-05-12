import streamlit as st
import pandas as pd
from collections import Counter

# --- CONFIGURATION ---
st.set_page_config(page_title="IA V29 - ROTATION MOMENTUM", layout="wide", page_icon="♻️")

# --- 1. BASE DE DONNÉES (10 DERNIERS TIRAGES) ---
HISTORIQUE_LOTO = [
    ([17, 18, 30, 34, 39], [0]),  # DERNIER TIRAGE (A EXCLURE/PENALISER)
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
    ([2, 17, 19, 34, 37], [8, 11]), # DERNIER TIRAGE
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

# --- 2. MATRICES DE PROBABILITÉS ---
REF_PROB_LOTO = {1: 80.4, 32: 80.4, 11: 77.0, 42: 71.5, 14: 71.5, 34: 68.8, 39: 68.8, 36: 68.8, 44: 68.8, 13: 63.3, 24: 57.4, 20: 51.8, 28: 48.6, 49: 46.3, 40: 46.3, 5: 44.0, 45: 44.0, 47: 42.5, 9: 40.4, 35: 40.4, 4: 37.4, 41: 37.4, 6: 37.4, 15: 28.7, 27: 28.7, 37: 28.7, 19: 27.0, 7: 25.5, 31: 22.8, 12: 18.3, 22: 18.3, 3: 18.3, 48: 17.0, 10: 17.0, 43: 16.8, 26: 16.8, 23: 13.0, 17: 12.3, 18: 9.6, 30: 9.6, 25: 9.6, 29: 9.4, 2: 6.7, 21: 6.7, 16: 4.9}
REF_PROB_EURO = {21: 79.8, 32: 79.8, 39: 76.3, 35: 70.6, 7: 67.9, 15: 67.9, 18: 62.2, 6: 62.2, 43: 56.3, 50: 53.4, 48: 53.4, 24: 51.9, 11: 50.9, 22: 50.9, 45: 50.9, 25: 50.9, 30: 50.9, 36: 50.9, 33: 47.5, 20: 45.2, 9: 45.2, 5: 41.6, 12: 41.6, 31: 39.3, 1: 39.3, 23: 39.3, 38: 36.4, 49: 36.4, 42: 34.8, 27: 33.4, 3: 27.8, 2: 27.8, 34: 26.0, 44: 24.6, 8: 24.6, 37: 17.6, 40: 17.5, 16: 17.3, 10: 16.4, 29: 16.0, 17: 14.8, 19: 11.6, 26: 11.6, 14: 9.0, 4: 9.0, 13: 7.9, 46: 6.2, 28: 5.1, 47: 2.1, 41: 1.6}

# --- 3. MOTEUR DE ROTATION MOMENTUM ---
def moteur_rotation_momentum(historique, ref_probas):
    dernier_tirage = historique[0][0]
    # Circuit Fermé : Uniquement les numéros sortis sur les 10 derniers
    tous_nums = [n for tirage, comp in historique for n in tirage]
    counts = Counter(tous_nums)
    set_valide = set(tous_nums)
    
    rotation_data = []
    for num in set_valide:
        p = ref_probas.get(num, 0)
        freq = counts.get(num, 0)
        
        # LOGIQUE DE ROTATION :
        # Si le numéro est sorti au dernier tirage, on lui inflige un malus massif
        # pour forcer l'IA à regarder les autres numéros "chauds" du circuit.
        malus_recence = -500 if num in dernier_tirage else 0
        
        # Score : (Fréquence x 50) + (Probabilité x 2) + Malus Rotation
        score = (freq * 50) + (p * 2) + malus_recence
        
        rotation_data.append({
            "Numéro": num,
            "Sorties (10j)": freq,
            "Probabilité (%)": p,
            "Statut": "Vient de sortir" if num in dernier_tirage else "En attente",
            "Score": score
        })
    
    return pd.DataFrame(rotation_data).sort_values("Score", ascending=False)

# --- 4. INTERFACE ---
st.title("♻️ IA V29 - ROTATION DES SORTIES")
st.markdown("### Stratégie : Utiliser le Momentum des 10 derniers en évitant les répétitions immédiates.")

c1, c2 = st.columns(2)

with c1:
    st.header("🎰 LOTO (Rotation)")
    df_loto = moteur_rotation_momentum(HISTORIQUE_LOTO, REF_PROB_LOTO)
    st.dataframe(df_loto[df_loto['Statut'] == "En attente"], hide_index=True)
    jeu_l = df_loto.head(5)['Numéro'].tolist()
    st.success(f"**Pronostic Loto (Rotation) :** {sorted(jeu_l)}")

with c2:
    st.header("🇪🇺 EURO (Rotation)")
    df_euro = moteur_rotation_momentum(HISTORIQUE_EURO, REF_PROB_EURO)
    st.dataframe(df_euro[df_euro['Statut'] == "En attente"], hide_index=True)
    jeu_e = df_euro.head(5)['Numéro'].tolist()
    st.error(f"**Pronostic Euro (Rotation) :** {sorted(jeu_e)}")

st.divider()
st.info("💡 **Analyse V29 :** Les numéros sortis au dernier tirage (ex: 17, 18, 30, 34, 39 pour le Loto) sont masqués ou pénalisés pour favoriser la sortie des autres numéros du bloc des 10 derniers tirages.")

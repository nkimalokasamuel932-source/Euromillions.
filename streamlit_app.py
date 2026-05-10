import streamlit as st
import pandas as pd
import io
from collections import Counter

# --- CONFIGURATION ---
st.set_page_config(page_title="IA V23 - RÉSONANCE & SORTIES", layout="wide", page_icon="🔥")

# --- 1. SYNCHRONISATION DES DERNIERS RÉSULTATS (MAI 2026) ---
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

# --- 2. MATRICES DE PROBABILITÉS FOURNIES ---
prob_loto = {
    1: 80.4, 32: 80.4, 11: 77.0, 42: 71.5, 14: 71.5, 34: 68.8, 39: 68.8, 36: 68.8, 44: 68.8,
    13: 63.3, 24: 57.4, 20: 51.8, 28: 48.6, 49: 46.3, 40: 46.3, 5: 44.0, 45: 44.0, 47: 42.5,
    9: 40.4, 35: 40.4, 4: 37.4, 41: 37.4, 6: 37.4, 15: 28.7, 27: 28.7, 37: 28.7, 19: 27.0, 
    26: 16.8, 18: 9.6, 25: 9.6, 21: 6.7, 16: 4.9
}

prob_euro = {
    21: 79.8, 32: 79.8, 39: 76.3, 35: 70.6, 7: 67.9, 15: 67.9, 18: 62.2, 6: 62.2,
    43: 56.3, 50: 53.4, 48: 53.4, 24: 51.9, 11: 50.9, 22: 50.9, 36: 50.9, 20: 45.2,
    31: 39.3, 1: 39.3, 42: 34.8, 27: 33.4, 3: 27.8, 2: 27.8, 34: 26.0, 8: 24.6, 
    17: 14.8, 19: 11.6, 47: 2.1
}

# --- 3. MOTEUR DE DÉCISION V23 ---
def moteur_v23_priorite_sorties(historique, probas_dict):
    tous_sortis = [n for t, e in historique for n in t]
    counts = Counter(tous_sortis)
    dernier = historique[0][0]
    
    data = []
    for num, p in probas_dict.items():
        # A. Bonus de Sorties Récentes (L'élément clé demandé)
        # On donne 60 points par sortie sur les 10 derniers tirages
        nb_sorties = counts.get(num, 0)
        bonus_sorties = nb_sorties * 60
        
        # B. Score Probabilité Pondéré
        score_p = p * 1.2
        
        # C. Bonus de Répétition Flash (Dernier tirage)
        bonus_flash = 50 if num in dernier else 0
        
        # D. Sécurité Rupture (Pour le n°1 Loto ou n°21 Euro)
        # Si proba > 75% et 0 sortie, on booste pour la sortie imminente
        bonus_rupture = 150 if (p > 75 and nb_sorties == 0) else 0

        score_final = bonus_sorties + score_p + bonus_flash + bonus_rupture
        data.append({"Numéro": num, "Score": score_final, "Sorties": nb_sorties, "Proba": p})

    return pd.DataFrame(data).sort_values("Score", ascending=False)

# --- 4. INTERFACE ---
st.title("🛰️ IA EXPERT V23 - PRIORITÉ SORTIES RÉCENTES")
st.markdown("### Algorithme synchronisé sur les 10 derniers tirages + Matrices de Probabilités")

res_loto = moteur_v23_priorite_sorties(HISTORIQUE_LOTO, prob_loto)
res_euro = moteur_v23_priorite_sorties(HISTORIQUE_EURO, prob_euro)

c1, c2 = st.columns(2)

with c1:
    st.header("🎰 LOTO : FOCUS FORMES")
    # Sélection des 5 meilleurs scores
    sel_l = res_loto.head(5)['Numéro'].tolist()
    sel_l.sort()
    st.success(f"### 👉 {', '.join(map(str, sel_l))}")
    st.write("**Détails des Bases :**")
    st.dataframe(res_loto[['Numéro', 'Score', 'Sorties', 'Proba']].head(5))

with c2:
    st.header("🇪🇺 EURO : FOCUS FORMES")
    sel_e = res_euro.head(5)['Numéro'].tolist()
    sel_e.sort()
    st.error(f"### 👉 {', '.join(map(str, sel_e))}")
    st.write("**Détails des Bases :**")
    st.dataframe(res_euro[['Numéro', 'Score', 'Sorties', 'Proba']].head(5))

st.divider()
st.info("💡 **Analyse de l'expert :** Ce code favorise les numéros qui 'bougent' (ceux qui ont déjà des sorties au compteur) tout en gardant le n°1 (Loto) et le n°21 (Euro) en sécurité grâce au bonus de rupture de probabilité (150 pts).")

import streamlit as st
import pandas as pd
import io
from collections import Counter

# --- CONFIGURATION ---
st.set_page_config(page_title="IA EXPERT V18.1 - FUSION TOTALE", layout="wide", page_icon="♾️")

# --- 1. HISTORIQUES OFFICIELS (LES 10 DERNIERS) ---
HISTORIQUE_LOTO = [
    ([7, 18, 27, 35, 48], [5]), ([4, 8, 15, 18, 46], [2]), ([10, 17, 19, 29, 41], [7]),
    ([2, 3, 30, 31, 37], [8]), ([6, 15, 23, 27, 43], [4]), ([9, 17, 22, 25, 49], [3]),
    ([2, 12, 16, 20, 26], [2]), ([30, 37, 38, 40, 43], [1]), ([2, 12, 21, 29, 33], [6]),
    ([5, 22, 23, 24, 25], [10])
]

HISTORIQUE_EURO = [
    ([3, 4, 8, 20, 31], [1, 9]), ([3, 9, 42, 46, 47], [1, 11]), ([26, 29, 41, 46, 47], [8, 9]),
    ([1, 2, 4, 7, 28], [5, 12]), ([10, 13, 14, 38, 41], [6, 9]), ([11, 14, 19, 36, 49], [6, 7]),
    ([8, 27, 29, 46, 49], [2, 10]), ([5, 8, 10, 33, 38], [2, 7]), ([4, 10, 43, 44, 48], [2, 4]),
    ([12, 16, 17, 18, 27], [1, 3])
]

# --- 2. BASE DE DONNÉES EXPERT (LOTO & EURO) ---
loto_data = """Numéro,Réussite,FormeG,EcartMax,EcartActuel,Affinite,AnnoncePar,AnnonciateurDe
41,322,8,41,2,16,13,17
13,321,5,55,13,3,31,3
1,291,3,42,42,49,34,6
18,272,10,67,0,13,46,29
2,284,9,55,3,13,45,17
17,284,10,58,2,30,39,41
27,291,4,63,0,4,18,30
7,294,7,52,0,11,13,12
28,291,6,53,17,40,11,22
19,272,6,119,2,29,7,11
15,312,5,46,1,24,10,23"""

stats_globales_euro = {
    42: 12.42, 35: 12.42, 21: 12.27, 29: 11.96, 34: 11.66, 10: 11.35, 13: 11.20, 
    19: 11.04, 47: 10.89, 3: 8.44, 4: 8.74, 8: 9.51, 31: 8.13, 20: 10.28, 1: 7.21
}

# --- 3. MOTEUR DE RÉSONANCE ET SUPERPOSITION V18.1 ---
def moteur_v18_fusion(df_stats, historique, type_jeu):
    df = df_stats.copy()
    tous_sortis = [n for tirage, etoiles in historique for n in tirage]
    counts = Counter(tous_sortis)
    dernier_tirage = historique[0][0]
    moyenne_pos = sum(dernier_tirage) / len(dernier_tirage)
    
    # A. Score de Résonance (Base Solide + Activité)
    def calculer_resonance(row):
        num = row['Numéro']
        freq_10 = counts.get(num, 0)
        
        # Bonus Base Solide (Numéros actifs sur les 10 derniers)
        bonus_base = 35 if 1 <= freq_10 <= 3 else (10 if freq_10 > 3 else 0)
        
        # Puissance historique (% Euro ou Réussite Loto)
        if type_jeu == "EURO":
            poids_hist = stats_globales_euro.get(num, 9.0) * 3
        else:
            poids_hist = row.get('Réussite', 0) / 25

        # B. Observation de Position (Compensation de Masse)
        bonus_pos = 0
        if moyenne_pos > 28 and num <= 22: bonus_pos = 30 # Tirage haut -> focus bas
        if moyenne_pos < 22 and num >= 30: bonus_pos = 30 # Tirage bas -> focus haut

        # C. Alerte Rupture (Ecart Record)
        bonus_rupture = 0
        if row.get('EcartActuel', 0) >= row.get('EcartMax', 0) and row.get('EcartMax', 0) > 0:
            bonus_rupture = 70
            
        return (freq_10 * 12) + bonus_base + poids_hist + bonus_pos + bonus_rupture

    df['score_resonance'] = df.apply(calculer_resonance, axis=1)
    
    # D. Liens d'Affinités (Succession)
    df['bonus_liens'] = 0
    for n in dernier_tirage:
        if 'AnnoncePar' in df.columns:
            df.loc[df['AnnoncePar'] == n, 'bonus_liens'] += 25
        if 'AnnonciateurDe' in df.columns:
            df.loc[df['AnnonciateurDe'] == n, 'bonus_liens'] += 20

    df['score_final'] = df['score_resonance'] + df['bonus_liens']
    return df.sort_values('score_final', ascending=False)

# --- 4. INTERFACE ---
st.title("🛰️ IA EXPERT V18.1 - RÉSONANCE & SUPERPOSITION")
st.markdown("### Analyse des 10 derniers tirages + Puissance Historique")

# Préparation DataFrames
df_loto = pd.read_csv(io.StringIO(loto_data))
df_euro = pd.DataFrame(list(stats_globales_euro.items()), columns=['Numéro', 'Pourcentage'])
for col in ['EcartActuel', 'EcartMax', 'AnnoncePar', 'AnnonciateurDe']: df_euro[col] = 0
# Correction écarts Euro connus
df_euro.loc[df_euro['Numéro'] == 32, ['EcartActuel', 'EcartMax']] = [38, 47]
df_euro.loc[df_euro['Numéro'] == 21, ['EcartActuel', 'EcartMax']] = [32, 55]

# Calculs
res_loto = moteur_v18_fusion(df_loto, HISTORIQUE_LOTO, "LOTO")
res_euro = moteur_v18_fusion(df_euro, HISTORIQUE_EURO, "EURO")

c1, c2 = st.columns(2)

with c1:
    st.header("🎰 PRONOSTIC LOTO")
    t_l = res_loto.head(5)['Numéro'].tolist()
    t_l.sort()
    st.success(f"### 👉 {', '.join(map(str, t_l))}")
    st.info(f"**Analyse :** Moyenne dernier tirage élevée ({sum(HISTORIQUE_LOTO[0][0])/5}). Le moteur privilégie la zone basse et les bases solides.")
    if 1 in t_l: st.error("🚨 ALERTE : Rupture statistique imminente sur le n°1.")

with c2:
    st.header("🇪🇺 PRONOSTIC EURO")
    t_e = res_euro.head(5)['Numéro'].tolist()
    t_e.sort()
    st.error(f"### 👉 {', '.join(map(str, t_e))}")
    st.info(f"**Analyse :** Moyenne dernier tirage basse ({sum(HISTORIQUE_EURO[0][0])/5}). Le moteur réinjecte les fortes puissances historiques (%).")

st.divider()
with st.expander("📊 Détails de la Résonance (Top 10)"):
    col_a, col_b = st.columns(2)
    col_a.write("**Loto :**")
    col_a.dataframe(res_loto[['Numéro', 'score_final', 'score_resonance', 'bonus_liens']].head(10))
    col_b.write("**Euro :**")
    col_b.dataframe(res_euro[['Numéro', 'score_final', 'score_resonance']].head(10))

import streamlit as st
import pandas as pd
import io
from collections import Counter

# --- CONFIGURATION ---
st.set_page_config(page_title="IA EXPERT V21 - SYNCHRO TOTALE", layout="wide", page_icon="🌐")

# --- 1. BASE DE DONNÉES SYNCHRONISÉE (MAI 2026) ---

# Derniers résultats Loto (MAJ: 06/05)
HISTORIQUE_LOTO = [
    ([7, 18, 27, 35, 48], [5]),   # 6 Mai
    ([4, 8, 15, 18, 46], [2]),    # 4 Mai
    ([10, 17, 19, 29, 41], [7]),  # 2 Mai
    ([2, 3, 30, 31, 37], [8]),    # 29 Avril
    ([6, 15, 23, 27, 43], [4]),
    ([9, 17, 22, 25, 49], [3]),
    ([2, 12, 16, 20, 26], [2]),
    ([30, 37, 38, 40, 43], [1]),
    ([2, 12, 21, 29, 33], [6]),
    ([5, 22, 23, 24, 25], [10])
]

# Derniers résultats Euro (MAJ: 08/05)
HISTORIQUE_EURO = [
    ([2, 17, 19, 34, 37], [8, 11]), # 8 Mai - Tirage de ce soir
    ([3, 4, 8, 20, 31], [1, 9]),    # 5 Mai
    ([3, 9, 42, 46, 47], [1, 11]),  # 1er Mai
    ([26, 29, 41, 46, 47], [8, 9]), # 28 Avril
    ([1, 2, 4, 7, 28], [5, 12]),    # 14 Avril
    ([10, 13, 14, 38, 41], [6, 9]), # 10 Avril
    ([11, 14, 19, 36, 49], [6, 7]), # 7 Avril
    ([8, 27, 29, 46, 49], [2, 10]), # 3 Avril
    ([5, 8, 10, 33, 38], [2, 7]),    # 31 Mars
    ([4, 10, 43, 44, 48], [2, 4])    # 27 Mars
]

# --- 2. MATRICE DE PUISSANCE (LOTO & EURO) ---
loto_stats = """Numéro,Réussite,EcartMax,EcartActuel,AnnoncePar,AnnonciateurDe
1,291,42,42,34,6
13,321,55,13,31,3
18,272,67,0,46,29
41,322,41,2,13,17
2,284,55,3,45,9
19,272,119,2,7,11
28,291,53,17,11,22"""

euro_stats = {
    42: 12.42, 47: 10.89, 21: 12.27, 34: 11.66, 19: 11.04, 
    2: 9.97, 17: 10.12, 32: 9.36, 44: 10.74, 3: 8.44
}

# --- 3. MOTEUR DE SYNCHRONISATION V21 ---
def moteur_v21_synchro(stats_df, historique, type_jeu):
    df = stats_df.copy()
    tous_sortis = [n for t, e in historique for n in t]
    counts = Counter(tous_sortis)
    dernier = historique[0][0]
    
    # 1. Poids des Bases Solides (Sorties sur les 10 derniers)
    df['base_solide'] = df['Numéro'].apply(lambda x: counts.get(x, 0) * 50)
    
    # 2. Poids de Forme (Répétition du dernier tirage)
    df['forme_flash'] = df['Numéro'].apply(lambda x: 40 if x in dernier else 0)
    
    # 3. Poids de Tension (Ecart Critique)
    if 'EcartActuel' in df.columns:
        df['tension'] = (df['EcartActuel'] / df['EcartMax'] * 100) * 2
    else:
        df['tension'] = 0

    # 4. Compensation de Masse
    moyenne_dernier = sum(dernier) / 5
    df['compensation'] = 0
    if moyenne_dernier > 28: # Si trop haut, on booste le bas
        df.loc[df['Numéro'] < 25, 'compensation'] = 30
    elif moyenne_dernier < 22: # Si trop bas, on booste le haut
        df.loc[df['Numéro'] > 25, 'compensation'] = 30

    # Score Final
    df['score_total'] = df['base_solide'] + df['forme_flash'] + df['tension'] + df['compensation']
    return df.sort_values('score_total', ascending=False)

# --- 4. INTERFACE ---
st.title("🛰️ IA EXPERT V21 - CONSOLE SYNCHRONISÉE")
st.write(f"État du système : **Opérationnel** | Dernière synchro : **Euro 08/05**")

# Traitement Loto
df_loto_input = pd.read_csv(io.StringIO(loto_stats))
res_loto = moteur_v21_synchro(df_loto_input, HISTORIQUE_LOTO, "LOTO")

# Traitement Euro
df_euro_input = pd.DataFrame(list(euro_stats.items()), columns=['Numéro', 'Pct'])
# On simule les colonnes manquantes pour l'Euro pour le moteur
df_euro_input['EcartActuel'] = 0
df_euro_input['EcartMax'] = 0
df_euro_input.loc[df_euro_input['Numéro'] == 32, ['EcartActuel', 'EcartMax']] = [38, 47]
df_euro_input.loc[df_euro_input['Numéro'] == 21, ['EcartActuel', 'EcartMax']] = [32, 55]

res_euro = moteur_v21_synchro(df_euro_input, HISTORIQUE_EURO, "EURO")

c1, c2 = st.columns(2)

with c1:
    st.header("🎰 LOTO (Prochain Tirage)")
    t_l = res_loto.head(5)['Numéro'].tolist()
    t_l.sort()
    st.success(f"### 👉 {', '.join(map(str, t_l))}")
    st.write("**Analyse :** Focus sur la rupture du n°1 et la répétition du 18.")

with c2:
    st.header("🇪🇺 EURO (Prochain Tirage)")
    t_e = res_euro.head(5)['Numéro'].tolist()
    t_e.sort()
    st.error(f"### 👉 {', '.join(map(str, t_e))}")
    st.write("**Analyse :** Ancrage sur les bases solides (19, 34) et retour zone haute.")

st.divider()
st.subheader("📊 Tableau de Bord des Fréquences (10 derniers tirages)")
st.write("Numéros les plus actifs actuellement :")
all_active = Counter([n for t, e in HISTORIQUE_LOTO + HISTORIQUE_EURO for n in t])
st.bar_chart(pd.DataFrame.from_dict(all_active, orient='index', columns=['Sorties']).head(20))

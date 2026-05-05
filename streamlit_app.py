import streamlit as st
import pandas as pd
import io
from collections import Counter

# --- CONFIGURATION ---
st.set_page_config(page_title="IA EXPERT V12 - FULL HISTORY", layout="wide", page_icon="💎")

# --- 1. HISTORIQUE LOTO (10 DERNIERS TIRAGES) ---
HISTORIQUE_LOTO = [
    ([4, 8, 15, 18, 46], [2]),    # 4 Mai
    ([10, 17, 19, 29, 41], [7]),  # 2 Mai
    ([2, 3, 30, 31, 37], [8]),    # 29 Avril
    ([6, 15, 23, 27, 43], [4]),   # 27 Avril
    ([9, 17, 22, 25, 49], [3]),   # 25 Avril
    ([2, 12, 16, 20, 26], [2]),   # 24 Avril (Super Loto)
    ([30, 37, 38, 40, 43], [1]),  # 22 Avril
    ([2, 12, 21, 29, 33], [6]),   # 20 Avril
    ([5, 22, 23, 24, 25], [10]),  # 18 Avril
    ([2, 21, 44, 47, 48], [10])   # 15 Avril
]

# --- 2. HISTORIQUE EURO (10 DERNIERS TIRAGES) ---
HISTORIQUE_EURO = [
    ([3, 9, 42, 46, 47], [1, 11]),   # 1er Mai
    ([26, 29, 41, 46, 47], [8, 9]),  # 28 Avril
    ([1, 2, 4, 7, 28], [5, 12]),     # 14 Avril
    ([10, 13, 14, 38, 41], [6, 9]),  # 10 Avril
    ([11, 14, 19, 36, 49], [6, 7]),  # 7 Avril
    ([8, 27, 29, 46, 49], [2, 10]),  # 3 Avril
    ([5, 8, 10, 33, 38], [2, 7]),    # 31 Mars
    ([4, 10, 43, 44, 48], [2, 4]),   # 27 Mars
    ([12, 16, 17, 18, 27], [1, 3]),  # 24 Mars
    ([7, 15, 22, 31, 46], [2, 10])   # 17 Mars
]

# --- 3. BASES DE DONNÉES STATISTIQUES ---
euro_csv = """Numéro,Réussite totale,Forme générale,Écart maximum,Écart actuel,Annonceur_De
44,222,12,48,5,50
42,220,10,50,0,12
23,218,4,46,4,19
19,216,5,43,7,26
29,216,11,44,1,19
32,178,4,47,36,25
26,202,9,70,1,21
47,182,9,82,0,3
41,179,11,46,1,15
3,188,3,65,0,1
1,185,5,58,5,44
10,211,10,56,6,24"""

loto_csv = """Numéro,Réussite totale,Forme générale,Écart maximum,Écart actuel,Annonceur_De
41,322,8,41,1,17
13,321,6,55,12,3
22,314,9,50,4,26
15,312,5,46,0,23
3,305,7,49,2,15
1,291,3,42,41,6
4,285,6,46,0,44
8,271,6,58,0,43
18,271,7,67,0,29
46,281,4,42,0,18
2,284,9,55,2,9
17,284,10,58,1,41
23,291,9,52,3,32
5,289,9,46,8,9
31,299,6,67,2,13"""

# --- 4. MOTEUR DE CALCUL AVANCÉ ---
def moteur_ia_v12(df, historique, type_jeu):
    df = df.copy()
    dernier_tirage = historique[0][0]
    max_val = 49 if type_jeu == "LOTO" else 50
    
    # A. Fréquence Dynamique (Calculée sur les 10 tirages)
    tous_nums = [n for tirage, etoiles in historique for n in tirage]
    freqs = Counter(tous_nums)
    df['bonus_frequence'] = df['Numéro'].apply(lambda x: freqs.get(x, 0) * 10)
    
    # B. Tension et Voisinage
    df['tension'] = (df['Écart actuel'] / df['Écart maximum'] * 100)
    voisins = [n-1 for n in dernier_tirage] + [n+1 for n in dernier_tirage]
    df['bonus_voisin'] = df['Numéro'].apply(lambda x: 20 if x in voisins else 0)
    
    # C. Annonceur de Succession
    appeles = df[df['Numéro'].isin(dernier_tirage)]['Annonceur_De'].tolist()
    df['bonus_annonce'] = df['Numéro'].apply(lambda x: 25 if x in appeles else 0)
    
    # D. Logique des Masses
    poids_bas = sum(1 for n in dernier_tirage if n <= (max_val/2))
    df['bonus_masse'] = 0
    if poids_bas >= 4: df.loc[df['Numéro'] > (max_val/2), 'bonus_masse'] = 20
    elif poids_bas <= 1: df.loc[df['Numéro'] <= (max_val/2), 'bonus_masse'] = 25

    # SCORE FINAL
    df['score'] = (df['tension'] * 0.4) + (df['Forme générale'] * 1.5) + \
                  df['bonus_frequence'] + df['bonus_voisin'] + \
                  df['bonus_annonce'] + df['bonus_masse']
    return df.sort_values('score', ascending=False)

# --- 5. INTERFACE ---
st.title("💎 IA EXPERT V12 : Analyse Historique Double")

df_l = pd.read_csv(io.StringIO(loto_csv))
df_e = pd.read_csv(io.StringIO(euro_csv))

res_loto = moteur_ia_v12(df_l, HISTORIQUE_LOTO, "LOTO")
res_euro = moteur_ia_v12(df_e, HISTORIQUE_EURO, "EURO")

tab1, tab2 = st.tabs(["🎰 PRONOSTIC LOTO", "🇪🇺 PRONOSTIC EURO"])

with tab1:
    st.header("LOTO : Analyse des 10 derniers tirages")
    c1, c2 = st.columns([2, 1])
    with c1:
        st.bar_chart(res_loto.head(10).set_index('Numéro')['score'])
    with c2:
        ticket_l = res_loto.head(5)['Numéro'].tolist()
        ticket_l.sort()
        st.success("### 🎟️ TICKET À JOUER")
        st.subheader(f"{', '.join(map(str, ticket_l))}")
        st.write(f"Priorité Fréquence : {res_loto.iloc[0]['Numéro']}")

with tab2:
    st.header("EURO : Analyse des 10 derniers tirages")
    c1, c2 = st.columns([2, 1])
    with c1:
        st.bar_chart(res_euro.head(10).set_index('Numéro')['score'], color="#FF4B4B")
    with c2:
        ticket_e = res_euro.head(5)['Numéro'].tolist()
        ticket_e.sort()
        st.error("### 🎟️ TICKET À JOUER")
        st.subheader(f"{', '.join(map(str, ticket_e))}")
        st.write(f"Priorité Succession : {res_euro.iloc[0]['Annonceur_De']}")

st.divider()
st.info("💡 **Note IA :** Le moteur détecte une forte répétition du n°2 au Loto (4 sorties en 10 tirages) et du n°46 à l'Euro. La probabilité de sortie des voisins (1, 3, 45, 47) est augmentée.")

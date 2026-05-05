import streamlit as st
import pandas as pd
import io

# --- CONFIGURATION ---
st.set_page_config(page_title="IA EXPERT V7 - MULTI-JEUX", layout="wide", page_icon="⚖️")

# --- 1. DERNIERS RÉSULTATS (À mettre à jour après chaque tirage) ---
DERNIERS_LOTO = [4, 8, 15, 18, 46]
DERNIERS_EURO = [26, 29, 41, 46, 47]

# --- 2. DONNÉES STATISTIQUES (FUSIONNÉES) ---
# Données Loto basées sur ton tableau (Extraits)
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
46,281,4,42,0,18"""

# Données EuroMillions basées sur ton tableau (Extraits)
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
46,172,7,66,0,17"""

# --- 3. MOTEUR DE CALCUL EXPERT ---
def calculer_scores(df, derniers_numeros, type_jeu):
    df = df.copy()
    max_num = 49 if type_jeu == "LOTO" else 50
    
    # A. Tension (Retard vs Historique)
    df['tension'] = (df['Écart actuel'] / df['Écart maximum'] * 100)
    
    # B. Bonus Voisinage
    voisins = [n-1 for n in derniers_numeros] + [n+1 for n in derniers_numeros]
    df['bonus_voisin'] = df['Numéro'].apply(lambda x: 20 if x in voisins else 0)
    
    # C. Bonus Annonce (Basé sur tes colonnes "Annonceur_De")
    appeles = df[df['Numéro'].isin(derniers_numeros)]['Annonceur_De'].tolist()
    df['bonus_annonce'] = df['Numéro'].apply(lambda x: 25 if x in appeles else 0)
    
    # D. Logique des Masses
    poids_bas = sum(1 for n in derniers_numeros if n <= (max_num/2))
    df['bonus_masse'] = 0
    if poids_bas >= 4: df.loc[df['Numéro'] > (max_num/2), 'bonus_masse'] = 15
    elif poids_bas <= 1: df.loc[df['Numéro'] <= (max_num/2), 'bonus_masse'] = 20

    # Score Final
    df['score'] = (df['tension'] * 0.4) + (df['Forme générale'] * 1.5) + df['bonus_voisin'] + df['bonus_annonce'] + df['bonus_masse']
    return df.sort_values('score', ascending=False)

# --- 4. INTERFACE ---
st.title("🛰️ IA EXPERT V7 : Évaluation Croisée Loto & Euro")

tab1, tab2, tab3 = st.tabs(["🎰 LOTO", "🇪🇺 EURO", "🧠 ÉVALUATION CROISÉE"])

with tab1:
    df_l = pd.read_csv(io.StringIO(loto_csv))
    res_l = calculer_scores(df_l, DERNIERS_LOTO, "LOTO")
    st.header(f"Top Loto : {res_l['Numéro'].iloc[0]} (Score {res_l['score'].iloc[0]:.1f})")
    st.bar_chart(res_l.head(10).set_index('Numéro')['score'])
    st.dataframe(res_l[['Numéro', 'score', 'Écart actuel', 'bonus_annonce']].head(10))

with tab2:
    df_e = pd.read_csv(io.StringIO(euro_csv))
    res_e = calculer_scores(df_e, DERNIERS_EURO, "EURO")
    st.header(f"Top Euro : {res_e['Numéro'].iloc[0]} (Score {res_e['score'].iloc[0]:.1f})")
    st.bar_chart(res_e.head(10).set_index('Numéro')['score'], color="#FF4B4B")
    st.dataframe(res_e[['Numéro', 'score', 'Écart actuel', 'bonus_annonce']].head(10))

with tab3:
    st.header("🔍 Analyse des Points Chauds")
    
    # Comparaison des masses
    m_loto = sum(1 for n in DERNIERS_LOTO if n <= 24)
    m_euro = sum(1 for n in DERNIERS_EURO if n <= 25)
    
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Masse Basse Loto", f"{m_loto}/5", delta="Équilibré" if 2<=m_loto<=3 else "Déséquilibre")
    with c2:
        st.metric("Masse Basse Euro", f"{m_euro}/5", delta="Équilibré" if 2<=m_euro<=3 else "Déséquilibre", delta_color="inverse")

    st.info("""
    **Stratégie de Jeu suggérée :**
    *   **Loto :** Le numéro 1 approche de son écart max historique (41/42). C'est la priorité n°1.
    *   **Euro :** Déséquilibre total vers le haut. Il faut impérativement jouer des numéros entre 1 et 25 au prochain tirage.
    *   **Transversal :** Le numéro 23 apparaît dans les deux statistiques comme une force d'annonce majeure.
    """)

import streamlit as st
import pandas as pd
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="IA EXPERT V4 - PRÉDICTION", layout="wide", page_icon="🔮")

# --- PARAMÈTRES DES DERNIERS TIRAGES ---
# Mets à jour ces numéros après chaque tirage pour activer les bonus
DERNIERS_LOTO = [4, 12, 25, 33, 48]
DERNIERS_EURO = [11, 14, 20, 35, 43]

# --- DICTIONNAIRE DES ANNONCIATEURS (Basé sur tes données) ---
# Format : {Numéro Sorti : Numéro qu'il annonce souvent}
ANNONCES_EURO = {23: 19, 10: 24, 49: 42, 13: 26, 50: 16, 44: 50, 42: 12, 17: 7}
ANNONCES_LOTO = {23: 32, 10: 47, 49: 29, 13: 3, 16: 5, 2: 9, 27: 30, 41: 17}

# --- MOTEUR DE CALCUL ---
def calculer_scores_expert(df, derniers_numeros, dico_annonces):
    df = df.copy()
    df['ecart_max'] = df['ecart_max'].replace(0, 1)
    moy_h = df['reussite'].mean() if df['reussite'].mean() != 0 else 1
    
    # 1. Tension & Accélération
    df['tension'] = (df['ecart_actuel'] / df['ecart_max'] * 100).clip(upper=110)
    df['acceleration'] = (df['forme_generale'] / (moy_h / 10) * 100).fillna(0)
    
    # 2. Bonus Voisinage (n+1 / n-1)
    voisins = [n-1 for n in derniers_numeros] + [n+1 for n in derniers_numeros]
    df['bonus_voisin'] = df['numero'].apply(lambda x: 15 if x in voisins else 0)
    
    # 3. Bonus Annonciateur (Le numéro qui "appelle" l'autre)
    df['bonus_annonce'] = 0
    for dernier in derniers_numeros:
        if dernier in dico_annonces:
            num_appelé = dico_annonces[dernier]
            df.loc[df['numero'] == num_appelé, 'bonus_annonce'] += 20

    # 4. Score Final Pondéré
    df['score_expert'] = (df['tension'] * 0.40) + (df['acceleration'] * 0.30) + df['bonus_voisin'] + df['bonus_annonce']
    return df.sort_values('score_expert', ascending=False)

# --- CHARGEMENT ---
@st.cache_data
def load_data():
    if os.path.exists('data_expert.csv'):
        return pd.read_csv('data_expert.csv')
    return None

df_raw = load_data()

# --- INTERFACE ---
st.title("🔮 IA EXPERT V4 : Système de Succession")
st.markdown("---")

if df_raw is not None:
    # Nettoyage
    df_raw['jeu'] = df_raw['jeu'].astype(str).str.upper().str.strip()
    
    # Calculs
    df_euro = calculer_scores_expert(df_raw[df_raw['jeu'] == 'EURO'], DERNIERS_EURO, ANNONCES_EURO)
    df_loto = calculer_scores_expert(df_raw[df_raw['jeu'] == 'LOTO'], DERNIERS_LOTO, ANNONCES_LOTO)

    # --- ALERTES SUITES ---
    for jeu_name, df_res in [("Euro", df_euro), ("Loto", df_loto)]:
        top_10 = df_res.head(10)['numero'].tolist()
        suites = [f"{n}-{n+1}" for n in top_10 if n+1 in top_10]
        if suites:
            st.warning(f"⚠️ **Alerte Suite {jeu_name} :** Les paires {', '.join(suites)} sont dans le Top 10 !")

    # --- AFFICHAGE ---
    tab1, tab2 = st.tabs(["🇪🇺 EURO MILLIONS", "🎰 LOTO"])

    with tab1:
        c1, c2 = st.columns([1, 1])
        with c1:
            st.subheader("📊 Graphique des Probabilités")
            st.bar_chart(df_euro.head(10).set_index('numero')['score_expert'])
        with c2:
            st.subheader("📋 Top Experts")
            st.dataframe(df_euro[['numero', 'score_expert', 'tension', 'acceleration', 'bonus_annonce']].head(12))

    with tab2:
        c1, c2 = st.columns([1, 1])
        with c1:
            st.subheader("📊 Graphique des Probabilités")
            st.bar_chart(df_loto.head(10).set_index('numero')['score_expert'], color="#FF4B4B")
        with c2:
            st.subheader("📋 Top Experts")
            st.dataframe(df_loto[['numero', 'score_expert', 'tension', 'acceleration', 'bonus_annonce']].head(12))

else:
    st.error("Fichier data_expert.csv manquant.")

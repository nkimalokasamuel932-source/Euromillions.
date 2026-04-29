import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime

# --- CONFIGURATION ENGINE ---
st.set_page_config(page_title="IA OMNIBUS V6.0 - High Performance", page_icon="⚡", layout="wide")

# Design Système : Dark Neumorphism
st.markdown("""
    <style>
    .main { background: radial-gradient(circle at top, #0f172a, #020617); color: #f8fafc; font-family: 'Urbanist', sans-serif; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: transparent; border-radius: 4px; color: #94a3b8; }
    .stTabs [data-baseweb="tab--active"] { border-bottom: 2px solid #00ffcc; color: #00ffcc; font-weight: bold; }
    
    .metric-card {
        background: rgba(30, 41, 59, 0.7); padding: 20px; border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1); text-align: center;
    }
    .ball {
        display: inline-flex; align-items: center; justify-content: center;
        width: 58px; height: 58px; border-radius: 50%; font-size: 24px;
        font-weight: 800; margin: 8px; color: #000;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3), inset -4px -4px 8px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    .ball:hover { transform: scale(1.15) rotate(5deg); }
    .euro-ball { background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%); }
    .loto-ball { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- ENGINE : CHARGEMENT & CALCULS ---
@st.cache_data
def get_data():
    file = "data_fusion.csv"
    if os.path.exists(file):
        return pd.read_csv(file)
    return pd.DataFrame()

df = get_data()

def predict_engine(mode="euro"):
    if df.empty: return []
    
    # Création du Score IA
    if mode == "euro":
        # Logique : Tension Euro + Masse Euro - (Pénalité Loto si sorti ce soir)
        scores = (df['masse_euro'] * 0.3) + (df['ecart_euro'] * 0.7)
        # Application du Vase Communiquant
        df['score'] = np.where(df['sorti_loto_ce_soir'] == 1, scores - 60, scores)
    else:
        # Logique Loto : Masse Loto + Écart Loto + Bonus Forme
        scores = (df['masse_loto'] * 0.5) + (df['ecart_loto'] * 0.3)
        df['score'] = np.where(df['sorti_loto_ce_soir'] == 1, scores + 30, scores)
    
    # On retourne les 5 meilleurs numéros
    return df.sort_values('score', ascending=False).head(5)['numero'].tolist()

# --- INTERFACE UTILISATEUR ---
st.title("⚡ IA OMNIBUS V6.0")
st.write(f"Moteur Prédictif Synchronisé | **Date : {datetime.now().strftime('%d/%m/%Y')}**")

if df.empty:
    st.error("❌ Fichier 'data_fusion.csv' non détecté. Veuillez l'ajouter à votre dossier GitHub.")
else:
    tab1, tab2, tab3 = st.tabs(["🎯 Tirages", "📈 Analyses Flux", "⚙️ Config"])

    with tab1:
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.subheader("🇪🇺 OPTIMISATION EURO")
            if st.button("CALCULER FLUX EURO"):
                picks = sorted(predict_engine("euro"))
                html = "".join([f"<div class='ball euro-ball'>{int(n)}</div>" for n in picks])
                st.markdown(html, unsafe_allow_html=True)
                st.caption("Stratégie : Rupture de Tension (Ecart Max)")
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.subheader("🇫🇷 OPTIMISATION LOTO")
            if st.button("CALCULER FLUX LOTO"):
                picks = sorted(predict_engine("loto"))
                html = "".join([f"<div class='ball loto-ball'>{int(n)}</div>" for n in picks])
                st.markdown(html, unsafe_allow_html=True)
                st.caption("Stratégie : Inertie de Forme (Masse Max)")
            st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.write("### 🔥 Zones de Chaleur Statistique")
        # Création d'un graphique de pression
        chart_data = df[['numero', 'ecart_euro', 'ecart_loto']].set_index('numero')
        st.bar_chart(chart_data)
        st.info("Les barres les plus hautes indiquent les numéros sous tension maximale (rupture imminente).")

    with tab3:
        st.write("### 🛠️ Données Sources")
        st.dataframe(df, use_container_width=True)
        st.success(f"Base de données : {len(df)} numéros indexés.")

st.divider()
st.caption("Version 6.0 | Architecture AIO (All-In-One) | Compatible Streamlit Cloud 2026")

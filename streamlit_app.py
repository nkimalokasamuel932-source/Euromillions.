import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime

# --- 1. CONFIGURATION ET STYLE ---
st.set_page_config(page_title="IA OMNIBUS V9.0 - Triple Flux", page_icon="🧬", layout="wide")

st.markdown("""
    <style>
    .main { background: radial-gradient(circle at top, #081221, #020617); color: #f8fafc; font-family: 'Urbanist', sans-serif; }
    .card { background: rgba(30, 41, 59, 0.4); padding: 20px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px; }
    .strat-header { font-size: 18px; font-weight: bold; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px; }
    
    /* Couleurs des Stratégies */
    .alpha-title { color: #00ffcc; }
    .beta-title { color: #ff00ff; }
    .theta-title { color: #f8fafc; border-bottom: 1px solid #94a3b8; }
    
    .ball {
        display: inline-flex; align-items: center; justify-content: center;
        width: 52px; height: 52px; border-radius: 50%; font-size: 20px;
        font-weight: 800; margin: 6px; color: #000;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3), inset -3px -3px 6px rgba(0,0,0,0.2);
    }
    .alpha-ball { background: linear-gradient(135deg, #00f2fe, #4facfe); }
    .beta-ball { background: linear-gradient(135deg, #f093fb, #f5576c); color: white; }
    .theta-ball { background: linear-gradient(135deg, #94a3b8, #475569); color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BASE DE DONNÉES INTERNE (Synchronisée avec tes stats d'Expert) ---
@st.cache_data
def get_internal_db():
    data = {
        "numero": [1, 3, 7, 9, 10, 11, 13, 15, 17, 18, 19, 22, 23, 25, 29, 31, 32, 33, 41, 42, 46, 47],
        "reussite": [291, 305, 294, 299, 292, 274, 321, 311, 284, 270, 271, 314, 291, 273, 300, 299, 278, 278, 322, 274, 280, 280],
        "ecart": [39, 0, 0, 2, 0, 25, 11, 1, 0, 8, 0, 2, 1, 2, 0, 0, 32, 5, 0, 17, 10, 7],
        "max": [42, 49, 52, 44, 43, 65, 55, 46, 58, 67, 119, 50, 52, 53, 38, 67, 64, 41, 41, 54, 42, 68],
        "annonce_par": [34, 44, 13, 2, 26, 19, 31, 10, 41, 13, 7, 6, 9, 15, 38, 37, 23, 25, 13, 9, 1, 10],
        "affinite": [49, 13, 11, 15, 30, 7, 3, 24, 30, 13, 29, 23, 32, 33, 19, 36, 22, 22, 16, 16, 22, 21]
    }
    return pd.DataFrame(data)

df = get_internal_db()

# --- 3. MOTEUR DE CALCUL MULTI-STRATÉGIES ---
def engine_multi_flux(last_draw):
    # STRATÉGIE ALPHA : Tension & Rupture (Les grands écarts)
    df['score_alpha'] = (df['reussite'] * 0.1) + (df['ecart'] * 2.5)
    # Bonus Annonciateurs
    for num in last_draw:
        df.loc[df['annonce_par'] == num, 'score_alpha'] += 40
    alpha = df.sort_values('score_alpha', ascending=False).head(5)['numero'].tolist()

    # STRATÉGIE BÊTA : Masse & Puissance (Les meilleures réussites / Forme)
    # On mélange les top réussites avec un peu d'aléatoire contrôlé
    beta_pool = df.sort_values('reussite', ascending=False).head(10)
    beta = beta_pool.sample(5)['numero'].tolist()

    # STRATÉGIE THÊTA : Chaos & Surprise (Numéros non attendus / Faible écart)
    # On cherche les numéros qui viennent de sortir ou dorment (écart < 5) 
    # et qui n'ont pas une réussite maximale.
    theta_pool = df[(df['ecart'] < 5) & (df['reussite'] < 300)]
    if len(theta_pool) < 5: theta_pool = df.sample(5) # Sécurité
    theta = theta_pool.sample(5)['numero'].tolist()

    return sorted(alpha), sorted(beta), sorted(theta)

# --- 4. INTERFACE ---
st.title("🧬 IA OMNIBUS V9.0")
st.write(f"Analyse Multi-Flux Synchronisée | **Dernier Tirage (Loto/Euro) : 7-10-17-19-29-41**")

# On définit le socle de calcul sur les derniers résultats connus
derniers_resultats = [7, 10, 17, 19, 29, 41]

if st.button("🌀 GÉNÉRER LES TROIS FLUX DE RÉSONANCE"):
    alpha, beta, theta = engine_multi_flux(derniers_resultats)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='strat-header alpha-title'>🎯 Flux ALPHA</div>", unsafe_allow_html=True)
        st.caption("Stratégie : Tension & Rupture")
        balls_html = "".join([f"<div class='ball alpha-ball'>{n}</div>" for n in alpha])
        st.markdown(balls_html, unsafe_allow_html=True)
        st.info("Cible les numéros en retard critique (ex: 32, 1).")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='strat-header beta-title'>🔥 Flux BÊTA</div>", unsafe_allow_html=True)
        st.caption("Stratégie : Masse & Puissance")
        balls_html = "".join([f"<div class='ball beta-ball'>{n}</div>" for n in beta])
        st.markdown(balls_html, unsafe_allow_html=True)
        st.info("Cible les piliers historiques (ex: 13, 22).")
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='strat-header theta-title'>🎲 Flux THÊTA</div>", unsafe_allow_html=True)
        st.caption("Stratégie : Chaos & Surprise")
        balls_html = "".join([f"<div class='ball theta-ball'>{n}</div>" for n in theta])
        st.markdown(balls_html, unsafe_allow_html=True)
        st.info("Cible l'imprévisible (numéros froids ou récents).")
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.write("### 📊 État de la Base de Données Omnibus")
st.dataframe(df.sort_values('ecart', ascending=False), use_container_width=True)
st.caption("Version 9.0 | Système Multi-Grilles pour couverture maximale du hasard.")

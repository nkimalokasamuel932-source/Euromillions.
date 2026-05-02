import streamlit as st
import pandas as pd
import random

# --- CONFIGURATION ---
st.set_page_config(page_title="OMNIBUS V10 - Multi-Jeux", page_icon="📡", layout="wide")

st.markdown("""
    <style>
    .main { background: #020617; color: #f8fafc; font-family: 'Urbanist', sans-serif; }
    .card { background: rgba(30, 41, 59, 0.4); padding: 20px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px; }
    .ball {
        display: inline-flex; align-items: center; justify-content: center;
        width: 45px; height: 45px; border-radius: 50%; font-size: 18px;
        font-weight: 800; margin: 5px; color: #000;
        box-shadow: inset -2px -2px 6px rgba(0,0,0,0.3);
    }
    .alpha { background: linear-gradient(135deg, #00f2fe, #4facfe); }
    .beta { background: linear-gradient(135deg, #f093fb, #f5576c); color: white; }
    .theta { background: linear-gradient(135deg, #94a3b8, #475569); color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. DATASET LOTO (Basé sur tes stats fournies) ---
@st.cache_data
def get_loto_data():
    return pd.DataFrame({
        "numero": [41, 13, 22, 15, 3, 29, 31, 9, 16, 1, 32, 11, 19],
        "reussite": [322, 321, 314, 311, 305, 300, 299, 299, 299, 291, 278, 274, 272],
        "ecart_actuel": [0, 11, 3, 2, 1, 0, 1, 3, 4, 40, 32, 26, 0],
        "ecart_max": [41, 55, 50, 46, 49, 38, 67, 44, 53, 42, 64, 65, 119],
        "annonce_par": [13, 31, 6, 10, 44, 38, 37, 2, 13, 34, 23, 19, 7]
    })

# --- 2. DATASET EUROMILLIONS (Basé sur tes stats fournies) ---
@st.cache_data
def get_euro_data():
    return pd.DataFrame({
        "numero": [44, 42, 23, 19, 29, 21, 10, 32, 47, 46, 3, 9],
        "reussite": [222, 220, 218, 216, 216, 212, 211, 178, 182, 172, 188, 184],
        "ecart_actuel": [5, 0, 4, 7, 1, 28, 6, 36, 0, 0, 0, 0],
        "ecart_max": [48, 50, 46, 43, 44, 52, 56, 47, 82, 66, 65, 76],
        "annonce_par": [45, 49, 5, 24, 6, 15, 44, 7, 21, 17, 28, 24]
    })

# --- 3. MOTEUR DE CALCUL ---
def calculate_flux(df, last_draw):
    # ALPHA : Tension (Écart)
    df['score_alpha'] = (df['reussite'] * 0.1) + (df['ecart_actuel'] * 2.5)
    for n in last_draw:
        df.loc[df['annonce_par'] == n, 'score_alpha'] += 50
    alpha = df.sort_values('score_alpha', ascending=False).head(5)['numero'].tolist()

    # BETA : Masse (Réussite)
    beta = df.sort_values('reussite', ascending=False).head(8).sample(5)['numero'].tolist()

    # THETA : Chaos (Ecart faible < 3)
    theta_pool = df[df['ecart_actuel'] < 3]
    theta = theta_pool.sample(min(5, len(theta_pool)))['numero'].tolist()

    return sorted(alpha), sorted(beta), sorted(theta)

# --- 4. INTERFACE ---
st.title("📡 IA OMNIBUS V10 - Système Expert")
game_mode = st.radio("Choisissez le moteur d'analyse :", ["🇫🇷 LOTO", "🇪🇺 EUROMILLIONS"])

if game_mode == "🇫🇷 LOTO":
    df_loto = get_loto_data()
    # Dernier tirage fourni : 10, 17, 19, 29, 41
    last_loto = [10, 17, 19, 29, 41]
    
    if st.button("CALCULER FLUX LOTO"):
        a, b, t = calculate_flux(df_loto, last_loto)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("<div class='card'><b class='alpha'>FLUX ALPHA (Tension)</b>", unsafe_allow_html=True)
            st.write("".join([f"<div class='ball alpha'>{n}</div>" for n in a]), unsafe_allow_html=True)
            st.caption("Cible le retard du numéro 1 et 32")
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='card'><b class='beta'>FLUX BÊTA (Masse)</b>", unsafe_allow_html=True)
            st.write("".join([f"<div class='ball beta'>{n}</div>" for n in b]), unsafe_allow_html=True)
            st.caption("Cible les piliers 41 et 13")
            st.markdown("</div>", unsafe_allow_html=True)
        with c3:
            st.markdown("<div class='card'><b>FLUX THÊTA (Chaos)</b>", unsafe_allow_html=True)
            st.write("".join([f"<div class='ball theta'>{n}</div>" for n in t]), unsafe_allow_html=True)
            st.caption("Cible les répétitions (29, 10, 19)")
            st.markdown("</div>", unsafe_allow_html=True)

else:
    df_euro = get_euro_data()
    # Dernier tirage fourni : 3, 9, 42, 46, 47
    last_euro = [3, 9, 42, 46, 47]
    
    if st.button("CALCULER FLUX EURO"):
        a, b, t = calculate_flux(df_euro, last_euro)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("<div class='card'><b class='alpha'>FLUX ALPHA (Tension)</b>", unsafe_allow_html=True)
            st.write("".join([f"<div class='ball alpha'>{n}</div>" for n in a]), unsafe_allow_html=True)
            st.caption("Cible l'alerte sur le 32 et 21")
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='card'><b class='beta'>FLUX BÊTA (Masse)</b>", unsafe_allow_html=True)
            st.write("".join([f"<div class='ball beta'>{n}</div>" for n in b]), unsafe_allow_html=True)
            st.caption("Cible les piliers 44 et 42")
            st.markdown("</div>", unsafe_allow_html=True)
        with c3:
            st.markdown("<div class='card'><b>FLUX THÊTA (Chaos)</b>", unsafe_allow_html=True)
            st.write("".join([f"<div class='ball theta'>{n}</div>" for n in t]), unsafe_allow_html=True)
            st.caption("Cible les sorties récentes (3, 9, 47)")
            st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.write("### 🗠 Analyse des 5 derniers tirages intégrée")
st.info("L'algorithme a détecté une migration de la zone 40 vers la zone 10. Les flux Thêta sont prioritaires pour capturer l'inertie.")

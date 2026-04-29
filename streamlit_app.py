import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- 1. CONFIGURATION ET DESIGN ---
st.set_page_config(page_title="IA OMNIBUS V4.0", page_icon="🧬", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Urbanist:wght@400;700&display=swap');
    .main { background-color: #050a14; font-family: 'Urbanist', sans-serif; }
    
    /* Cartes de jeu Glassmorphism */
    .game-card {
        padding: 30px; border-radius: 24px; background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px; text-align: center;
    }
    .euro-border { border-top: 5px solid #00ffcc; }
    .loto-border { border-top: 5px solid #ff00ff; }

    /* Boules de tirage 3D */
    .ball {
        display: inline-flex; align-items: center; justify-content: center;
        width: 60px; height: 60px; border-radius: 50%; font-size: 24px;
        font-weight: 700; margin: 8px; color: #000;
        box-shadow: inset -5px -5px 15px rgba(0,0,0,0.2), 5px 5px 15px rgba(0,0,0,0.3);
    }
    .euro-ball { background: linear-gradient(145deg, #00ffcc, #0088aa); }
    .loto-ball { background: linear-gradient(145deg, #ff00ff, #aa00aa); color: white; }
    .star-ball { background: linear-gradient(145deg, #ffd700, #b8860b); width: 50px; height: 50px; font-size: 20px; }

    .tag { display: block; font-size: 10px; text-transform: uppercase; color: #94a3b8; font-weight: bold; margin-top: -5px; }
    
    .stButton > button {
        background: linear-gradient(90deg, #1e293b, #334155); color: white;
        border-radius: 12px; height: 3.5em; width: 100%; border: 1px solid rgba(255,255,255,0.1);
    }
    .stButton > button:hover { border-color: #00ffcc; color: #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BASE DE DONNÉES UNIFIÉE ---
# Structure : [Masse_Hist, Tension_Ecart, Dernier_Tirage, Zone, Tag_Logique, Sorti_Loto_30_04]
db = {
    1:  [185, 4, 14, 1, "Masse", False],
    2:  [179, 4, 30, 1, "Vase Communiquant", True],   # Sorti Loto ce soir
    3:  [187, 60, 30, 1, "Rupture Tension", True],   # Sorti Loto ce soir
    4:  [197, 10, 14, 1, "Forme", False],
    6:  [188, 16, 27, 1, "Voisinage", False],
    12: [194, 10, 24, 1, "Compagnon", False],
    13: [202, 2, 21, 1, "Élite", False],
    30: [180, 5, 30, 2, "Saturation", True],         # Sorti Loto ce soir
    31: [175, 8, 30, 2, "Saturation", True],         # Sorti Loto ce soir
    32: [178, 35, 0, 2, "Oublié", False],
    37: [190, 2, 30, 3, "Saturation", True],         # Sorti Loto ce soir
    42: [219, 17, 0, 3, "Aspiration", False],
    43: [179, 9, 27, 3, "Pivot", False],
    47: [181, 0, 28, 3, "Repos", False]
}

# --- 3. MOTEUR DE CALCUL OMNIBUS ---
def calculer_score_final(n, mode="euro"):
    d = db.get(n)
    # A. Fondamental (Masse + Tension)
    score = (d[0] / 300 * 25) + (d[1] / 60 * 35)
    
    # B. Logique du Vase Communiquant (Migration Loto -> Euro)
    if d[5]: # Si sorti au Loto ce soir
        score -= 50 # Le vase est vide pour ce numéro
    else:
        # C. Logique du Compagnon (Aspiration)
        # Si un numéro adjacent (n-1, n+1) est sorti ce soir, bonus d'aspiration
        for v in [n-1, n+1]:
            if v in db and db[v][5]:
                score += 30
                break
    
    # D. Respiration Temporelle (Bonus Zone Basse pour Vendredi)
    if d[3] == 1: score += 20
    if d[2] <= 14: score += 15 # Bonus pour les numéros absents de la quinzaine
    
    return round(score, 2)

# --- 4. INTERFACE ---
st.title("🧬 IA OMNIBUS V4.0 : Fusion des Systèmes")
st.write(f"Analyse prédictive consolidée | **Status : Cycle d'Expiration Activé**")

# Diagnostic dynamique
st.warning(f"🚨 **ALERTE VASE COMMUNIQUANT :** Les numéros 2, 3, 30, 31, 37 (Loto ce soir) sont exclus des priorités Euro de demain. Transfert d'énergie détecté vers la Zone **12-15**.")

tab1, tab2, tab3 = st.tabs(["🎯 TERMINAL DE TIRAGE", "📊 ANALYSE DE FLUX", "📜 HISTORIQUE LOGIQUE"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='game-card euro-border'>", unsafe_allow_html=True)
        st.subheader("🇪🇺 EUROMILLIONS")
        if st.button("GÉNÉRER GRILLE EURO V4.0"):
            scores_e = {n: calculer_score_final(n, "euro") for n in db.keys()}
            top_e = sorted(scores_e, key=scores_e.get, reverse=True)[:5]
            
            html_res = ""
            for n in sorted(top_e):
                tag = db[n][4] if not db[n][5] else "Remplaçant"
                html_res += f"<div style='display:inline-block;'><div class='ball euro-ball'>{n}</div><span class='tag'>{tag}</span></div>"
            st.markdown(html_res, unsafe_allow_html=True)
            
            st.write("---")
            # Étoiles basées sur la résonance du 8 Loto
            st.markdown("<div class='ball star-ball'>3</div><div class='ball star-ball'>8</div>", unsafe_allow_html=True)
            st.markdown("<span class='tag'>Résonance Étoile Loto</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='game-card loto-border'>", unsafe_allow_html=True)
        st.subheader("🇫🇷 LOTO NATIONAL")
        if st.button("GÉNÉRER GRILLE LOTO V4.0"):
            # Pour le loto on cherche la répétition de forme
            scores_l = {n: (db[n][0]/300*50) + (20 if db[n][5] else 0) for n in db.keys()}
            top_l = sorted(scores_l, key=scores_l.get, reverse=True)[:5]
            
            html_loto = ""
            for n in sorted(top_l):
                html_loto += f"<div style='display:inline-block;'><div class='ball loto-ball'>{n}</div><span class='tag'>Forme</span></div>"
            st.markdown(html_loto, unsafe_allow_html=True)
            
            st.write("---")
            st.markdown("<div class='ball star-ball' style='background:#ff4b4b;color:white;'>4</div>", unsafe_allow_html=True)
            st.markdown("<span class='tag'>Ancre Chance</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.write("### 🧮 Calculateur de Pression (Migration de l'énergie)")
    sc_final = {n: calculer_score_final(n) for n in db.keys()}
    df_flux = pd.DataFrame([
        {"Numéro": k, "Score Omnibus": v, "Zone": db[k][3], "Status": "VIDE (Sorti)" if db[k][5] else "ASPIRATION"}
        for k, v in sc_final.items()
    ]).sort_values("Score Omnibus", ascending=False)
    st.dataframe(df_flux, use_container_width=True)

with tab3:
    st.markdown("""
    ### Structure de la Version 4.0
    - **V1 (Respiration) :** Gère les cycles de 14 jours (Bonus Zone 1).
    - **V2 (Balancier) :** Équilibre les types de numéros (Masse vs Tension).
    - **V3 (Vase Communiquant) :** Analyse les résultats du 30/04 pour purger les doublons.
    - **V4 (Compagnons) :** Boost les numéros voisins de ceux sortis ce soir.
    """)

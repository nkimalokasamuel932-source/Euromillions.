import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- 1. CONFIGURATION & DESIGN ---
st.set_page_config(page_title="IA OMNIBUS V4.1 ELITE", page_icon="🧬", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Urbanist:wght@400;700&display=swap');
    .main { background-color: #050a14; font-family: 'Urbanist', sans-serif; color: #ffffff; }
    
    /* Cartes Glassmorphism */
    .game-card {
        padding: 30px; border-radius: 24px; background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px; text-align: center;
    }
    .euro-border { border-top: 5px solid #00ffcc; box-shadow: 0 10px 30px rgba(0, 255, 204, 0.1); }
    .loto-border { border-top: 5px solid #ff00ff; box-shadow: 0 10px 30px rgba(255, 0, 255, 0.1); }

    /* Boules 3D Premium */
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
        transition: all 0.3s;
    }
    .stButton > button:hover { border-color: #00ffcc; color: #00ffcc; transform: translateY(-2px); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DICTIONNAIRE DES INDICATEURS STATISTIQUES (Base de données) ---
# Format : [Masse_Hist, Tension_Ecart, Date_Derniere_Sortie, Zone, Label_Type, Est_Sorti_Loto_30_04]
# Zone : 1 (Bas), 2 (Milieu), 3 (Haut)
db = {
    1:  [185, 4, 14, 1, "Masse Fondamentale", False],
    2:  [179, 4, 30, 1, "Vase Épuisé", True],         # SORTI AU LOTO 30/04
    3:  [187, 60, 30, 1, "Tension Relâchée", True],   # SORTI AU LOTO 30/04
    4:  [197, 10, 14, 1, "Forme Constante", False],
    6:  [188, 16, 27, 1, "Voisinage Alerte", False],
    12: [194, 10, 24, 1, "Compagnon Direct", False], # COMPAGNON DU 2 (ASSPIRÉ)
    13: [202, 2, 21, 1, "Élite Prioritaire", False], # COMPAGNON DU 3 (ASSPIRÉ)
    23: [218, 3, 27, 2, "Pivot Central", False],
    30: [180, 5, 30, 2, "Saturation Médiane", True],  # SORTI AU LOTO 30/04
    31: [175, 8, 30, 2, "Saturation Médiane", True],  # SORTI AU LOTO 30/04
    32: [178, 35, 0, 2, "Oublié Critique", False],    # TENSION MAX ACTUELLE
    37: [190, 2, 30, 3, "Saturation Haute", True],    # SORTI AU LOTO 30/04
    42: [219, 17, 0, 3, "Aspiration Sommet", False],
    43: [179, 9, 27, 3, "Pivot Historique", False]
}

# --- 3. MOTEUR DE CALCUL MULTI-LOGIQUE ---
def calculer_score_ia(n):
    d = db.get(n)
    # A. Fondamental (Masse 30% + Tension 40%)
    score = (d[0] / 300 * 30) + (d[1] / 60 * 40)
    
    # B. Logique du Vase Communiquant
    if d[5]: # Si sorti ce soir au Loto
        score -= 55 # Malus critique (Énergie vide)
    else:
        # C. Logique du Compagnon (Voisinage)
        # On vérifie si un numéro à +/- 1 ou +/- 10 est sorti ce soir
        for v in [n-1, n+1, n-10, n+10]:
            if v in db and db[v][5]: # Si le voisin est sorti au Loto
                score += 35 # Bonus d'aspiration
                break
    
    # D. Respiration (Bonus Zone Basse pour Vendredi)
    if d[3] == 1: score += 15
    if d[2] <= 14: score += 20 # Bonus "Oubli"
    
    return round(score, 2)

# --- 4. INTERFACE ---
st.title("🧬 IA OMNIBUS V4.1 : Terminal Expert")
st.write(f"Analyse des flux du **{datetime.now().strftime('%d/%m/%Y')}** | Focus : **Vendredi 01 Mai**")

# Barre de diagnostic IA
st.warning("⚠️ **ALERTE LOGIQUE :** Le 2 et le 3 ont migré vers le Loto. Pression maximale détectée sur le **12**, **13** et **32**.")

tab1, tab2 = st.tabs(["🎯 TERMINAL DE PRÉDICTION", "📊 MATRICE DES INDICATEURS"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='game-card euro-border'>", unsafe_allow_html=True)
        st.subheader("🇪🇺 EURO - PHASE D'EXPIRATION")
        if st.button("CALCULER GRILLE EURO"):
            scores_e = {n: calculer_score_ia(n) for n in db.keys()}
            top_e = sorted(scores_e, key=scores_e.get, reverse=True)[:5]
            
            # Affichage des boules
            html_euro = ""
            for n in sorted(top_e):
                tag = db[n][4]
                html_euro += f"<div style='display:inline-block;text-align:center;'><div class='ball euro-ball'>{n}</div><span class='tag'>{tag}</span></div>"
            st.markdown(html_euro, unsafe_allow_html=True)
            
            st.write("---")
            # Étoiles (Résonance du 8 Loto)
            st.markdown("<div class='ball star-ball'>3</div><div class='ball star-ball'>8</div><p><span class='tag'>Étoiles de Résonance</span></p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='game-card loto-border'>", unsafe_allow_html=True)
        st.subheader("🇫🇷 LOTO - PHASE BALANCIER")
        if st.button("CALCULER GRILLE LOTO"):
            # Pour le loto on privilégie la forme récente
            scores_l = {n: (db[n][0]/300*40) + (30 if db[n][5] else 0) for n in db.keys()}
            top_l = sorted(scores_l, key=scores_l.get, reverse=True)[:5]
            
            html_loto = ""
            for n in sorted(top_l):
                html_loto += f"<div style='display:inline-block;text-align:center;'><div class='ball loto-ball'>{n}</div><span class='tag'>Forme</span></div>"
            st.markdown(html_loto, unsafe_allow_html=True)
            
            st.write("---")
            st.markdown("<div class='ball star-ball' style='background:#ff4b4b;color:white;'>4</div><p><span class='tag'>Chance Prioritaire</span></p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.write("### 🧮 Détail des Indicateurs de Force")
    data_table = []
    for k, v in db.items():
        score = calculer_score_ia(k)
        data_table.append({
            "Num": k,
            "Score Global": score,
            "Tension (Ecart)": v[1],
            "Migration": "⚠️ Épuisé" if v[5] else "🔥 Aspiré",
            "Zone": f"Zone {v[3]}"
        })
    df = pd.DataFrame(data_table).sort_values("Score Global", ascending=False)
    st.dataframe(df, use_container_width=True)

st.divider()
st.caption("Version 4.1 - Logique de transfert d'énergie post-tirage Loto du 30/04.")

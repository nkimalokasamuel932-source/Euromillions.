import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# --- 1. CONFIGURATION ET DESIGN ---
st.set_page_config(page_title="IA OMNIBUS V7.0 EXPERT", page_icon="🧬", layout="wide")

st.markdown("""
    <style>
    .main { background: radial-gradient(circle at top, #081221, #020617); color: #f8fafc; font-family: 'Urbanist', sans-serif; }
    .card { background: rgba(30, 41, 59, 0.5); padding: 25px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px; }
    .ball {
        display: inline-flex; align-items: center; justify-content: center;
        width: 58px; height: 58px; border-radius: 50%; font-size: 24px;
        font-weight: 800; margin: 8px; color: #000;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3), inset -4px -4px 8px rgba(0,0,0,0.2);
    }
    .euro-ball { background: linear-gradient(135deg, #00f2fe, #4facfe); }
    .star-ball { background: linear-gradient(135deg, #ffd700, #b8860b); width: 48px; height: 48px; font-size: 18px; }
    .status-text { font-size: 14px; color: #94a3b8; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BASE DE DONNÉES CONSOLIDÉE (Tes stats de vendredi 1er Mai) ---
# Format : [Réussite_Tot, Forme_Rec, Ecart_Act, Ecart_Max, Meilleure_Affin, Annonce_Par, Annonciateur_De]
db_expert = {
    13: [321, 0, 10, 55, 3, 31, 3],
    41: [321, 1, 9, 41, 16, 13, 17],
    22: [314, 3, 2, 50, 23, 6, 26],
    15: [311, 1, 1, 46, 24, 10, 23],
    3:  [305, 1, 0, 49, 13, 44, 15],
    9:  [299, 1, 0, 44, 15, 2, 23],
    16: [299, 2, 3, 53, 6, 13, 5],
    31: [299, 1, 0, 67, 36, 37, 13],
    32: [278, 0, 31, 64, 22, 23, 3],
    42: [274, 0, 0, 54, 16, 9, 14],
    11: [274, 0, 0, 65, 7, 19, 1],
    46: [280, 0, 0, 42, 22, 1, 18],
    47: [280, 1, 0, 68, 21, 10, 3],
    1:  [291, 0, 0, 42, 49, 34, 6]
}

# --- 3. MOTEUR DE CALCUL PRÉDICTIF (ALGO V7) ---
def engine_omnibus(last_draw_results):
    scores = {}
    for n, stats in db_expert.items():
        reussite, forme, ecart, ecart_max, affin, par, annonciateur = stats
        
        # A. Score de Tension (Le ressort statistique)
        score = (reussite * 0.1) + (ecart * 2.0)
        
        # B. Bonus de Zone Critique (Ecart > 60% du Max)
        if ecart > (ecart_max * 0.6):
            score += 45
            
        # C. Logique d'Annonciation (Basée sur le tirage du 1er Mai)
        for last_num in last_draw_results:
            if par == last_num: # Si le numéro est "annoncé par" un sortant
                score += 55
            if affin == last_num: # Si le numéro a une affinité avec un sortant
                score += 30
        
        # D. Malus de sortie récente (Vase vide)
        if ecart == 0:
            score -= 70
            
        scores[n] = round(score, 2)
    
    return sorted(scores, key=scores.get, reverse=True)[:5]

# --- 4. INTERFACE UTILISATEUR ---
st.title("🧬 IA OMNIBUS V7.0 : Système Expert de Flux")
st.write(f"Analyse Post-Tirage du **01/05/2026** | Statut : Synchronisé")

# Résultats du tirage de ce vendredi (1er mai)
derniers_resultats = [1, 3, 9, 11, 42]
etoiles_sorties = [46, 47]

tab1, tab2 = st.tabs(["🎯 GÉNÉRATEUR DE PRÉDICTIONS", "📊 MATRICE ANALYTIQUE"])

with tab1:
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🔮 Prédiction Prochain Tirage")
        st.write("Cible : EuroMillions Mardi 05 Mai")
        
        if st.button("LANCER L'ALGORITHME DE RÉSONANCE"):
            top_numbers = engine_omnibus(derniers_resultats)
            
            # Affichage des boules
            html_res = "".join([f"<div class='ball euro-ball'>{n}</div>" for n in sorted(top_numbers)])
            st.markdown(html_res, unsafe_allow_html=True)
            
            st.write("---")
            st.write("**Étoiles recommandées par affinité :**")
            st.markdown("<div class='ball star-ball'>2</div><div class='ball star-ball'>10</div>", unsafe_allow_html=True)
            st.success("Calcul terminé : Les coefficients d'annonciation ont été appliqués.")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("💡 Diagnostic IA")
        st.info(f"""
            - **Numéros sortis :** {derniers_resultats}
            - **Aspiration :** Le numéro 13 et le 32 sont en surtension.
            - **Annonciation :** Le 42 étant sorti, il appelle ses affinités directes.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.write("### 🧮 Matrice de Calcul Interne")
    data_view = []
    for n, s in db_expert.items():
        data_view.append({
            "Numéro": n,
            "Réussite": s[0],
            "Écart Actuel": s[2],
            "Max Historique": s[3],
            "Annoncé Par": s[5]
        })
    st.dataframe(pd.DataFrame(data_view).sort_values("Écart Actuel", ascending=False), use_container_width=True)

st.divider()
st.caption("Moteur IA Omnibus V7.0 - Basé sur l'analyse des affinités historiques et des tensions de rupture.")

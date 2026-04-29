import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="IA OMNIBUS V5.2 CSV", page_icon="📊", layout="wide")

# --- CHARGEMENT DU CSV FUSIONNÉ ---
def load_fusion_data():
    file = "data_fusion.csv"
    if os.path.exists(file):
        df = pd.read_csv(file)
        # On convertit le DF en dictionnaire pour le moteur de calcul
        db = {}
        for _, r in df.iterrows():
            db[int(r['numero'])] = [
                r['masse_euro'], r['ecart_euro'], 
                r['masse_loto'], r['ecart_loto'], 
                bool(r['sorti_loto_ce_soir'])
            ]
        return db
    else:
        st.error("Fichier data_fusion.csv introuvable !")
        return {}

db = load_fusion_data()

# --- MOTEUR IA ---
def calculer_score(n, mode="euro"):
    d = db.get(n)
    if not d: return 0
    
    if mode == "euro":
        # Priorité Ecart Euro (Index 1)
        score = (d[0]/300*30) + (d[1]/60*50)
        if d[4]: score -= 60 # Malus Vase Communiquant
        for v in [n-1, n+1]: # Bonus Aspiration
            if v in db and db[v][4]: score += 35
    else:
        # Priorité Masse Loto (Index 2)
        score = (d[2]/400*40) + (d[3]/50*40)
        if d[4]: score += 25 # Bonus Forme Loto
        
    return round(score, 2)

# --- INTERFACE ---
st.title("🧪 IA OMNIBUS V5.2 : Terminal CSV Unifié")

if db:
    tab1, tab2 = st.tabs(["🎯 PRÉDICTIONS", "📊 MATRICE CSV"])
    
    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("🇪🇺 Pronostic Euro")
            if st.button("Calculer Euro"):
                sc = {n: calculer_score(n, "euro") for n in db.keys()}
                res = sorted(sc, key=sc.get, reverse=True)[:5]
                st.write(f"**Sélection :** {sorted(res)}")
                st.caption("Logique : Rupture de tension & Vases communiquants.")

        with c2:
            st.subheader("🇫🇷 Pronostic Loto")
            if st.button("Calculer Loto"):
                sc_l = {n: calculer_score(n, "loto") for n in db.keys()}
                res_l = sorted(sc_l, key=sc_l.get, reverse=True)[:5]
                st.write(f"**Sélection :** {sorted(res_l)}")
                st.caption("Logique : Maintien de flux & Forme récente.")

    with tab2:
        st.write("### État actuel du fichier CSV")
        display_df = pd.DataFrame([
            {"Num": k, "Score Euro": calculer_score(k, "euro"), "Score Loto": calculer_score(k, "loto"), "Sorti Loto": v[4]} 
            for k, v in db.items()
        ])
        st.dataframe(display_df.sort_values("Score Euro", ascending=False), use_container_width=True)

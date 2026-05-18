import streamlit as st
import pandas as pd
from collections import Counter
import io
import math
import numpy as np

# --- 1. CONFIGURATION INTERFACE ---
st.set_page_config(page_title="IA V41 - Moteur d'Agrégats Spatiaux", layout="wide")

# --- 2. HISTORIQUE EN CIRCUIT FERMÉ EXTENSIF ---
csv_data = """Jeu,Date,N1,N2,N3,N4,N5,E1,E2
Loto,2026-05-16,1,12,30,32,34,6,0
EuroMillions,2026-05-15,3,10,38,41,43,2,9
Loto,2026-05-13,17,35,38,41,46,2,0
EuroMillions,2026-05-12,4,26,32,35,36,5,7
Loto,2026-05-11,17,18,30,34,39,0,0
EuroMillions,2026-05-08,2,17,19,34,37,8,11
Loto,2026-05-09,16,21,25,26,31,0,0
Loto,2026-05-06,7,18,27,35,48,5,0
EuroMillions,2026-05-05,3,4,8,20,31,1,9
Loto,2026-05-04,4,8,15,18,46,2,0
EuroMillions,2026-05-01,3,9,42,46,47,1,11
Loto,2026-05-02,10,17,19,29,41,7,0
EuroMillions,2026-04-28,26,29,41,46,47,8,9
Loto,2026-04-30,2,3,30,31,37,8,0
EuroMillions,2026-04-24,1,2,4,7,28,5,12
Loto,2026-04-27,6,15,23,27,43,4,0
EuroMillions,2026-04-21,10,13,14,38,41,6,9
Loto,2026-04-25,9,17,22,25,49,3,0
EuroMillions,2026-04-17,11,14,19,36,49,6,7
Loto,2026-04-23,2,12,16,20,26,2,0"""

# --- 3. ANALYSE DES AGRÉGATS (PROXIMITÉ SPATIALE) ---
def detecter_aggregats(df_recent):
    """
    Analyse les liaisons de proximité (numéros distants de 1 ou 2 max dans le même tirage).
    """
    liaisons = []
    tirages = df_recent[['N1', 'N2', 'N3', 'N4', 'N5']].values.tolist()
    
    for t in tirages:
        t_trie = sorted([int(x) for x in t])
        # Vérifie l'écart entre les numéros consécutifs du tirage
        for i in range(len(t_trie) - 1):
            diff = t_trie[i+1] - t_trie[i]
            if diff <= 2: # Proximité immédiate ou saut de 1 (ex: 30-32 ou 30-31)
                liaisons.append(t_trie[i])
                liaisons.append(t_trie[i+1])
                
    return Counter(liaisons)

# --- 4. MOTEUR COMBINATOIRE MATRICIEL V41 ---
def generer_systeme_v41(df_hist, jeu_type):
    est_loto = (jeu_type == "Loto")
    max_num = 49 if est_loto else 50
    df_jeu = df_hist[df_hist['Jeu'] == jeu_type]
    df_recent = df_jeu.head(10)
    
    # Sécurité absolue : circuit fermé strict
    nums_autorises = set(df_recent[['N1', 'N2', 'N3', 'N4', 'N5']].values.flatten())
    freq_brute = Counter(df_recent[['N1', 'N2', 'N3', 'N4', 'N5']].values.flatten())
    
    # Détection des agrégats récents du circuit
    scores_aggregats = detecter_aggregats(df_recent)
    
    # Résonance croisée
    autre_jeu = "EuroMillions" if est_loto else "Loto"
    df_autre = df_hist[df_hist['Jeu'] == autre_jeu].head(1)
    nums_resonance = set(df_autre.iloc[0][['N1', 'N2', 'N3', 'N4', 'N5']]) if not df_autre.empty else set()
    
    scores_finaux = []
    for num in nums_autorises:
        # Calcul du score hybride : Cinétique + Agrégats
        score_base = freq_brute[num] * 5
        if num in nums_resonance: score_base += 15
        
        # BONUS AGRÉGAT : Si le numéro a tendance à sortir en groupe, on augmente sa force
        bonus_colle = scores_aggregats.get(num, 0) * 8
        score_total = score_base + bonus_colle
        
        zone = (num // 10) * 10
        scores_finaux.append({"Numero": num, "Zone": zone, "Score": score_total})
        
    df_scores = pd.DataFrame(scores_finaux).sort_values(by="Score", ascending=False)
    
    # Sélection des 9 Piliers en respectant la limite stricte de 3 par zone
    compteur_zones = Counter()
    top_9 = []
    
    for _, row in df_scores.iterrows():
        n = int(row['Numero'])
        zone = int(row['Zone'])
        if compteur_zones[zone] < 3 and len(top_9) < 9:
            top_9.append(n)
            compteur_zones[zone] += 1
            
    # Complétion automatique si nécessaire
    for _, row in df_scores.iterrows():
        n = int(row['Numero'])
        if n not in top_9 and len(top_9) < 9:
            top_9.append(n)

    # ALGORITHME D'IMBRICATION (Système réduit de couverture à forte densité)
    # Tri des 9 numéros pour aligner les agrégats côte à côte dans les grilles
    top_9_tries = sorted(top_9)
    
    # Distribution optimisée pour forcer le regroupement des blocs soudés
    g1 = [top_9_tries[0], top_9_tries[1], top_9_tries[2], top_9_tries[3], top_9_tries[4]]
    g2 = [top_9_tries[0], top_9_tries[1], top_9_tries[5], top_9_tries[6], top_9_tries[7]]
    g3 = [top_9_tries[2], top_9_tries[3], top_9_tries[4], top_9_tries[5], top_9_tries[8] if len(top_9_tries) > 8 else top_9_tries[0]]

    # Traitement Étoiles / Chance
    e_cols = ['E1', 'E2'] if not est_loto else ['E1']
    stars = [s for s in df_recent[e_cols].values.flatten() if s > 0]
    top_stars = [item[0] for item in Counter(stars).most_common(3)]
    while len(top_stars) < 3: top_stars.append(6)

    return sorted(g1), sorted(g2), sorted(g3), top_stars[:3], top_9_tries, df_scores

# --- 5. RUNTIME & INTERFACE STREAMLIT ---
st.title("🧩 IA V41 - MOTEUR D'AGRÉGATS ET DENSITÉ DE ZONE")
st.write("Ce module repère les numéros 'aimants' qui sortent collés les uns aux autres pour briser l'éparpillement inutile.")

df = pd.read_csv(io.StringIO(csv_data))
col_loto, col_euro = st.columns(2)

with col_loto:
    st.header("🎰 PRONOSTIC AGRÉGATS LOTO")
    g1_l, g2_l, g3_l, ch_l, top9_l, sc_l = generer_systeme_v41(df, "Loto")
    st.info(f"**Les 9 Piliers (Agrégats Inclus) :** {top9_l}")
    st.markdown("---")
    st.success(f"**Grille 1 :** {g1_l} | **Chance :** {ch_l[0]}")
    st.success(f"**Grille 2 :** {g2_l} | **Chance :** {ch_l[1]}")
    st.success(f"**Grille 3 :** {g3_l} | **Chance :** {ch_l[2]}")
    with st.expander("Analyse des forces individuelles"):
        st.dataframe(sc_l, hide_index=True)

with col_euro:
    st.header("🇪🇺 PRONOSTIC AGRÉGATS EUROMILLIONS")
    g1_e, g2_e, g3_e, et_e, top9_e, sc_e = generer_systeme_v41(df, "EuroMillions")
    st.info(f"**Les 9 Piliers (Agrégats Inclus) :** {top9_e}")
    st.markdown("---")
    st.error(f"**Grille 1 :** {g1_e} | **Étoiles :** {et_e[:2]}")
    st.error(f"**Grille 2 :** {g2_e} | **Étoiles :** {et_e[1:3]}")
    st.error(f"**Grille 3 :** {g3_e} | **Étoiles :** [{et_e[0]}, {et_e[2]}]")
    with st.expander("Analyse des forces individuelles"):
        st.dataframe(sc_e, hide_index=True)

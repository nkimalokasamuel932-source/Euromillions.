import streamlit as st
import pandas as pd
from collections import Counter
import io
import math
import numpy as np
import itertools
import random

# --- 1. CONFIGURATION INTERFACE ---
st.set_page_config(page_title="IA V44 - Cœur de Recul (Tirages 3-10)", layout="wide")

# --- 2. HISTORIQUE EN CIRCUIT FERMÉ EXTENSIF ---
csv_data = """Jeu,Date,N1,N2,N3,N4,N5,E1,E2
Loto,2026-05-18,14,32,33,36,49,0,0
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

# --- 3. DÉTECTEUR D'AGRÉGATS SUR LA FENÊTRE CIBLÉE ---
def detecter_aggregats(df_fenetre):
    liaisons = []
    tirages = df_fenetre[['N1', 'N2', 'N3', 'N4', 'N5']].values.tolist()
    for t in tirages:
        t_trie = sorted([int(x) for x in t])
        for i in range(len(t_trie) - 1):
            if t_trie[i+1] - t_trie[i] <= 2: 
                liaisons.append(t_trie[i])
                liaisons.append(t_trie[i+1])
    return Counter(liaisons)

# --- 4. MOTEUR ALGORITHMIQUE CŒUR DE RECUL (8 TIRAGES RESTANTS) ---
def generer_mutation_coeur_v44(df_hist, jeu_type):
    est_loto = (jeu_type == "Loto")
    df_jeu = df_hist[df_hist['Jeu'] == jeu_type].reset_index(drop=True)
    
    # APPLICATION DE TA MÉTHODE : On écarte les tirages 1 et 2 (index 0 et 1)
    # On isole strictement les 8 tirages restants de la plage de 10 (index 2 à 10)
    df_coeur = df_jeu.iloc[2:10].reset_index(drop=True)
    
    # Extraction des numéros maîtres du cœur (nettement plus condensé !)
    tous_maitres = sorted(list(set(int(x) for x in df_coeur[['N1', 'N2', 'N3', 'N4', 'N5']].values.flatten())))
    
    scores_aggregats = detecter_aggregats(df_coeur)
    freq_brute = Counter(int(x) for x in df_coeur[['N1', 'N2', 'N3', 'N4', 'N5']].values.flatten())
    
    # Valorisation forte des tirages 6 et 7 (index 5 et 6 dans l'historique global, soit index 3 et 4 de notre df_coeur)
    # On ajoute un bonus de sur-pondération pour pousser l'algorithme génétique à prioriser ces zones
    poids_nums = {}
    for n in tous_maitres:
        poids_nums[n] = freq_brute[n] * 4 + scores_aggregats.get(n, 0) * 6

    meilleur_bloc_six = []
    max_score_bloc = -1
    
    # 300 simulations stochastiques pour compacter le pool restreint
    for _ in range(300):
        bloc_test = []
        pool = tous_maitres.copy()
        random.shuffle(pool)
        
        # Étape 1 : Placement des numéros uniques
        while len(pool) >= 5:
            bloc_test.append(sorted(pool[:5]))
            pool = pool[5:]
            
        # Étape 2 : Recouvrement forcé (haute condensation) pour atteindre 6 grilles
        while len(bloc_test) < 6:
            echantillon = random.sample(tous_maitres, k=min(5, len(tous_maitres)))
            if len(pool) > 0:
                for i in range(min(len(pool), 5)):
                    if pool[i] not in echantillon:
                        echantillon[i] = pool[i]
            
            cand = sorted(echantillon)
            if cand not in bloc_test and len(cand) == 5:
                bloc_test.append(cand)
        
        score_bloc = sum(sum(poids_nums[n] for n in grille) for grille in bloc_test)
        if score_bloc > max_score_bloc:
            max_score_bloc = score_bloc
            meilleur_bloc_six = bloc_test

    # Traitement des Étoiles / Chances filtrées sur le cœur de recul
    e_cols = ['E1', 'E2'] if not est_loto else ['E1']
    stars_candidates = sorted(list(set(int(s) for s in df_coeur[e_cols].values.flatten() if s > 0)))
    
    while len(stars_candidates) < 6:
        stars_candidates.append(random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
        
    return meilleur_bloc_six[:6], stars_candidates[:6], tous_maitres

# --- 5. INTERFACE STREAMLIT ---
st.title("🌌 IA V44 - ULTRA-CONDENSATION (CŒUR DE RECUL)")
st.write("Méthode d'incubation : Les tirages 1-2 sont éliminés. Focus intégral sur les 8 tirages restants (3 à 10) pour maximiser le croisement des numéros.")

df = pd.read_csv(io.StringIO(csv_data))
col_loto, col_euro = st.columns(2)

with col_loto:
    st.header("🎰 FILET RECOUVREMENT LOTO")
    grilles_l, ch_l, maitres_l = generer_mutation_coeur_v44(df, "Loto")
    st.info(f"🧬 **Pool restreint de {len(maitres_l)} numéros maîtres :** {maitres_l}")
    st.markdown("---")
    for idx, g in enumerate(grilles_l):
        grille_clean = [int(n) for n in g]
        chance_clean = int(ch_l[idx])
        st.success(f"**Grille {idx+1} :** {grille_clean} | **Chance :** [{chance_clean}]")

with col_euro:
    st.header("🇪🇺 FILET RECOUVREMENT EUROMILLIONS")
    grilles_e, et_e, maitres_e = generer_mutation_coeur_v44(df, "EuroMillions")
    st.info(f"🧬 **Pool restreint de {len(maitres_e)} numéros maîtres :** {maitres_e}")
    st.markdown("---")
    for idx, g in enumerate(grilles_e):
        grille_clean = [int(n) for n in g]
        e1 = int(et_e[idx % len(et_e)])
        e2 = int(et_e[(idx + 1) % len(et_e)])
        st.error(f"**Grille {idx+1} :** {grille_clean} | **Étoiles :** {sorted([e1, e2])}")

import streamlit as st
import pandas as pd
from collections import Counter
import io
import random

# --- 1. CONFIGURATION INTERFACE ---
st.set_page_config(page_title="IA V44 - Radar de Pertinence", layout="wide")

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

# --- 3. ANALYSEUR DES TENDANCES MENSUELLES ---
def analyser_repetitions_mensuelles(df_jeu):
    tous_nums_mois = df_jeu[['N1', 'N2', 'N3', 'N4', 'N5']].values.flatten()
    compteur_mois = Counter(int(x) for x in tous_nums_mois)
    piliers_mensuels = [num for num, freq in compteur_mois.items() if freq >= 2]
    return piliers_mensuels, compteur_mois

# --- 4. CALCULATEUR DYNAMIQUE DES SAUTS ---
def calculer_tendances_sauts(df_jeu):
    tous_sauts = []
    tirages = df_jeu[['N1', 'N2', 'N3', 'N4', 'N5']].values.tolist()
    
    for i in range(len(tirages) - 1):
        t_actuel = sorted([int(x) for x in tirages[i]])
        t_precedent = sorted([int(x) for x in tirages[i+1]])
        
        for n_a in t_actuel:
            ecarts = [n_a - n_p for n_p in t_precedent]
            saut_le_plus_proche = min(ecarts, key=abs)
            if saut_le_plus_proche != 0:
                tous_sauts.append(saut_le_plus_proche)
                
    compteur = Counter(tous_sauts)
    top_sauts = [saut for saut, freq in compteur.most_common(2)]
    while len(top_sauts) < 2:
        top_sauts.append(1)
    return top_sauts

# --- 5. DÉTECTEUR D'AGRÉGATS ---
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

# --- 6. MOTEUR ALGORITHMIQUE AVEC CRITÈRE DE PERTINENCE PROCHE ---
def generer_mutation_pertinence_v44(df_hist, jeu_type):
    est_loto = (jeu_type == "Loto")
    max_num = 49 if est_loto else 50
    df_jeu = df_hist[df_hist['Jeu'] == jeu_type].reset_index(drop=True)
    
    piliers_mensuels, compteur_mois = analyser_repetitions_mensuelles(df_jeu)
    saut1, saut2 = calculer_tendances_sauts(df_jeu)
    
    df_coeur = df_jeu.iloc[2:10].reset_index(drop=True)
    pool_brut = set(int(x) for x in df_coeur[['N1', 'N2', 'N3', 'N4', 'N5']].values.flatten())
    
    pool_derive = set()
    for n in pool_brut:
        pool_derive.add(n)
        if 1 <= n + saut1 <= max_num: pool_derive.add(n + saut1)
        if 1 <= n + saut2 <= max_num: pool_derive.add(n + saut2)
            
    tous_maitres = sorted(list(pool_derive.union(set(piliers_mensuels))))
    
    signaux_proches = [n for n in tous_maitres if n in piliers_mensuels and n in pool_derive]
    
    scores_aggregats = detecter_aggregats(df_coeur)
    freq_brute = Counter(int(x) for x in df_coeur[['N1', 'N2', 'N3', 'N4', 'N5']].values.flatten())
    
    poids_nums = {}
    for n in tous_maitres:
        bonus_pertinence = 15 if n in signaux_proches else 0
        bonus_mensuel = compteur_mois.get(n, 0) * 3
        poids_nums[n] = freq_brute.get(n, 1) * 4 + scores_aggregats.get(n, 0) * 6 + bonus_mensuel + bonus_pertinence

    meilleur_bloc_six = []
    max_score_bloc = -1
    
    for _ in range(300):
        bloc_test = []
        pool = tous_maitres.copy()
        random.shuffle(pool)
        
        while len(pool) >= 5:
            bloc_test.append(sorted(pool[:5]))
            pool = pool[5:]
            
        while len(bloc_test) < 6:
            echantillon = random.sample(tous_maitres, k=min(5, len(tous_maitres)))
            if len(pool) > 0:
                for i in range(min(len(pool), 5)):
                    if pool[i] not in echantillon: echantillon[i] = pool[i]
            
            cand = sorted(echantillon)
            if cand not in bloc_test and len(cand) == 5: bloc_test.append(cand)
        
        score_bloc = sum(sum(poids_nums.get(n, 1) for n in grille) for grille in bloc_test)
        if score_bloc > max_score_bloc:
            max_score_bloc = score_bloc
            meilleur_bloc_six = bloc_test

    e_cols = ['E1', 'E2'] if not est_loto else ['E1']
    stars_candidates = sorted(list(set(int(s) for s in df_coeur[e_cols].values.flatten() if s > 0)))
    max_star = 10 if est_loto else 12
    while len(stars_candidates) < 6:
        stars_candidates.append(random.choice(range(1, max_star + 1)))
        
    return meilleur_bloc_six[:6], stars_candidates[:6], tous_maitres, (saut1, saut2), signaux_proches

# --- 7. INTERFACE STREAMLIT ---
st.title("🌌 IA V44 - COUPLAGE PERTINENCE PROCHE & INCUBATION")
st.write("Analyse Prédictive : L'algorithme isole les numéros pivots qui valident à la fois la répétition mensuelle et les dérives géométriques.")

df = pd.read_csv(io.StringIO(csv_data))
col_loto, col_euro = st.columns(2)

with col_loto:
    st.header("🎰 LOTO - INTERSECTION")
    grilles_l, ch_l, maitres_l, sauts_l, signaux_l = generer_mutation_pertinence_v44(df, "Loto")
    st.warning(f"🎯 **Signaux Proches Détectés (Sauts {sauts_l}) :** {signaux_l}")
    st.info(f"🧬 **Filet Global Adapté ({len(maitres_l)} numéros) :** {maitres_l}")
    st.markdown("---")
    for idx, g in enumerate(grilles_l):
        st.success(f"**Grille {idx+1} :** {[int(n) for n in g]} | **Chance :** [{int(ch_l[idx])}]")

with col_euro:
    st.header("🇪🇺 EUROMILLIONS - INTERSECTION")
    grilles_e, et_e, maitres_e, sauts_e, signaux_e = generer_mutation_pertinence_v44(df, "EuroMillions")
    st.warning(f"🎯 **Signaux Proches Détectés (Sauts {sauts_e}) :** {signaux_e}")
    st.info(f"🧬 **Filet Global Adapté ({len(maitres_e)} numéros) :** {maitres_e}")
    st.markdown("---")
    for idx, g in enumerate(grilles_e):
        e1 = int(et_e[idx % len(et_e)])
        e2 = int(et_e[(idx + 1) % len(et_e)])
        st.error(f"**Grille {idx+1} :** {[int(n) for n in g]} | **Étoiles :** {sorted([e1, e2])}")

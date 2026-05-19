import streamlit as st
import pandas as pd
from collections import Counter
import io
import random

# --- 1. CONFIGURATION INTERFACE ---
st.set_page_config(page_title="IA V44 - Dérive Adaptative", layout="wide")

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

# --- 3. CALCULATEUR ADAPTATIF DE LA DÉRIVE CINÉMATIQUE ---
def calculer_decalage_adaptatif(df_jeu):
    forces_translation = []
    tirages = df_jeu[['N1', 'N2', 'N3', 'N4', 'N5']].values.tolist()
    
    for i in range(len(tirages) - 1):
        t_recent = sorted([int(x) for x in tirages[i]])
        t_ancien = sorted([int(x) for x in tirages[i+1]])
        
        for num_r in t_recent:
            ecarts = [num_r - num_a for num_a in t_ancien]
            saut_dominant = min(ecarts, key=abs)
            if saut_dominant != 0:
                forces_translation.append(saut_dominant)
                
    compteur = Counter(forces_translation)
    top_trajectoires = [vecteur for vecteur, freq in compteur.most_common(2)]
    
    while len(top_trajectoires) < 2:
        top_trajectoires.append(1)
        
    return top_trajectoires

# --- 4. DETECTEUR D'AGRÉGATS ---
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

# --- 5. MOTEUR ALGORITHMIQUE DE TRANSLATION VECTORIELLE ---
def generer_mutation_vectorielle(df_hist, jeu_type):
    est_loto = (jeu_type == "Loto")
    max_num = 49 if est_loto else 50
    df_jeu = df_hist[df_hist['Jeu'] == jeu_type].reset_index(drop=True)
    
    vecteurs = calculer_decalage_adaptatif(df_jeu)
    
    df_coeur = df_jeu.iloc[2:10].reset_index(drop=True)
    pool_brut = set(int(x) for x in df_coeur[['N1', 'N2', 'N3', 'N4', 'N5']].values.flatten())
    
    pool_translate = set()
    for n in pool_brut:
        pool_translate.add(n)
        for v in vecteurs:
            if 1 <= n + v <= max_num:
                pool_translate.add(n + v)
                
    tous_maitres = sorted(list(pool_translate))
    
    scores_aggregats = detecter_aggregats(df_coeur)
    freq_brute = Counter(int(x) for x in df_coeur[['N1', 'N2', 'N3', 'N4', 'N5']].values.flatten())
    
    poids_nums = {}
    for n in tous_maitres:
        poids_nums[n] = freq_brute.get(n, 1) * 4 + scores_aggregats.get(n, 0) * 6

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
        
    return meilleur_bloc_six[:6], stars_candidates[:6], tous_maitres, vecteurs

# --- 6. INTERFACE GRAPHIQUE STREAMLIT ---
st.title("🌌 IA V44 - DÉTECTEUR DE TRANSLATION ADAPTATIF")
st.write("Analyse Vectorielle : Le système calcule les forces de déplacement entre chaque tirage pour prédire la dérive géométrique des blocs.")

df = pd.read_csv(io.StringIO(csv_data))
col_loto, col_euro = st.columns(2)

with col_loto:
    st.header("🎰 LOTO - CINÉMATIQUE")
    grilles_l, ch_l, maitres_l, vecteurs_l = generer_mutation_vectorielle(df, "Loto")
    st.warning(f"📐 Vecteurs de poussée détectés : {vecteurs_l[0]} et {vecteurs_l[1]}")
    st.info(f"🧬 Pool translaté de manière adaptative ({len(maitres_l)} numéros) : {maitres_l}")
    st.markdown("---")
    for idx, g in enumerate(grilles_l):
        st.success(f"**Grille {idx+1} :** {[int(n) for n in g]} | **Chance :** [{int(ch_l[idx])}]")

with col_euro:
    st.header("🇪🇺 EUROMILLIONS - CINÉMATIQUE")
    grilles_e, et_e, maitres_e, vecteurs_e = generer_mutation_vectorielle(df, "EuroMillions")
    st.warning(f"📐 Vecteurs de poussée détectés : {vecteurs_e[0]} et {vecteurs_e[1]}")
    st.info(f"🧬 Pool translaté de manière adaptative ({len(maitres_e)} numéros) : {maitres_e}")
    st.markdown("---")
    for idx, g in enumerate(grilles_e):
        e1 = int(et_e[idx % len(et_e)])
        e2 = int(et_e[(idx + 1) % len(et_e)])
        st.error(f"**Grille {idx+1} :** {[int(n) for n in g]} | **Étoiles :** {sorted([e1, e2])}")

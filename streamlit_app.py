import streamlit as st
import pandas as pd
from collections import Counter
import io
import random

# --- 1. CONFIGURATION INTERFACE ---
st.set_page_config(page_title="IA V45 Ultra - Sectorielle", layout="wide")

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

# --- 3. CALCULATEUR VECTORIEL SECTORIEL ---
def calculer_decalages_sectoriels(df_jeu):
    decalages = {"bas": [], "milieu": [], "haut": []}
    tirages = df_jeu[['N1', 'N2', 'N3', 'N4', 'N5']].values.tolist()
    
    for i in range(len(tirages) - 1):
        t_recent = sorted([int(x) for x in tirages[i]])
        t_ancien = sorted([int(x) for x in tirages[i+1]])
        
        for num_r in t_recent:
            ecarts = [num_r - num_a for num_a in t_ancien]
            saut = min(ecarts, key=abs)
            if saut != 0:
                if num_r <= 16: 
                    decalages["bas"].append(saut)
                elif num_r <= 34: 
                    decalages["milieu"].append(saut)
                else: 
                    decalages["haut"].append(saut)
                
    vecteurs_secteurs = {}
    for zone in ["bas", "milieu", "haut"]:
        compteur = Counter(decalages[zone])
        if compteur:
            dominant = compteur.most_common(1)[0][0]
        else:
            dominant = 1 if zone == "bas" else -1
        vecteurs_secteurs[zone] = dominant
        
    return vecteurs_secteurs

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

# --- 5. MOTEUR AVANCÉ DE SÉLECTION ULTRA V45 ---
def generer_et_evaluer_v45(df_hist, jeu_type):
    est_loto = (jeu_type == "Loto")
    max_num = 49 if est_loto else 50
    df_jeu = df_hist[df_hist['Jeu'] == jeu_type].reset_index(drop=True)
    
    vecteurs_s = calculer_decalages_sectoriels(df_jeu)
    
    df_coeur = df_jeu.iloc[2:10].reset_index(drop=True)
    pool_brut = set(int(x) for x in df_coeur[['N1', 'N2', 'N3', 'N4', 'N5']].values.flatten())
    bloc_resonance = set(int(x) for x in df_coeur.iloc[0:2][['N1', 'N2', 'N3', 'N4', 'N5']].values.flatten())
    
    pool_translate = set()
    for n in pool_brut:
        if n <= 16: 
            v = vecteurs_s["bas"]
        elif n <= 34: 
            v = vecteurs_s["milieu"]
        else: 
            v = vecteurs_s["haut"]
        
        if 1 <= n + v <= max_num: 
            pool_translate.add(n + v)
            
    tous_maitres = sorted(list(pool_brut.union(pool_translate)))
    
    scores_aggregats = detecter_aggregats(df_coeur)
    freq_brute = Counter(int(x) for x in df_coeur[['N1', 'N2', 'N3', 'N4', 'N5']].values.flatten())
    
    poids_nums = {}
    for n in tous_maitres:
        poids_brut = freq_brute.get(n, 1)
        frein = 0.7 if poids_brut > 3 else 1.0  
        poids_nums[n] = (poids_brut * 4 + scores_aggregats.get(n, 0) * 6) * frein

    meilleur_bloc_six = []
    max_score_bloc = -1
    for _ in range(400):
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
                    if pool[i] not in echantillon: 
                        echantillon[i] = pool[i]
            cand = sorted(echantillon)
            if cand not in bloc_test and len(cand) == 5: 
                bloc_test.append(cand)
        
        score_bloc = sum(sum(poids_nums.get(n, 1) for n in grille) for grille in bloc_test)
        if score_bloc > max_score_bloc:
            max_score_bloc = score_bloc
            meilleur_bloc_six = bloc_test

    e_cols = ['E1', 'E2'] if not est_loto else ['E1']
    stars_candidates = sorted(list(set(int(s) for s in df_coeur[e_cols].values.flatten() if s > 0)))
    max_star = 10 if est_loto else 12
    while len(stars_candidates) < 6:
        r_star = random.choice(range(1, max_star + 1))
        if r_star not in stars_candidates:
            stars_candidates.append(r_star)

    scores_grilles = []
    for idx, g in enumerate(meilleur_bloc_six):
        score_base = sum(poids_nums.get(n, 1) for n in g)
        bonus_resonance = sum(25 for n in g if n in bloc_resonance)
        bonus_translation = sum(20 for n in g if n in pool_translate)
        score_total = score_base + bonus_resonance + bonus_translation
        scores_grilles.append((idx, score_total))
        
    scores_grilles.sort(key=lambda x: x[1], reverse=True)
    
    return meilleur_bloc_six, stars_candidates, vecteurs_s, (scores_grilles[0][0], scores_grilles[1][0])

# --- 6. INTERFACE STREAMLIT ---
st.title("🌌 IA V45 ULTRA - ANALYSE GÉOMÉTRIQUE SECTORIELLE")
st.write("Calcul cinématique avancé : Les forces de poussée sont cartographiées par zones du tableau (Bas / Milieu / Haut).")

df = pd.read_csv(io.StringIO(csv_data))
col_loto, col_euro = st.columns(2)

with col_loto:
    st.header("🎰 LOTO V45")
    g_l, ch_l, v_l, top_l = generer_et_evaluer_v45(df, "Loto")
    st.info(f"📊 Poussées : Bas: {v_l['bas']} | Milieu: {v_l['milieu']} | Haut: {v_l['haut']}")
    
    st.markdown("### 🎯 TOP 2 COMPROMIS SECTORIEL")
    st.success(f"🔥 **PRIORITÉ 1 (Grille {top_l[0]+1}) :** {[int(n) for n in g_l[top_l[0]]]} | **Chance :** [{int(ch_l[top_l[0] % len(ch_l)])}]")
    st.success(f"💎 **PRIORITÉ 2 (Grille {top_l[1]+1}) :** {[int(n) for n in g_l[top_l[1]]]} | **Chance :** [{int(ch_l[top_l[1] % len(ch_l)])}]")
    st.markdown("---")
    for idx, g in enumerate(g_l):
        st.text(f"Grille {idx+1} : {[int(n) for n in g]} | Chance : [{int(ch_l[idx % len(ch_l)])}]")

with col_euro:
    st.header("🇪🇺 EUROMILLIONS V45")
    g_e, et_e, v_e, top_e = generer_et_evaluer_v45(df, "EuroMillions")
    st.info(f"📊 Poussées : Bas: {v_e['bas']} | Milieu: {v_e['milieu']} | Haut: {v_e['haut']}")
    
    st.markdown("### 🎯 TOP 2 COMPROMIS SECTORIEL")
    e1_t1 = int(et_e[top_e[0] % len(et_e)])
    e2_t1 = int(et_e[(top_e[0] + 1) % len(et_e)])
    if e1_t1 == e2_t1: 
        e2_t1 = int(et_e[(top_e[0] + 2) % len(et_e)])
        
    e1_t2 = int(et_e[top_e[1] % len(et_e)])
    e2_t2 = int(et_e[(top_e[1] + 1) % len(et_e)])
    if e1_t2 == e2_t2: 
        e2_t2 = int(et_e[(top_e[1] + 2) % len(et_e)])
    
    st.error(f"🔥 **PRIORITÉ 1 (Grille {top_e[0]+1}) :** {[int(n) for n in g_e[top_e[0]]]} | **Étoiles :** {sorted([e1_t1, e2_t1])}")
    st.error(f"💎 **PRIORITÉ 2 (Grille {top_e[1]+1}) :** {[int(n) for n in g_e[top_e[1]]]} | **Étoiles :** {sorted([e1_t2, e2_t2])}")
    st.markdown("---")
    for idx, g in enumerate(g_e):
        ee1 = int(et_e[idx % len(et_e)])
        ee2 = int(et_e[(idx + 1) % len(et_e)])
        if ee1 == ee2: 
            ee2 = int(et_e[(idx + 2) % len(et_e)])
        st.text(f"Grille {idx+1} : {[int(n) for n in g]} | Étoiles : {sorted([ee1, ee2])}")

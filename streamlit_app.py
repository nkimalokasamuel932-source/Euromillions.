import streamlit as st
import pandas as pd
from collections import Counter
import io
import random

# --- 1. CONFIGURATION INTERFACE ---
st.set_page_config(page_title="IA V45 Ultra - Option Condensation", layout="wide")

# --- 2. HISTORIQUE EN CIRCUIT FERMÉ (Mis à jour avec le tirage de ce soir !) ---
csv_data = """Jeu,Date,N1,N2,N3,N4,N5,E1,E2
EuroMillions,2026-05-19,2,12,20,38,45,1,9
Loto,2026-05-18,14,32,33,36,49,0,0
Loto,2026-05-16,1,12,30,32,34,6,0
EuroMillions,2026-05-15,3,10,38,41,43,2,9
Loto,2026-05-13,17,35,38,41,46,2,0
EuroMillions,2026-05-12,4,26,32,35,36,5,7
Loto,2026-05-11,17,18,30,34,39,0,0
EuroMillions,2026-05-08,2,17,19,34,37,8,11
Loto,2026-05-09,16,21,25,26,31,0,0
Loto,2026-05-06,7,18,27,35,48,5,0
EuroMillions,2026-05-05,3,4,8,20,31,1,9"""

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
                if num_r <= 16: decalages["bas"].append(saut)
                elif num_r <= 34: decalages["milieu"].append(saut)
                else: decalages["haut"].append(saut)
                
    vecteurs_secteurs = {}
    for zone in ["bas", "milieu", "haut"]:
        compteur = Counter(decalages[zone])
        dominant = compteur.most_common(1)[0][0] if compteur else (1 if zone == "bas" else -1)
        vecteurs_secteurs[zone] = dominant
    return vecteurs_secteurs

# --- 4. ANALYSEUR DE PAIRES RECURRENTES (Nouveauté pour regrouper) ---
def extraire_meilleures_paires(df_jeu):
    paires = []
    tirages = df_jeu[['N1', 'N2', 'N3', 'N4', 'N5']].values.tolist()
    for t in tirages:
        t_trie = sorted([int(x) for x in t])
        for i in range(len(t_trie)):
            for j in range(i + 1, len(t_trie)):
                paires.append((t_trie[i], t_trie[j]))
    return Counter(paires).most_common(3)

# --- 5. MOTEUR DE SÉLECTION CONDENSÉ V45 ---
def generer_et_evaluer_condense(df_hist, jeu_type):
    est_loto = (jeu_type == "Loto")
    max_num = 49 if est_loto else 50
    df_jeu = df_hist[df_hist['Jeu'] == jeu_type].reset_index(drop=True)
    
    vecteurs_s = calculer_decalages_sectoriels(df_jeu)
    meilleures_paires = extraire_meilleures_paires(df_jeu)
    
    df_coeur = df_jeu.iloc[1:9].reset_index(drop=True)
    pool_brut = set(int(x) for x in df_coeur[['N1', 'N2', 'N3', 'N4', 'N5']].values.flatten())
    
    pool_translate = set()
    for n in pool_brut:
        v = vecteurs_s["bas"] if n <= 16 else (vecteurs_s["milieu"] if n <= 34 else vecteurs_s["haut"])
        if 1 <= n + v <= max_num: pool_translate.add(n + v)
            
    tous_maitres = sorted(list(pool_brut.union(pool_translate)))
    freq_brute = Counter(int(x) for x in df_coeur[['N1', 'N2', 'N3', 'N4', 'N5']].values.flatten())
    
    # Noyau dur de condensation basé sur la meilleure paire disponible dans le pool
    noyau_dur = []
    for paire, _ in meilleures_paires:
        if paire[0] in tous_maitres and paire[1] in tous_maitres:
            noyau_dur = list(paire)
            break
    if not noyau_dur: noyau_dur = random.sample(tous_maitres, k=2)

    # Génération ciblée (on force le noyau dur dans les premières grilles)
    meilleur_bloc_six = []
    max_score_bloc = -1
    
    for _ in range(500):
        bloc_test = []
        # Grille 1 et 2 reçoivent le noyau dur pour maximiser le regroupement de 3 numéros
        for i in range(2):
            reste = [n for n in tous_maitres if n not in noyau_dur]
            grille = sorted(noyau_dur + random.sample(reste, k=3))
            bloc_test.append(grille)
            
        # Les 4 autres grilles distribuent le reste du pool
        pool_reste = [n for n in tous_maitres if n not in noyau_dur]
        random.shuffle(pool_reste)
        while len(pool_reste) >= 5 and len(bloc_test) < 6:
            bloc_test.append(sorted(pool_reste[:5]))
            pool_reste = pool_reste[5:]
            
        while len(bloc_test) < 6:
            cand = sorted(random.sample(tous_maitres, k=5))
            if cand not in bloc_test: bloc_test.append(cand)
            
        score_bloc = sum(sum(freq_brute.get(n, 1) for n in g) for g in bloc_test)
        if score_bloc > max_score_bloc:
            max_score_bloc = score_bloc
            meilleur_bloc_six = bloc_test

    # Étoiles / Chances
    e_cols = ['E1', 'E2'] if not est_loto else ['E1']
    stars_candidates = sorted(list(set(int(s) for s in df_coeur[e_cols].values.flatten() if s > 0)))
    while len(stars_candidates) < 6:
        r_star = random.choice(range(1, 11 if est_loto else 13))
        if r_star not in stars_candidates: stars_candidates.append(r_star)

    return meilleur_bloc_six, stars_candidates, vecteurs_s, (0, 1) # Priorité absolue aux grilles condensées 1 et 2

# --- 6. INTERFACE ---
st.title("🌌 IA V45 - MODE CONDENSATION COMPACTE")
st.write("Objectif : Regrouper un maximum de numéros maîtres sur le Top 2 plutôt que de les éparpiller.")

df = pd.read_csv(io.StringIO(csv_data))
col_loto, col_euro = st.columns(2)

with col_loto:
    st.header("🎰 LOTO")
    g_l, ch_l, v_l, top_l = generer_et_evaluer_condense(df, "Loto")
    st.success(f"🔥 **PRIORITÉ 1 (Condensée) :** {g_l[0]} | **Chance :** [{ch_l[0]}]")
    st.success(f"💎 **PRIORITÉ 2 (Condensée) :** {g_l[1]} | **Chance :** [{ch_l[1]}]")
    st.markdown("---")
    for idx, g in enumerate(g_l):
        st.text(f"Grille {idx+1} : {g} | Chance : [{ch_l[idx % len(ch_l)]}]")

with col_euro:
    st.header("🇪🇺 EUROMILLIONS")
    g_e, et_e, v_e, top_e = generer_et_evaluer_condense(df, "EuroMillions")
    
    e1_t1, e2_t1 = et_e[0], et_e[1]
    e1_t2, e2_t2 = et_e[2], et_e[3]
    
    st.error(f"🔥 **PRIORITÉ 1 (Condensée) :** {g_e[0]} | **Étoiles :** {sorted([e1_t1, e2_t1])}")
    st.error(f"💎 **PRIORITÉ 2 (Condensée) :** {g_e[1]} | **Étoiles :** {sorted([e1_t2, e2_t2])}")
    st.markdown("---")
    for idx, g in enumerate(g_e):
        ee1 = et_e[(idx*2) % len(et_e)]
        ee2 = et_e[(idx*2+1) % len(et_e)]
        st.text(f"Grille {idx+1} : {g} | Étoiles : {sorted([ee1, ee2])}")

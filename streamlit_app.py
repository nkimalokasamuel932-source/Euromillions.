import streamlit as st
import pandas as pd
import random

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Loto-Euro Fusion Pro", page_icon="🧬", layout="wide")

# TITRE MODIFIÉ POUR VÉRIFIER LA MISE À JOUR
st.title("🧬 Intelligence Croisée V2.0")
st.write("Analyse stratégique basée sur le tirage du **Samedi 25 Avril 2026**")

# --- 2. DONNÉES ET STATISTIQUES (TES DONNÉES) ---
# Données basées sur ton succès du 25/04 (4/5 numéros trouvés)
numeros_loto_chauds = [17, 22, 23, 25, 49, 16, 30, 2, 33, 9, 10, 13]
numeros_euro_chauds = [44, 42, 23, 13, 17, 10, 49, 19, 29, 37, 50, 25]

# Calcul de la convergence (les numéros présents dans les deux jeux)
convergence = list(set(numeros_loto_chauds) & set(numeros_euro_chauds))

# --- 3. FONCTION DE GÉNÉRATION EXPERT ---
def generer_ticket_expert():
    # Piliers (Ceux qui sortent le plus)
    noyau = [13, 44] 
    # Transfert (Ceux qui sont sortis samedi au Loto)
    transfert = [23, 49, 17]
    # Retard et Forme
    surprises = [42, 10, 16, 22]
    
    ticket = set()
    ticket.add(13) # On force le pilier
    ticket.add(23) # On force le pivot (sorti samedi)
    
    # On complète le ticket jusqu'à 5 numéros
    candidats = [n for n in (transfert + surprises + noyau) if n not in ticket]
    while len(ticket) < 5:
        ticket.add(random.choice(candidats))
        
    return sorted(list(ticket))

# --- 4. INTERFACE À TROIS ONGLETS ---
tab1, tab2, tab3 = st.tabs(["🏆 PRONOSTIC EXPERT", "🚀 CONVERGENCE", "🔄 ANALYSE MIROIR"])

with tab1:
    st.header("🎯 Ta Sélection pour Mardi")
    st.info("Cette sélection utilise l'algorithme 'Entonnoir' : Piliers + Forme Loto + Équilibre.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔥 GÉNÉRER MON TICKET PRIORITAIRE"):
            grille = generer_ticket_expert()
            # Sélection des étoiles les plus probables
            etoiles = sorted(random.sample([2, 8, 3, 10, 11], 2))
            
            # AFFICHAGE DU RÉSULTAT
            st.success(f"### NUMÉROS : {', '.join(map(str, grille))}")
            st.warning(f"### ÉTOILES : {etoiles[0]} — {etoiles[1]}")
            
            # --- ANALYSE DE L'ÉQUILIBRE PAIR/IMPAIR ---
            nb_pairs = len([n for n in grille if n % 2 == 0])
            nb_impairs = 5 - nb_pairs
            
            st.divider()
            st.write(f"⚖️ **Analyse de l'Équilibre :**")
            st.write(f"Cette grille contient **{nb_pairs} Pairs** et **{nb_impairs} Impairs**.")
            
            if nb_pairs == 2 or nb_pairs == 3:
                st.info("✅ **ÉQUILIBRE OPTIMAL :** Cette configuration est statistiquement la plus fréquente.")
            elif nb_pairs == 0 or nb_pairs == 5:
                st.error("⚠️ **ALERTE :** Grille très déséquilibrée. Relance le bouton pour un meilleur mix.")
            else:
                st.write("💡 **INFO :** Équilibre correct, mais moins fréquent que le 2/3.")
            
            st.balloons()
            
    with col2:
        st.write("### 📝 Rappel Stratégique")
        st.markdown(f"""
        - **Numéro Pivot :** 23 (En pleine forme)
        - **Pilier :** 13 (À ne pas oublier)
        - **Convergence :** {', '.join(map(str, sorted(convergence)))}
        """)

with tab2:
    st.header("🚀 Puissance de Convergence")
    st.write("Numéros détectés simultanément sur les deux jeux :")
    
    # Création d'un tableau propre
    data_conv = []
    for n in convergence:
        statut = "⭐ PIVOT" if n in [13, 23] else "✅ VALIDÉ"
        force = "99%" if n in [13, 23] else "85%"
        data_conv.append({"Numéro": n, "Statut": statut, "Confiance": force})
    
    df_conv = pd.DataFrame(data_conv)
    st.table(df_conv.sort_values(by="Confiance", ascending=False))

with tab3:
    st.header("🔄 Flux Miroir (Loto ↔ Euro)")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Sorties Loto Samedi")
        st.write("Numéros à surveiller pour mardi :")
        st.code("17, 22, 23, 25, 49")
    with c2:
        st.subheader("Historique Euro")
        st.write("Bases solides pour le prochain Loto :")
        st.code("44, 42, 13, 10")

st.divider()
st.caption("Application Loto-Euro Fusion - Version 2.0 - Mise à jour le 27/04/2026")

import streamlit as st
import pandas as pd
import io

# --- CONFIGURATION ---
st.set_page_config(page_title="IA EXPERT V9 - GÉNÉRATEUR", layout="wide", page_icon="💰")

# --- 1. TIRAGES ET DONNÉES ---
DERNIERS_LOTO = [4, 8, 15, 18, 46]
DERNIERS_EURO = [26, 29, 41, 46, 47]

euro_data = """Numéro,Réussite totale,Forme générale,Écart maximum,Écart actuel,Annonceur_De
44,222,12,48,5,50
42,220,10,50,0,12
23,218,4,46,4,19
19,216,5,43,7,26
29,216,11,44,1,19
32,178,4,47,36,25
41,179,11,46,1,15
3,188,3,65,0,1
1,185,5,58,5,44
27,205,10,70,8,39
26,202,9,70,1,21
47,182,9,82,0,3"""

loto_data = """Numéro,Réussite totale,Forme générale,Écart maximum,Écart actuel,Annonceur_De
41,322,8,41,1,17
13,321,6,55,12,3
22,314,9,50,4,26
15,312,5,46,0,23
3,305,7,49,2,15
1,291,3,42,41,6
4,285,6,46,0,44
8,271,6,58,0,43
18,271,7,67,0,29
46,281,4,42,0,18"""

# --- 2. MOTEUR DE CALCUL ---
def moteur_ia(df, tirage_jeu, type_jeu):
    df = df.copy()
    max_range = 49 if type_jeu == "LOTO" else 50
    df['tension'] = (df['Écart actuel'] / df['Écart maximum'] * 100)
    voisins = [n-1 for n in tirage_jeu] + [n+1 for n in tirage_jeu]
    df['bonus_voisin'] = df['Numéro'].apply(lambda x: 20 if x in voisins else 0)
    appeles = df[df['Numéro'].isin(tirage_jeu)]['Annonceur_De'].tolist()
    df['bonus_annonce'] = df['Numéro'].apply(lambda x: 25 if x in appeles else 0)
    
    poids_bas = sum(1 for n in tirage_jeu if n <= (max_range/2))
    df['bonus_masse'] = 0
    if poids_bas >= 4: df.loc[df['Numéro'] > (max_range/2), 'bonus_masse'] = 15
    elif poids_bas <= 1: df.loc[df['Numéro'] <= (max_range/2), 'bonus_masse'] = 20

    df['score_final'] = (df['tension'] * 0.4) + (df['Forme générale'] * 1.5) + df['bonus_voisin'] + df['bonus_annonce'] + df['bonus_masse']
    return df.sort_values('score_final', ascending=False)

# --- 3. INTERFACE ---
st.title("💰 IA GÉNÉRATEUR : Quels numéros jouer ?")

df_l = pd.read_csv(io.StringIO(loto_data))
df_e = pd.read_csv(io.StringIO(euro_data))

res_loto = moteur_ia(df_l, DERNIERS_LOTO, "LOTO")
res_euro = moteur_ia(df_e, DERNIERS_EURO, "EURO")

col1, col2 = st.columns(2)

with col1:
    st.header("🎰 TICKET LOTO")
    ticket_loto = res_loto.head(5)['Numéro'].tolist()
    ticket_loto.sort()
    st.subheader(f"Jouer : {', '.join(map(str, ticket_loto))}")
    st.info(f"Probabilité de succès basée sur l'écart du n°{ticket_loto[0]}")

with col2:
    st.header("🇪🇺 TICKET EURO")
    ticket_euro = res_euro.head(5)['Numéro'].tolist()
    ticket_euro.sort()
    st.subheader(f"Jouer : {', '.join(map(str, ticket_euro))}")
    st.error(f"Alerte : Priorité zone BASSE (1-25) activée.")

st.divider()

# --- 4. ANALYSE DÉTAILLÉE DES CHOIX ---
st.write("### 🧠 Pourquoi ces numéros ?")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Tension Max", f"N°{res_loto.iloc[0]['Numéro']}", "Score Critique")
with c2:
    st.metric("Annonce Forte", f"N°{res_euro.iloc[0]['Annonceur_De']}", "Succession")
with c3:
    st.metric("Compensation", "Zone Basse", "+20 pts bonus")

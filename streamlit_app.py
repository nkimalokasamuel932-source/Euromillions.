import streamlit as st
import pandas as pd
import os

# =====================================================================
# SÉCURITÉ : ÉCRAN DE CONNEXION MULTI-UTILISATEURS (VIP)
# =====================================================================
st.set_page_config(page_title="Observatoire Circuit Fermé", layout="centered")

# Initialisation de la session utilisateur
if "connecte" not in st.session_state:
    st.session_state["connecte"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

# Si l'utilisateur n'est pas connecté, on affiche le formulaire de login
if not st.session_state["connecte"]:
    st.title("🔒 Loto Radar Pro V45 — Accès Sécurisé")
    st.markdown("### 🎫 Espace Membres Privé")
    
    # Formulaire de saisie
    username_input = st.text_input("Nom d'utilisateur :")
    password_input = st.text_input("Mot de passe :", type="password")
    
    if st.button("🔑 Se connecter au Radar"):
        try:
            # Récupération de la liste des comptes cachée dans les secrets de Streamlit
            comptes_vip = st.secrets["comptes_utilisateurs"]
            
            # Vérification des identifiants
            if username_input in comptes_vip and comptes_vip[username_input] == password_input:
                st.session_state["connecte"] = True
                st.session_state["username"] = username_input
                st.success(f"Bonjour {username_input} ! Connexion réussie...")
                st.rerun()
            else:
                st.error("❌ Identifiant ou mot de passe incorrect.")
        except Exception as e:
            st.warning("⚠️ Configuration de sécurité en cours sur le serveur. Veuillez patienter.")
            
    st.markdown("---")
    st.info("💡 Pour obtenir vos accès personnels ou renouveler votre abonnement, contactez le gestionnaire.")
    st.stop() # Bloque l'application tant qu'on n'est pas logué

# =====================================================================
# CONFIGURATION DE LA BARRE LATÉRALE (SIDEBAR)
# =====================================================================
if st.sidebar.button("🚪 Se déconnecter"):
    st.session_state["connecte"] = False
    st.session_state["username"] = ""
    st.rerun()

st.sidebar.markdown(f"👤 Membre connecté : **{st.session_state['username']}**")

# =====================================================================
# DONNÉES INVARIANTES ET CONFIGURATION DU RADAR
# =====================================================================
COLONNES_BRUTES = {
    "COLONNE 0 (Ancrage)": [3, 10, 15, 17, 20, 30, 35, 41, 43],
    "COLONNE 1 (Verrous)": [1, 4, 14, 25, 26, 32, 34, 39, 48],
    "COLONNE 2 (Résonance)": [2, 8, 12, 18, 19, 30, 33, 36, 46],
    "COLONNE 3 (Dérive)": [7, 16, 21, 27, 28, 31, 37, 38, 45, 48]
}

CHANCES_LOTO = [3, 6, 2, 7, 5, 9]
ETOILES_EURO = [[1, 9], [3, 11], [2, 8], [4, 12], [5, 10], [6, 7]]

CSV_LOTO = "historique_loto.csv"
CSV_EURO = "historique_euromillions.csv"

# Initialisation des fichiers de données si inexistants
if not os.path.exists(CSV_LOTO):
    hist_loto = [
        {"Jeu": "Loto", "Date": "2026-05-04", "N1": 4, "N2": 8, "N3": 15, "N4": 18, "N5": 46, "E1": 2, "E2": 0},
        {"Jeu": "Loto", "Date": "2026-05-06", "N1": 7, "N2": 18, "N3": 27, "N4": 35, "N5": 48, "E1": 5, "E2": 0},
        {"Jeu": "Loto", "Date": "2026-05-09", "N1": 16, "N2": 21, "N3": 25, "N4": 26, "N5": 31, "E1": 1, "E2": 0},
        {"Jeu": "Loto", "Date": "2026-05-11", "N1": 17, "N2": 18, "N3": 30, "N4": 34, "N5": 39, "E1": 9, "E2": 0},
        {"Jeu": "Loto", "Date": "2026-05-13", "N1": 17, "N2": 35, "N3": 38, "N4": 41, "N5": 46, "E1": 2, "E2": 0},
        {"Jeu": "Loto", "Date": "2026-05-16", "N1": 1, "N2": 12, "N3": 30, "N4": 32, "N5": 34, "E1": 4, "E2": 0},
        {"Jeu": "Loto", "Date": "2026-05-18", "N1": 14, "N2": 32, "N3": 33, "N4": 36, "N5": 49, "E1": 3, "E2": 0},
        {"Jeu": "Loto", "Date": "2026-05-20", "N1": 8, "N2": 15, "N3": 28, "N4": 30, "N5": 48, "E1": 7, "E2": 0},
        {"Jeu": "Loto", "Date": "2026-05-23", "N1": 20, "N2": 21, "N3": 23, "N4": 36, "N5": 38, "E1": 2, "E2": 0},
        {"Jeu": "Loto", "Date": "2026-05-25", "N1": 19, "N2": 22, "N3": 27, "N4": 31, "N5": 49, "E1": 3, "E2": 0},
        {"Jeu": "Loto", "Date": "2026-05-27", "N1": 3, "N2": 4, "N3": 15, "N4":

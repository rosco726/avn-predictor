import streamlit as st

# Titre et sélection du projet
st.title("🔢 Prédiction pour le projet : aviator")

# Initialiser les valeurs si pas encore fait
if "valeurs" not in st.session_state:
st.session_state.valeurs = []

# Champ de saisie
valeur = st.text_input("Entrez la valeur 1/30", value="")

# Bouton pour ajouter la valeur
if st.button("Ajoutez cette valeur"):
try:
# Convertir en float même si la saisie contient une virgule
valeur_float = float(valeur.replace(",", "."))
st.session_state.valeurs.append(valeur_float)
st.success(f"Valeur ajoutée : {valeur_float}")
st.rerun()
except ValueError:
st.error("❌ Entrez un nombre valide (ex: 1.23)")

# Affichage des valeurs enregistrées
if st.session_state.valeurs:
st.subheader("Valeurs enregistrées :")
st.write(st.session_state.valeurs)

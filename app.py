import streamlit as st

st.title("Prédiction pour le projet : aviator")

# Initialisation de session_state
if "valeurs" not in st.session_state:
st.session_state.valeurs = []

# Création d'un champ de texte pour entrer une valeur
valeur = st.text_input("Entrez la valeur 1/30", "")

# Bouton pour ajouter la valeur à la liste
if st.button("Ajoutez cette valeur"):
try:
val = float(valeur.replace(",", ".")) # Remplace virgule par point
st.session_state.valeurs.append(val)
st.success(f"Valeur {val} ajoutée.")
except ValueError:
st.error("Veuillez entrer une valeur numérique valide.")

# Affichage des valeurs entrées
if st.session_state.valeurs:
st.write("Valeurs enregistrées :")
st.write(st.session_state.valeurs)
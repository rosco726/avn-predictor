import streamlit as st

st.title("Prédiction pour le projet : aviator")

# Initialisation de session_state
if "valeurs" not in st.session_state:
	st.session_state.valeurs = []

# Création d'un champ de texte pour entrer une valeur
valeur = st.text_input("Entrez la valeur. "")

# Bouton pour ajouter la valeur à la liste
if st.button("Ajoutez cette valeur"):
	try:
		val = float(valeur.remplace(",", ".")) # Remplace virgule par point
		st.session_state.valeurs.append(val)
		st.success(f"Valeur {val} ajoutée.")

# Affichage des valeurs entrées
if st.session_state.valeurs:
	st.write("Valeurs enregistrées :")
	st.write(st.session_state.valeurs)

# ✅ Bouton pour réinitialiser la liste
if st.button("Réinitialiser les valeurs"):
	st.session_state.valeurs = []
	st.success("Liste réinitialisée.")

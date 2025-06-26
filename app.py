import streamlit as st
import json
import os

st.title("🎯 Prédiction pour le projet : Aviator")

# Initialisation de session_state
if "valeurs" not in st.session_state:
	st.session_state.valeurs = []

# Champ de texte pour entrer une valeur
valeur = st.text_input("Entrez une valeur", "")

# Bouton pour ajouter la valeur à la liste
if st.button("➕ Ajouter la valeur"):
	try:
		val = float(valeur.replace(",", ".")) # Remplacer la virgule par un point
		st.session_state.valeurs.append(val)
		st.success(f"✅ Valeur {val} ajoutée.")
	except ValueError:
		st.error("🚫 Veuillez entrer une valeur numérique valide.")

# Affichage des valeurs enregistrées
if st.session_state.valeurs:
	st.subheader("📋 Valeurs enregistrées")
	st.write(st.session_state.valeurs)

# Bouton pour réinitialiser
if st.button("♻️ Réinitialiser les valeurs"):
	st.session_state.valeurs = []
	st.success("✅ Liste réinitialisée.")

# Fonction d'enregistrement de l'algorithme (simulation ici)
def enregistrer_algorithme(valeurs, chemin_fichier="algorithme.json"):
	try:
		with open(chemin_fichier, "w") as f:
			json.dump({"valeurs": valeurs}, f, indent=4)
		return True
	except Exception as e:
		st.error(f"Erreur lors de l'enregistrement : {e}")
		return False

# Bouton pour sauvegarder les données de l'algorithme
if st.button("📦 Enregistrer l'algorithme"):
	if st.session_state.valeurs:
		success = enregistrer_algorithme(st.session_state.valeurs)
		if success:
			st.success("✅ Algorithme enregistré avec succès !")
	else:
		st.warning("⚠️ Aucune valeur à enregistrer.")

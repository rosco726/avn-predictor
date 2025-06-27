import streamlit as st
import json
import os
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

# Dossier pour sauvegarder les modèles
DOSSIER_MODELES = "algorithmes"
os.makedirs(DOSSIER_MODELES, exist_ok=True)

st.title("🧠 Prédiction pour le projet : Aviator")

# Initialisation de session_state
if "valeurs" not in st.session_state:
    st.session_state.valeurs = []

# ➕ Ajouter une nouvelle valeur
valeur = st.text_input("Entrez une valeur numérique", "")

if st.button("Ajouter la valeur"):
    try:
        val = float(valeur.replace(",", "."))
        st.session_state.valeurs.append(val)
        st.success(f"Valeur {val} ajoutée avec succès.")
    except ValueError:
        st.error("🚫 Veuillez entrer un nombre valide.")

# 📋 Affichage des valeurs saisies
if st.session_state.valeurs:
    st.subheader("📌 Valeurs actuelles :")
    st.write(st.session_state.valeurs)

# ♻️ Réinitialiser la liste en cours
if st.button("Réinitialiser les valeurs"):
    st.session_state.valeurs = []
    st.success("✅ Liste réinitialisée.")

# 📁 Sauvegarde de l'algorithme
st.subheader("📦 Sauvegarder un algorithme")
nom_algo = st.text_input("Nom de l'algorithme à enregistrer")

def enregistrer_algorithme(nom, valeurs):
    chemin = os.path.join(DOSSIER_MODELES, f"{nom}.json")
    with open(chemin, "w") as f:
        json.dump({"valeurs": valeurs}, f, indent=4)
    return chemin

if st.button("💾 Enregistrer l'algorithme"):
    if not nom_algo.strip():
        st.warning("Veuillez entrer un nom.")
    elif not st.session_state.valeurs:
        st.warning("Aucune valeur à enregistrer.")
    else:
        chemin = enregistrer_algorithme(nom_algo.strip(), st.session_state.valeurs)
        st.success(f"✅ Algorithme enregistré sous le nom : {nom_algo.strip()}")

# 📂 Chargement d’un algorithme existant
st.subheader("📂 Charger un algorithme existant")
fichiers = [f.replace(".json", "") for f in os.listdir(DOSSIER_MODELES) if f.endswith(".json")]
algo_selectionne = st.selectbox("Choisissez un algorithme", fichiers)

def charger_algorithme(nom):
    chemin = os.path.join(DOSSIER_MODELES, f"{nom}.json")
    with open(chemin, "r") as f:
        donnees = json.load(f)
    return donnees["valeurs"]

if st.button("📥 Charger cet algorithme"):
    try:
        valeurs_chargees = charger_algorithme(algo_selectionne)
        st.session_state.valeurs = valeurs_chargees
        st.success(f"✅ Algorithme '{algo_selectionne}' chargé.")
        st.write("📌 Valeurs :")
        st.write(valeurs_chargees)
    except Exception as e:
        st.error(f"Erreur : {e}")

# 🔮 Prédiction de 3 valeurs futures
st.subheader("🔮 Générer les 3 prochaines valeurs")

def generer_predictions(valeurs, n=3):
    if len(valeurs) < 2:
        return None
    x = np.arange(len(valeurs))
    y = np.array(valeurs)
    coef = np.polyfit(x, y, 1)  # Régression linéaire
    tendance = np.poly1d(coef)
    return [round(tendance(i), 2) for i in range(len(valeurs), len(valeurs) + n)]

if st.button("🔮 Prédire les 3 prochaines valeurs"):
    if len(st.session_state.valeurs) < 2:
        st.warning("Il faut au moins 2 valeurs pour générer une prédiction.")
    else:
        pred = generer_predictions(st.session_state.valeurs)
        st.success("📈 Prédictions :")
        st.write(pred)

# 🧠 Prédiction via IA (LSTM)
st.subheader("🧠 Prédiction via IA (LSTM)")

def prepare_lstm_data(data, n_steps=5):
    X, y = [], []
    for i in range(len(data) - n_steps):
        X.append(data[i:i+n_steps])
        y.append(data[i+n_steps])
    return np.array(X), np.array(y)

def train_lstm_model(data):
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(np.array(data).reshape(-1, 1))

    X, y = prepare_lstm_data(data_scaled)

    X = X.reshape((X.shape[0], X.shape[1], 1))

    model = Sequential()
    model.add(LSTM(64, return_sequences=True, input_shape=(X.shape[1], 1)))
    model.add(LSTM(32))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=100, verbose=0)

    return model, scaler, X[-1].reshape(1, X.shape[1], 1)

def predict_lstm(model, scaler, last_input, n_predictions=3):
    preds = []
    current_input = last_input.copy()
    for _ in range(n_predictions):
        pred = model.predict(current_input, verbose=0)
        preds.append(scaler.inverse_transform(pred)[0][0])
        current_input = np.append(current_input[:,1:,:], [[pred[0]]], axis=1)
    return [round(p, 2) for p in preds]

if st.button("🔬 Prédire avec IA (LSTM)"):
    if len(st.session_state.valeurs) < 7:
        st.warning("⚠️ Il faut au moins 7 valeurs pour entraîner l'IA.")
    else:
        try:
            model, scaler, last_input = train_lstm_model(st.session_state.valeurs)
            lstm_preds = predict_lstm(model, scaler, last_input)
            st.success("📊 Prédictions IA (LSTM) :")
            st.write(lstm_preds)
        except Exception as e:
            st.error(f"Erreur IA : {e}")
import matplotlib.pyplot as plt
ax.plot(range(len(st.session_state.valeurs)), st.session_state.valeurs, label="Données")
ax.plot(range(len(st.session_state.valeurs), len(st.session_state.valeurs) + 3), lstm_preds, label="Prédictions")
ax.legend()
st.pyplot(fig)


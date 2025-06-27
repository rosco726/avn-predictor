import streamlit as st
import json
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

# Dossier pour sauvegarder les modèles
DOSSIER_MODELES = "algorithmes"
os.makedirs(DOSSIER_MODELES, exist_ok=True)

st.title("🧠 Prédiction pour le projet : Aviator")

if "valeurs" not in st.session_state:
    st.session_state.valeurs = []

valeur = st.text_input("Entrez une valeur numérique", "")

if st.button("Ajouter la valeur"):
    try:
        val = float(valeur.replace(",", "."))
        st.session_state.valeurs.append(val)
        st.success(f"Valeur {val} ajoutée avec succès.")
    except ValueError:
        st.error("🚫 Veuillez entrer un nombre valide.")

if st.session_state.valeurs:
    st.subheader("📌 Valeurs actuelles :")
    st.write(st.session_state.valeurs)

if st.button("Réinitialiser les valeurs"):
    st.session_state.valeurs = []
    st.success("✅ Liste réinitialisée.")

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
        st.write("📌 Valeurs :", valeurs_chargees)
    except Exception as e:
        st.error(f"Erreur : {e}")

st.subheader("🔮 Prédiction IA (LSTM)")

def prepare_lstm_data(data, n_steps=5):
    X, y = [], []
    for i in range(len(data) - n_steps):
        X.append(data[i:i+n_steps])
        y.append(data[i+n_steps])
    return np.array(X), np.array(y)

def train_lstm_model(data, n_steps=5):
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(np.array(data).reshape(-1, 1))

    X, y = prepare_lstm_data(data_scaled, n_steps)
    X = X.reshape((X.shape[0], X.shape[1], 1))

    model = Sequential()
    model.add(LSTM(64, return_sequences=True, input_shape=(X.shape[1], 1)))
    model.add(LSTM(32))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=300, verbose=0)

    return model, scaler, X[-1].reshape(1, X.shape[1], 1)

def predict_lstm(model, scaler, last_input, n_predictions=3):
    preds = []
    current_input = last_input.copy()
    for _ in range(n_predictions):
        pred = model.predict(current_input, verbose=0)
        preds.append(scaler.inverse_transform(pred)[0][0])
        current_input = np.append(current_input[:, 1:, :], [[pred[0]]], axis=1)
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

            st.write("📌 Dernières vraies valeurs :", st.session_state.valeurs[-3:])
            st.write("📈 Comparaison graphique :")

            fig, ax = plt.subplots()
            ax.plot(range(len(st.session_state.valeurs)), st.session_state.valeurs, label="Données")
            ax.plot(range(len(st.session_state.valeurs), len(st.session_state.valeurs) + 3), lstm_preds, label="Prédictions", color="orange")
            ax.legend()
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Erreur IA : {e}")

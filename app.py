import streamlit as st
import base64
import joblib
import pandas as pd

# configuration de la page
st.set_page_config(page_title="Dropout Predictor", layout="wide")

# chargement du modèle
@st.cache_resource
def load_model():
    return joblib.load("model/random_forest_model.pkl")

model = load_model()

# sidebar
st.sidebar.title("❕ À propos")
st.sidebar.write("""
Cette application utilise un modèle de Machine Learning
pour prédire le risque d'abandon scolaire.
""")

# bannière
def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img = get_base64_image("images/banner.jpg")

st.markdown(
    f"""
    <img src="data:image/jpg;base64,{img}" 
         style="width:100%; height:250px; object-fit:cover;">
    """,
    unsafe_allow_html=True
)

# titre
st.markdown(
    "<h1 style='text-align: center;'>🎓 Prédiction du risque d'abandon scolaire</h1>",
    unsafe_allow_html=True
)

st.divider()

# texte
st.write("""
Bienvenue sur cette application de prédiction du risque d'abandon scolaire. 

Cette application estime la probabilité d’abandon d'un(e) étudiant(e) en fonction des informations fournies.  

Veuillez renseigner les informations demandées ci-dessous, puis cliquez sur **"Prédire"** 
pour obtenir une évaluation du risque.
""")

st.divider()

# formulaire
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Âge", 15, 36)
    gender = st.selectbox("Genre", ["Masculin", "Féminin"])
    study_time_hours = st.slider("Temps d'étude journalier", 0.0, 10.0)

with col2:
    average_grade = st.number_input("Moyenne générale sur 20", 0.0, 20.0)
    absenteeism_rate = st.slider("Taux d'absentéisme", 0.0, 0.5)
    internet_access = st.selectbox("Accès à Internet", ["Oui", "Non"])
    extra_activities = st.selectbox("Activités extrascolaires", ["Oui", "Non"])

# bouton de prédiction
if st.button("🔍 Prédire"):

    # conversion
    input_data = pd.DataFrame([{
        "age": age,
        "gender": "Male" if gender == "Masculin" else "Female",
        "average_grade": average_grade,
        "absenteeism_rate": absenteeism_rate,
        "internet_access": "Yes" if internet_access == "Oui" else "No",
        "study_time_hours": study_time_hours,
        "extra_activities": "Yes" if extra_activities == "Oui" else "No"
    }])

    try:
        with st.spinner("Analyse en cours..."):

            prediction = model.predict(input_data)[0]

            proba = None
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(input_data)[0][1]

        st.subheader("Résultat")

        if prediction == 1:
            st.error("⚠️ Risque d'abandon.")
        else:
            st.success("✅ Faible risque d'abandon.")

        if proba is not None:
            st.progress(int(proba * 100))
            st.write(f"Probabilité : {proba*100:.2f}%")

            if proba > 0.7:
                st.warning("L'étudiant présente un fort risque. Une intervention est recommandée.")
            elif proba > 0.4:
                st.info("Risque modéré. Une surveillance est conseillée.")
            else:
                st.success("Situation stable")

    except Exception as e:
        st.error(f"Erreur : {e}")
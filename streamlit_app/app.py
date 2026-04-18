import streamlit as st
import requests
import base64

st.set_page_config(page_title="Dropout Predictor", layout="wide")


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
    "<h1 style='text-align: center;'>🎓 Prédiction du risque d'abandon scolaire </h1>",
    unsafe_allow_html=True
)

# message de bienvenue
st.markdown("""
Bienvenue sur cette application de prédiction du risque d'abandon scolaire. 

Cette application estime la probabilité d’abandon d'un(e) étudiant(e) en fonction des informations fournies.  

Veuillez renseigner les informations demandées ci-dessous, puis cliquez sur **"Prédire"** 
pour obtenir une évaluation du risque.
""")

# formulaire
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Âge", 15, 36)
    gender = st.selectbox("Genre", ["Masculin", "Féminin"])
    study_time_hours = st.slider("Temps d'étude journalier", 0.0, 10.0)

with col2:
    average_grade = st.number_input("Moyenne générale", 0.0, 20.0)
    absenteeism_rate = st.slider("Taux d'absentéisme", 0.0, 0.5)
    internet_access = st.selectbox("Accès à Internet", ["Oui", "Non"])
    extra_activities = st.selectbox("Activités extrascolaires", ["Oui", "Non"])

# bouton de prédiction
if st.button("🔍 Prédire"):

    data = {
        "age": age,
        "gender": "Male" if gender == "Masculin" else "Female",
        "average_grade": average_grade,
        "absenteeism_rate": absenteeism_rate,
        "internet_access": "Yes" if internet_access == "Oui" else "No",
        "study_time_hours": study_time_hours,
        "extra_activities": "Yes" if extra_activities == "Oui" else "No"
    }

    try:
        with st.spinner("Analyse en cours..."):
            response = requests.post("http://127.0.0.1:5000/predict", json=data)

        result = response.json()
        proba = result["dropout_probability"]

        st.subheader("Résultat")

        # résultat
        if result["prediction"] == 1:
            st.error("⚠️ Risque d'abandon.")
        else:
            st.success("✅ Faible risque d'abandon.")

        # barre de progression
        st.progress(int(proba * 100))
        st.write(f"Probabilité : {proba*100:.2f}%")

        st.subheader("Action")
        
        # action à mener
        if proba > 0.7:
            st.warning("L'étudiant présente un fort risque. Une intervention est recommandée.")
        elif proba > 0.4:
            st.info("Risque modéré. Une surveillance est conseillée.")
        else:
            st.success("Situation stable.")

    except requests.exceptions.ConnectionError:
        st.error("❌ Impossible de contacter l'API Flask. Vérifie qu'elle est lancée.")








# import streamlit as st
# import requests
# import base64

# st.set_page_config(page_title="Dropout Predictor", layout="wide")

# # 🔷 Sidebar
# st.sidebar.title("❕ À propos")
# st.sidebar.write("""
# Cette application utilise un modèle de Machine Learning
# pour prédire le risque d'abandon scolaire.
# """)

# # 🔷 Bannière
# def get_base64_image(path):
#     with open(path, "rb") as f:
#         return base64.b64encode(f.read()).decode()

# img = get_base64_image("images/banner.jpg")

# st.markdown(
#     f"""
#     <img src="data:image/jpg;base64,{img}" 
#          style="width:100%; height:250px; object-fit:cover;">
#     """,
#     unsafe_allow_html=True
# )

# # 🔷 Titre
# st.markdown(
#     "<h1 style='text-align: center;'>🎓 Prédiction du risque d'abandon scolaire</h1>",
#     unsafe_allow_html=True
# )

# # 🔷 Message de bienvenue
# st.markdown("""
# Bienvenue sur cette application de prédiction du risque d'abandon scolaire.  

# Cette application estime la probabilité d’abandon d'un(e) étudiant(e) en fonction des informations fournies.  

# 👉 Veuillez renseigner les informations ci-dessous puis cliquez sur **"Prédire"**.
# """)

# # 🔷 Formulaire
# col1, col2 = st.columns(2)

# with col1:
#     age = st.number_input("Âge", 15, 36)
#     gender = st.selectbox("Genre", ["Masculin", "Féminin"])
#     study_time_hours = st.slider("Temps d'étude journalier", 0.0, 10.0)

# with col2:
#     average_grade = st.number_input("Moyenne générale", 0.0, 20.0)
#     absenteeism_rate = st.slider("Taux d'absentéisme", 0.0, 0.5)
#     internet_access = st.selectbox("Accès à Internet", ["Oui", "Non"])
#     extra_activities = st.selectbox("Activités extrascolaires", ["Oui", "Non"])

# # 🔷 Bouton
# if st.button("🔍 Prédire"):

#     # ⚠️ Conversion des valeurs (TRÈS IMPORTANT)
#     data = {
#         "age": age,
#         "gender": "Male" if gender == "Masculin" else "Female",
#         "average_grade": average_grade,
#         "absenteeism_rate": absenteeism_rate,
#         "internet_access": "Yes" if internet_access == "Oui" else "No",
#         "study_time_hours": study_time_hours,
#         "extra_activities": "Yes" if extra_activities == "Oui" else "No"
#     }

    # try:
    #     with st.spinner("Analyse en cours..."):
    #         response = requests.post("http://127.0.0.1:5000/predict", json=data)

    #     # 🔷 Vérifier si l'API répond bien
    #     if response.status_code != 200:
    #         st.error("❌ Erreur API")
    #         st.write(response.text)
    #     else:
    #         result = response.json()

    #         # Debug (tu peux enlever après)
    #         # st.write(result)

    #         # 🔷 Gestion erreur API
    #         if "error" in result:
    #             st.error(result["error"])
    #         else:
    #             st.subheader("Résultat")

    #             prediction = result.get("prediction")
    #             proba = result.get("dropout_probability")

    #             # 🔷 Résultat principal
    #             if prediction == 1:
    #                 st.error("⚠️ Risque élevé d'abandon")
    #                 st.image("https://cdn-icons-png.flaticon.com/512/463/463612.png", width=100)
    #             else:
    #                 st.success("✅ Faible risque d'abandon")
    #                 st.image("https://cdn-icons-png.flaticon.com/512/190/190411.png", width=100)

    #             # 🔷 Probabilité (si disponible)
    #             if proba is not None:
    #                 st.progress(int(proba * 100))
    #                 st.write(f"Probabilité : {proba*100:.2f}%")

    #                 # 🔷 Interprétation
    #                 if proba > 0.7:
    #                     st.warning("Risque élevé : intervention recommandée.")
    #                 elif proba > 0.4:
    #                     st.info("Risque modéré : surveillance conseillée.")
    #                 else:
    #                     st.success("Situation stable.")

    #             else:
    #                 st.warning("⚠️ Probabilité non disponible pour ce modèle.")

    # except requests.exceptions.ConnectionError:
    #     st.error("❌ Impossible de contacter l'API Flask. Vérifie qu'elle est lancée.")
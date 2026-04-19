from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Charger ton pipeline complet (très important)
model = joblib.load("model/random_forest_model.pkl")


@app.route("/")
def home():
    return {"message": "Student Dropout API is running"}


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    try:
        # Créer DataFrame avec les bonnes colonnes
        input_data = pd.DataFrame([{
            "age": data["age"],
            "gender": data["gender"],
            "average_grade": data["average_grade"],
            "absenteeism_rate": data["absenteeism_rate"],
            "internet_access": data["internet_access"],
            "study_time_hours": data["study_time_hours"],
            "extra_activities": data["extra_activities"]
        }])

        prediction = model.predict(input_data)[0]

        proba = None
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(input_data)[0][1]

        return jsonify({
            "prediction": int(prediction),
            "dropout_probability": float(proba) if proba is not None else None
        })

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
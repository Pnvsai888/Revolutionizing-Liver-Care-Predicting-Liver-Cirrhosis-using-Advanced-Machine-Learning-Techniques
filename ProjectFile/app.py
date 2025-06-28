from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load the model
with open('liver_prediction.pkl', 'rb') as f:
    model = pickle.load(f)

# Input fields expected from the form
feature_names = [
    'AGE', 'Gender', 'Place(location where the patient lives)',
    'Duration of alcohol consumption(years)', 'Quantity of alcohol consumption (quarters/day)',
    'Type of alcohol consumed', 'Blood pressure (mmhg)', 'Obesity',
    'Family history of cirrhosis/ hereditary', 'Hemoglobin  (g/dl)', 'PCV  (%)',
    'RBC  (million cells/microliter)', 'MCV   (femtoliters/cell)', 'MCH  (picograms/cell)',
    'MCHC  (grams/deciliter)', 'Total Count', 'Polymorphs  (%)', 'Lymphocytes  (%)',
    'Monocytes   (%)', 'Eosinophils   (%)', 'Basophils  (%)',
    'Platelet Count  (lakhs/mm)', 'Direct    (mg/dl)', 'Indirect     (mg/dl)',
    'Total Protein     (g/dl)', 'Albumin   (g/dl)', 'Globulin  (g/dl)',
    'AL.Phosphatase      (U/L)', 'SGOT/AST      (U/L)', 'USG Abdomen (diffuse liver or  not)',
    'Lymphocytes  (%)', 'Hemoglobin  (g/dl)'
]

# Mapping for categorical fields
binary_map = {
    'Gender': {'male': 1, 'female': 0, 'transgender': 2},
    'Obesity': {'yes': 1, 'no': 0},
    'Family history of cirrhosis/ hereditary': {'yes': 1, 'no': 0},
    'USG Abdomen (diffuse liver or  not)': {'yes': 1, 'no': 0},
    'Place(location where the patient lives)': {'rural': 1, 'urban': 0},
    'Type of alcohol consumed': {'country liquor': 1, 'branded liquor': 2, 'both': 3},
}


@app.route('/')
def home():
    return render_template('page.html')  # Your homepage with info and image


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        # Form page
        return render_template('index.html', feature_names=feature_names)

    try:
        user_input = request.form
        values = []
        for field in feature_names:
            val = user_input.get(field, 0)
            val = val.strip().lower() if isinstance(val, str) else val
            if field in binary_map:
                val = binary_map[field].get(val, 0)
            else:
                val = float(val)
            values.append(val)

        prediction = model.predict([values])[0]
        result = "😡 Cirrhosis Detected" if prediction == 1 else "😊 No Cirrhosis Detected"
        return render_template('result.html', prediction_result=result)

    except Exception as e:
        return render_template('result.html', prediction_result=f"⚠️ Error: {e}")


if __name__ == '__main__':
    app.run(debug=True)

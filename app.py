from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import re
import sys

# ✅ Start message
print("✅ Starting Flask app...")


try:
    # Load the model and vectorizer
    model = joblib.load("phishing_model.pkl")
    vectorizer = joblib.load("tfidf_vectorizer.pkl")
except Exception as e:
    print(f"❌ Error loading model or vectorizer: {e}")
    sys.exit(1)


# Flask setup
app = Flask(__name__)
CORS(app)

# Text cleaner
def clean_text(text):
    text = re.sub(r"http\S+|www\S+|https\S+", '', text)
    text = re.sub(r'\@w+|\#','', text)
    text = re.sub(r'[^A-Za-z0-9 ]+', '', text)
    text = text.lower()
    return text

# API route
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    subject = data.get('subject', '')
    body = data.get('body', '')
    urls = data.get('urls', '')

    combined = f"{subject} {body} {urls}"
    cleaned = clean_text(combined)
    vectorized = vectorizer.transform([cleaned])
    prediction = model.predict(vectorized)[0]

    result = "Phishing Email ⚠️" if prediction == 1 else "Legitimate Email ✅"
    return jsonify({'result': result})

# ✅ Run the server
if __name__ == '__main__':
    app.run(debug=True)

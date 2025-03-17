from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

def generate_names(gender, culture):
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }

    prompt = f"Suggest 3 beautiful and unique {gender} baby names from {culture} culture. Only list the names clearly separated by commas."

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 50,
        "temperature": 0.8,
        "n": 1
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        names = response.json()['choices'][0]['message']['content']
        return names.split(',')
    else:
        return ["Error generating names."]

@app.route("/", methods=["GET", "POST"])
def index():
    names = None
    if request.method == "POST":
        gender = request.form.get("gender")
        culture = request.form.get("culture")
        names = generate_names(gender, culture)
    return render_template("index.html", names=names)

if __name__ == "__main__":
    app.run(debug=True)

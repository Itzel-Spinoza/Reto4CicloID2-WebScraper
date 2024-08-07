from flask import Flask, jsonify, request, send_from_directory
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory(os.path.abspath(os.path.dirname(__file__)), 'index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form.get('url')
    if not url:
        return jsonify({"error": "Por favor, proporciona un enlace."}), 400

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({"error": f"Error al acceder a la URL: {str(e)}"}), 400

    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)  # Extrae todo el texto de la página web

    return jsonify({"url": url, "text": text})

if __name__ == '__main__':
    app.run(debug=True)


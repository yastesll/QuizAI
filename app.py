"""
Date : 25/05/2025
BUT : Importer Flask & Créer l'application
Auteur : VIDZRAKOU
"""
from flask import Flask

app = Flask(__name__)

@app.route('/')
def accueil():
    return "Bonjour, QuizAI fonctionne !"

if __name__ == '__main__':
    app.run(debug=True)
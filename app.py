"""
Date : 25/05/2025
BUT : Importer Flask & Créer l'application
Auteur : VIDZRAKOU
"""
# on importe les modules nécessaires pour notre application Flask
from flask import Flask , render_template , request , redirect , url_for , session
# on importe les fonctions pour gérer les mots de passe et les sessions
from werkzeug.security import generate_password_hash , check_password_hash     
from dotenv import load_dotenv
# on importe les fonctions pour interagir avec la base de données
import sqlite3
import os
app = Flask(__name__)

load_dotenv() # on charge les variables d'environnement depuis le fichier .env
app.secret_key = os.getenv('SECRET_KEY') # on définit la clé secrète de l'application à partir de la variable d'environnement

def get_db():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # on obtient le chemin du répertoire actuel
    DB_PATH = os.path.join(BASE_DIR, 'database', 'quizai.db') # on construit le chemin vers la base de données
    conn = sqlite3.connect(DB_PATH) # on se connecte à la base de données
    conn.row_factory = sqlite3.Row # on configure la connexion pour retourner des lignes sous forme de dictionnaires
    return conn # on retourne la connexion à la base de données
@app.route('/register', methods=['GET', 'POST']) # on définit la route pour la page d'inscription
def register():
    if request.method == 'POST': # si la méthode de la requête est POST, cela signifie que le formulaire a été soumis
        nom = request.form['nom'] # on récupère le nom du formulaire
        email = request.form['email'] # on récupère l'email du formulaire
        mot_de_passe =generate_password_hash(request.form['mot_de_passe']) # on récupère le mot de passe du formulaire et on le hash pour plus de sécurité
        try:
            conn = get_db() # on obtient une connexion à la base de données
            cursor = conn.cursor() # on crée un curseur pour exécuter des commandes SQL
            cursor.execute('INSERT INTO users (nom, email, mot_de_passe) VALUES (?, ?, ?)', (nom, email, mot_de_passe)) # on insère les données de l'utilisateur dans la table users
            conn.commit() # on valide les changements dans la base de données
            conn.close() # on ferme la connexion à la base de données
            return redirect(url_for('login')) # on redirige l'utilisateur vers la page de connexion après une inscription réussie
        except:
            conn.close() # on ferme la connexion à la base de données en cas d'erreur
            return render_template('auth.html', error="Une erreur est survenue lors de l'inscription. Veuillez réessayer.") # on affiche un message d'erreur si l'inscription échoue    
    return render_template('auth.html') # si la méthode de la requête est GET, on affiche le formulaire d'inscription
@app.route('/login', methods=['GET', 'POST']) # on définit la route pour la page de connexion
def login():
    if request.method == 'POST':
        email = request.form['email'] # on récupère l'email du formulaire
        mot_de_passe = request.form['mot_de_passe'] # on récupère le mot de passe du formulaire
        conn = get_db() # on obtient une connexion à la base de données
        cursor = conn.cursor() # on crée un curseur pour exécuter des commandes SQL
        user = cursor.execute(
            'SELECT * FROM users WHERE email = ?', (email,)
        ).fetchone() # on cherche l'utilisateur dans la base de données en fonction de son email
        conn.close() # on ferme la connexion à la base de données
        if user and check_password_hash(user['mot_de_passe'], mot_de_passe): # si l'utilisateur existe et que le mot de passe est correct
            session['user_id'] = user['id'] # on stocke l'identifiant de l'utilisateur dans la session pour maintenir sa connexion
            session['user_name'] = user['nom'] # on stocke le nom de l'utilisateur dans la session pour l'afficher dans l'interface
            return redirect(url_for('dashboard')) # on redirige l'utilisateur vers la page d'accueil après une connexion réussie
        else:
            return render_template('auth.html', error="Email ou mot de passe incorrect.") # on affiche un message d'erreur si la connexion échoue
    return render_template('auth.html') # si la méthode de la requête est GET, on affiche le formulaire de connexion

@app.route('/logout') # on définit la route pour la déconnexion
def logout():
    session.clear() # on efface toutes les données de la session pour déconnecter l'utilisateur
    return redirect(url_for('accueil')) # on redirige l'utilisateur vers la page d'accueil après la déconnexion

@app.route('/dashboard') # on définit la route pour le tableau de bord de l'utilisateur
def dashboard():
    if 'user_id' not in session: # si l'utilisateur n'est pas connecté, on le redirige vers la page de connexion
        return redirect(url_for('login'))
    return render_template('dashboard.html') # si l'utilisateur est connecté, on affiche son tableau de bord


@app.route('/') # on définit la route pour la page d'accueil de l'application
def accueil():
    return render_template('index.html') # on affiche la page d'accueil

@app.route('/library')
def library():
    return render_template('library.html') # on affiche la page de la bibliothèque de quizs

@app.route('/upload')
def upload():
    return render_template('upload.html') # on affiche la page pour télécharger un quiz

@app.route('/config')
def config():
    return render_template('config.html') # on affiche la page de configuration du compte utilisateur

@app.route('/quiz')
def quiz():
    return render_template('quiz.html') # on affiche la page pour jouer à un quiz

@app.route('/results')
def results():
    return render_template('results.html')# on affiche la page des résultats d'un quiz

@app.route('/auth')
def auth():
    return render_template('auth.html') # on affiche la page d'authentification (inscription et connexion)
if __name__ == '__main__':
    app.run(debug=True)

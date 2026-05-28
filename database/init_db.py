import sqlite3 # c'est l'outil python pour parler à notre base de données
import os # c'est l'outil pour naviguer dans les dossiers de l'ordinateur
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# on trouve le chemin du dossier batabase/
DB_PATH = os.path.join(BASE_DIR, 'quizai.db')
# on dit que notre base de données s'appellera quizai
def init_db():
    conn = sqlite3.connect(DB_PATH)
    # on se connecte à la base de données
    cursor = conn.cursor()
    # on crée un curseur pour exécuter des commandes SQL
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT, -- c'est un identifiant unique qui s'incrémente automatiquement
            nom TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL, -- c'est un champ qui doit être unique pour chaque utilisateur
            mot_de_passe TEXT NOT NULL, -- c'est le mot de passe de l'utilisateur, on le stocke en texte pour l'instant mais il faudrait le hasher pour plus de sécurité
            date_inscription TEXT DEFAULT CURRENT_TIMESTAMP       )
        
    ''')
    # on crée la table users avec les champs id, nom, email, mot_de_passe et date_inscription
    # on crée la table courses avec les champs id, USER_ID, titre, contenu, est_public, vues et date_creation
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses(
            id INTEGER PRIMARY KEY AUTOINCREMENT, -- c'est un identifiant unique qui s'incrémente automatiquement
            user_id INTEGER NOT NULL, -- c'est l'identifiant de l'utilisateur qui a créé le quiz
            titre TEXT NOT NULL, -- c'est le titre du quiz
            contenu TEXT NOT NULL, -- c'est le contenu du quiz
            est_public INTEGER DEFAULT 0, -- c'est un indicateur pour savoir si le quiz est public ou non
            vues INTEGER DEFAULT 0, -- c'est le nombre de vues du quiz
            date_creation TEXT DEFAULT CURRENT_TIMESTAMP -- c'est la date de création du quiz
        )
    ''')   
   # on crée la table quizzes avec les champs id, USER_ID, course_id, titre, difficulte, questions et date_creatio
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quizzes(
            id INTEGER PRIMARY KEY AUTOINCREMENT, -- c'est un identifiant unique qui s'incrémente automatiquement
            user_id INTEGER NOT NULL, -- c'est l'identifiant de l'utilisateur qui a créé le quiz
            course_id INTEGER NOT NULL, -- c'est l'identifiant du cours auquel le quiz est associé
            titre TEXT NOT NULL, -- c'est le titre du quiz
            difficulte TEXT NOT NULL, -- c'est la difficulté du quiz

            questions TEXT NOT NULL,
            date_creation TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')  
    # on crée la table quiz_sessions avec les champs id, user_id, quiz_id, score, total_questions et date_session 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_sessions(
            id INTEGER PRIMARY KEY AUTOINCREMENT, -- c'est un identifiant unique qui s'incrémente automatiquement
            user_id INTEGER NOT NULL, -- c'est l'identifiant de l'utilisateur
            quiz_id INTEGER NOT NULL, -- c'est l'identifiant du quiz

            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            date_session TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS commentaires(
            id INTEGER PRIMARY KEY AUTOINCREMENT, -- c'est un identifiant unique qui s'incrémente automatiquement
            user_id INTEGER NOT NULL, -- c'est l'identifiant de l'utilisateur
            course_id INTEGER NOT NULL, -- c'est l'identifiant du cours

            contenu TEXT NOT NULL,
            date_commentaire TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit() # on valide les changements dans la base de données
    conn.close() # on ferme la connexion à la base de données
    print("Base de données créée avec succès !")

if __name__ == "__main__": # si on exécute ce fichier directement, on appelle la fonction init_db() pour créer la base de données
    init_db()

from flask import Flask, render_template, request, jsonify, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore
import os

app = Flask(__name__)

# Configuration de Firebase
# Vérifier si le fichier 'key.json' existe
key_path = 'key.json'
if not os.path.exists(key_path):
    raise FileNotFoundError(f"Le fichier {key_path} est introuvable")

cred = credentials.Certificate(key_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/sing',endpoint='sing')
def sing():
    return render_template('sing.html')  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/featuredrides', endpoint='featured_rides')
def featuredrides():
    return render_template('featured_rides.html')

@app.route('/graph')
def graph():
    return render_template('graph.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        # Vérifier si toutes les données nécessaires sont présentes
        if not all(key in request.form for key in ['nom', 'prenom', 'telephone', 'email', 'role', 'depart', 'arrivee']):
            return jsonify({'error': 'Données manquantes dans le formulaire'}), 400

        # Récupérer les données du formulaire
        data = {
            'nom': request.form['nom'],
            'prenom': request.form['prenom'],
            'telephone': request.form['telephone'],
            'email': request.form['email'],
            'role': request.form['role'],
            'depart': request.form['depart'],
            'arrivee': request.form['arrivee'],
            'commentaire': request.form.get('commentaire', '')
        }

        # Enregistrer dans Firebase Firestore
        db.collection('users').add(data)

        # Rediriger vers une page de confirmation avec les données
        return render_template('confirmation.html', nom=data['nom']) 
    except Exception as e:
        # Retourner une erreur détaillée si quelque chose échoue
        return jsonify({'error': f"Erreur lors de l'enregistrement dans Firestore : {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

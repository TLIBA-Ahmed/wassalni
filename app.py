from flask import Flask, render_template, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Configuration Firebase
cred = credentials.Certificate('key.json')  
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/sign')
def index():
    return render_template('sing.html')  

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
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

        return render_template('confirmation.html', nom=data['nom']) 
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

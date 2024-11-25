from flask import Flask, render_template
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate('recipe-page-project-firebase-adminsdk-v39uz-c296d89862.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route("/")
def index():
    # Fech recipes from Firestore
    recipes_ref = db.collection('recipes')
    recipes = [doc.to_dict() for doc in recipes_ref.stream()]
    
    # Pass documents to templates in the form of a list with recipe dictionaries
    return render_template("recipes.html", recipes=recipes)

if __name__ == "__main__":
    app.run(debug=True)

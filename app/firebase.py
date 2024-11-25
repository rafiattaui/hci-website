import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('recipe-page-project-firebase-adminsdk-v39uz-c296d89862.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()
print("Firebase initialized")

def create_empty_recipe():
    # Create empty recipe
    db.collection('recipes').add({
        'name': '',
        'description': '',
        'difficulty':0,
        'imageurl': '',
        'ingredients': {},
        'tags': [],
    })

def create_recipe(name, description, difficulty, imageurl, ingredients, tags):
    # Create recipe
    # ingredients is a dictionary with ingredient names as keys and quantities as values
    # tags is a list of strings
    # difficulty is an integer between 0 and 5
    # imageurl is a string
    # name is a string
    # description is a string
    db.collection('recipes').add({
        'name': name,
        'description': description,
        'difficulty': difficulty,
        'imageurl': imageurl,
        'ingredients': ingredients,
        'tags': tags,
    })
    
def delete_recipe(recipe_id):
    # Delete recipe
    db.collection('recipes').document(recipe_id).delete()

def get_ids():
    # Get all recipe ids
    recipes_ref = db.collection('recipes')
    return [doc.id for doc in recipes_ref.stream()]
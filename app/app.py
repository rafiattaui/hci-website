from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate('recipe-page-project-firebase-adminsdk.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
recipes_ref = db.collection('recipes')

@app.route("/")
def index():
    
    # Fetch recipes from Firestore
    recipes = [doc.to_dict() for doc in recipes_ref.stream()]
    
    # Pass documents to templates in the form of a list with recipe dictionaries
    return render_template("recipes.html", recipes=recipes)

@app.route("/", methods=["POST","GET"])
def index_query():
    recipes = []
    if request.method == "POST":
        query = request.form.get("query","".lower())
        docs = recipes_ref.stream()
        recipes = [doc.to_dict() for doc in docs if query in doc.to_dict()['name'].lower()]
        return render_template("recipes.html", recipes=recipes)
    
@app.route("/addrecipe")
def addrecipe():
    return render_template("addrecipe.html")

@app.route("/submit", methods=["POST"])
def submit():
    # Access form data
    recipe_name = request.form["recipe_name"]
    recipe_description = request.form["recipe_description"]
    recipe_video = request.form["recipe_video"]
    recipe_image = request.form["recipe_image"]
    recipe_difficulty = request.form["recipe_difficulty"]
    
    # Ingredients (Access ingredients names and quantities as seperate lists)
    ingredient_names = request.form.getlist("ingredient_name[]")
    ingredient_quantities = request.form.getlist("ingredient_quantity[]")
    
    # Steps (Access step descriptions as a list)
    recipe_steps = request.form.getlist("recipe_step[]")
    
    # Print values to check them
    print(f"Recipe Name: {recipe_name}")
    print(f"Description: {recipe_description}")
    print(f"Video Link: {recipe_video}")
    print(f"Image Link: {recipe_image}")
    print(f"Difficulty: {recipe_difficulty}")
    print(f"Ingredients: {dict(zip(ingredient_names, ingredient_quantities))}")
    print(f"Steps: {recipe_steps}")
    
    recipe_data = {
        'name': recipe_name,
        'description': recipe_description,
        'video': recipe_video,
        'imageurl': recipe_image,
        'difficulty': recipe_difficulty,
        'ingredients': dict(zip(ingredient_names, ingredient_quantities)),
        'steps': recipe_steps,
    }

    recipes_ref.add(recipe_data)
    
    # You can process the data here, save it to a database, or return a response
    return f"Recipe '{recipe_name}' submitted successfully!"

if __name__ == "__main__":
    app.run(debug=True)

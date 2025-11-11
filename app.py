from flask import Flask
from flask import abort, flash, make_response, redirect, render_template, request, session

import poems
import users
import secrets
import sqlite3


app = Flask(__name__)
app.secret_key = "Kissa123"

@app.route("/")
def index():
    all_poems = poems.get_all()
    return render_template("index.html", poems=all_poems)

def require_login():
    if "user_id" not in session:
        abort(403)


def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        flash("VIRHE: salasanat eivät ole samat")
        return redirect("/register")

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu")
        return redirect("/register")

    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("VIRHE: väärä tunnus tai salasana")
            return redirect("/login")


@app.route("/new_poem")
def new_poem():
  return render_template("new_poem.html")


@app.route("/create_poem", methods=["POST"])
def create_poem():
    require_login()
    check_csrf()
    
    title = request.form["title"]
    content = request.form["content"]
    user_id = session["user_id"]
    
    category = request.form.get("category", "").strip()
    themes_input = request.form.get("themes", "").strip()
    
    theme_values = None
    if themes_input:
        theme_values = [t.strip() for t in themes_input.split(",") if t.strip()]
    
    if not title or not content:
        flash("otsikko ja sisältö vaaditaan")
        return redirect("/new_poem")
    
    poem_id = poems.add_poem(
        title=title,
        content=content,
        user_id=user_id,
        category_value=category if category else None,
        theme_values=theme_values
    )
    
    return redirect(f"/poem/{poem_id}")

@app.route("/poem/<int:poem_id>")
def show_poem(poem_id):
    poem = poems.get_poem(poem_id)
    if not poem:
        abort(404)
    
    reviews = poems.get_reviews(poem_id)
    avg_rating = poems.get_average_rating(poem_id)
    categories = poems.get_categories(poem_id)
    themes = poems.get_themes(poem_id)
    
    return render_template("show_poem.html", 
                         poem=poem, 
                         reviews=reviews,
                         avg_rating=avg_rating,
                         categories=categories,
                         themes=themes)


@app.route("/edit_poem/<int:poem_id>")
def edit_poem(poem_id):
    require_login()
    poem = poems.get_poem(poem_id)
    if not poem:
        abort(404)
    # Check if user owns this poem
    if poem['user_id'] != session['user_id']:
        abort(403)
    categories = poems.get_categories(poem_id)
    themes = poems.get_themes(poem_id)
    return render_template("edit_poem.html",
        poem=poem,
        categories=categories,
        themes=themes)

@app.route("/update_poem/<int:poem_id>", methods=["POST"])
def update_poem(poem_id):
    require_login()
    check_csrf()
    poem = poems.get_poem(poem_id)
    if not poem:
        abort(404)
    # Check if user owns this poem
    if poem['user_id'] != session['user_id']:
        abort(403)
    
    title = request.form["title"]
    content = request.form["content"]
    category = request.form.get("category", "").strip()
    themes_input = request.form.get("themes", "").strip()
    
    if not title or not content:
        flash("otsikko ja sisältö vaaditaan")
        return redirect(f"/edit_poem/{poem_id}")
    
    # Update the poem
    poems.update_poem(poem_id, title, content)
    
    # Update category
    poems.update_category(poem_id, category if category else None)
    
    # Update themes
    theme_values = None
    if themes_input:
        theme_values = [t.strip() for t in themes_input.split(",") if t.strip()]
    poems.update_themes(poem_id, theme_values)
    
    flash("runo päivitetty onnistuneesti!")
    return redirect(f"/poem/{poem_id}")

@app.route("/delete_poem/<int:poem_id>", methods=["GET", "POST"])
def delete_poem_route(poem_id):
    require_login()
    poem = poems.get_poem(poem_id)
    if not poem:
        abort(404)
    # Check if user owns this poem
    if poem['user_id'] != session['user_id']:
        abort(403)
    
    if request.method == "GET":
        # Show confirmation page
        return render_template("delete_poem.html", poem=poem)
    
    if request.method == "POST":
        # Actually delete the poem
        check_csrf()
        if poems.delete_poem(poem_id, session["user_id"]):
            flash("runo poistettu onnistuneesti")
        else:
            flash("VIRHE: runon poistaminen epäonnistui")
        return redirect("/")
    

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")
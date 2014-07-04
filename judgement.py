from flask import Flask, render_template, redirect, request, flash, session as b_session
import model

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup", methods=["GET"])
def show_signup():
    return render_template("sign_up.html")

@app.route("/signup", methods=["POST"])
def process_signup():
    form_email = request.form['email']
    form_password = request.form['password']
    form_age = request.form['age']
    form_zipcode = request.form['zipcode']

    new_user = model.User(
        email = form_email,
        password = form_password,
        age = form_age,
        zipcode = form_zipcode
        )
    model.session.add(new_user)
    model.session.commit()
    
    return redirect("/personal_ratings")

@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def process_login():
    """user enters email, used to look up user in DB."""
    form_email = request.form['email']
    user = model.session.query(model.User).filter_by(email = form_email).all()
    if user:
        """setting session to user id"""
        b_session["user"] = user[0].id
        flash("Login successful. Welcome back!")
        return redirect("/")
    else:
        flash("No such email in our user database. Please re-enter.")
        return redirect("/login")

@app.route("/logout")
def logout():
    b_session.clear()
    return render_template("logout.html")

@app.route("/all_users")
def show_all_users():
    user_list = model.session.query(model.User).all()
    return render_template("user_list.html", user_list=user_list)

@app.route("/personal_ratings", methods=["GET"])
def show_personalratings():
    logged_in_user_id = b_session["user"]
    user_ratings = model.session.query(model.Rating).filter_by(user_id=logged_in_user_id)

    return render_template("personal_ratings.html", user_ratings=user_ratings)

@app.route("/new_rating", methods=["GET"])
def search_movies():
    return render_template("search_form.html")

@app.route("/new_rating", methods=["POST"])
def new_rating():
    form_search_phrase = "%" + request.form["search-phrase"] + "%"
    search_results = model.session.query(model.Movie).filter(model.Movie.title.like(form_search_phrase)).all()
    if search_results:
        return render_template("search_results.html", search_results=search_results, user_id = b_session['user'])
    else:
        flash("Sorry, no movies in our database match your search.")
        return redirect("/new_rating")
    

@app.route("/set_rating", methods=["POST"])
def set_rating():
    form_rating = request.form["rating"]
    form_movie_id = request.form["movie_id"]
    user_id = b_session["user"]
    
    rating = model.session.query(model.Rating).filter(model.Rating.movie_id == form_movie_id, model.Rating.user_id == user_id).first()

    if not rating:
        rating = model.Rating(movie_id=form_movie_id, user_id=user_id)
        model.session.add(rating)
    rating.rating = form_rating
    model.session.commit()

    return "success"
    

if __name__ == "__main__":
    app.run(debug=True)
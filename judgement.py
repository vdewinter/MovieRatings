from flask import Flask, render_template, redirect, request, flash, session as b_session
import model

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("sign_up.html")
    elif request.method == "POST":
        # add new user to DB
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

@app.route("/login", methods=["GET", "POST"])
def show_login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        form_email = request.form['email']
        user = model.session.query(model.User).filter_by(email = form_email).all()
        if user:
            # setting session['user'] to user id
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
def show_personal_ratings():
    if len(b_session):
        logged_in_user_id = b_session["user"]
        user_ratings = model.session.query(model.Rating).filter_by(user_id=logged_in_user_id)
    else:
        return("Please log in or sign up to search for and rate movies.")
        
    return render_template("personal_ratings.html", user_ratings=user_ratings)

@app.route("/search_movies", methods=["GET", "POST"])
def search_movies():
    if len(b_session):
        if request.method == "GET":
            return render_template("search_form.html")
        elif request.method == "POST":
            # query DB for movie title
            form_search_phrase = "%" + request.form["search-phrase"] + "%"
            search_results = model.session.query(model.Movie).filter(model.Movie.title.like(form_search_phrase)).all()

            if search_results:
                return render_template("search_results.html", search_results=search_results, user_id = b_session['user'])
            else:
                flash("Sorry, no movies in our database match your search.")
                return redirect("/search_movies")
    else:
        return("Please log in or sign up to search for and rate movies.")

@app.route("/set_rating", methods=["POST"])
def set_rating():
    form_rating = request.form["rating"]
    form_movie_id = request.form["movie_id"]
    user_id = b_session["user"]
    
    rating = model.session.query(model.Rating).filter(model.Rating.movie_id == form_movie_id, model.Rating.user_id == user_id).first()

    # check if a rating for a given user/movie combo exists; if not, create a new rating in the DB.
    if not rating:
        rating = model.Rating(movie_id=form_movie_id, user_id=user_id)
        model.session.add(rating)

    # update rating to newly selected rating
    rating.rating = form_rating
    model.session.commit()

    return "success"

@app.route("/movie/<int:id>", methods = ["GET"])
def view_movie(id):
    movie = model.session.query(model.Movie).get(id)
    ratings = movie.ratings

    rating_nums = []
    user_rating = None

    for r in ratings:
        if r.user_id == b_session['user']:
            user_rating = r
        rating_nums.append(r.rating)
    avg_rating = float(sum(rating_nums))/len(rating_nums)

    # only predict if a user has not rated the movie
    user = model.session.query(model.User).get(b_session['user'])
    prediction = None

    if not user_rating:
        prediction = user.predict_rating(movie)

    return render_template("movie.html", movie = movie, average = avg_rating,\
        user_rating = user_rating, prediction = prediction)



if __name__ == "__main__":
    app.run(debug=True)
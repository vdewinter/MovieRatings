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
    print form_email, form_password, form_age, form_zipcode
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
        return redirect("/personal_ratings")
    else:
        flash("No such email in our user database. Please re-enter.")
        return redirect("/login")

@app.route("/logout")
def logout():
    b_session.clear()
    return render_template("logout.html")

@app.route("/all_users")
def show_all_users():
    user_list = model.session.query(model.User).limit(5).all()
    return render_template("user_list.html", user_list=user_list)

@app.route("/personal_ratings", methods=["GET"])
def show_personalratings():
    logged_in_user_id = b_session["user"]
    user_ratings = model.session.query(model.Rating).filter_by(user_id=logged_in_user_id)
    return render_template("personal_ratings.html", user_ratings=user_ratings)

# @app.route("/movie_record_%s" % movie.id, methods=["GET"])
# def show_movie_record():
#     pass

# @app.route("/movie_record_%s" % movie.id, methods=['POST'])
# def update_movie_record():
#     pass
    

if __name__ == "__main__":
    app.run(debug=True)
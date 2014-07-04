import model, csv, datetime

def load_users(session):
    with open('./seed_data/u.user', 'rb') as csvfile:
        user_rows = csv.reader(csvfile, delimiter="|")
        for user in user_rows:
            user_id = user[0]
            user_age = user[1]
            user_zipcode = user[4]
            c = model.User(id = user_id, 
                     age = user_age,
                     zipcode = user_zipcode)
            session.add(c)
        session.commit()


def load_movies(session):
    with open('./seed_data/u.item', 'rb') as csvfile:
        movie_rows = csv.reader(csvfile, delimiter="|")
        for movie in movie_rows:
            movie_id = movie[0]
            title = movie[1][:-6].strip() # strip out release year from title
            title = title.decode("latin-1")
            if movie[2]:
                release_date = datetime.datetime.strptime(movie[2], "%d-%b-%Y")
            url = movie[4] 
            m = model.Movie(id = movie_id,
                            title = title,
                            release_date = release_date,
                            url = url)
            session.add(m)
        session.commit()

def load_ratings(session):
    with open('./seed_data/u.data', 'rb') as csvfile:
        ratings_rows = csv.reader(csvfile, delimiter="\t")
        for rating_row in ratings_rows:
            user_id = rating_row[0]
            movie_id = rating_row[1]
            movie_rating = rating_row[2]
            r = model.Rating(user_id = user_id,
                            movie_id = movie_id,
                            rating = movie_rating)
            session.add(r)
        session.commit()

def main(session):
    load_users(session)
    load_movies(session)
    load_ratings(session)

if __name__ == "__main__":
    s = model.connect()
    main(s)

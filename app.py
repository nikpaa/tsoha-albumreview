from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenvt("DB_URL")
db = SQLAlchemy(app)

def get_albums(db) -> list:
    result = db.session.execute("""
        SELECT
          album.id,
          artist.name AS artist,
          album.name,
          album.genre,
          album.year,
          AVG(review.rating) AS rating
        FROM album
        INNER JOIN artist ON artist.id = artist_id
        LEFT JOIN review ON album_id = album.id
        GROUP BY album.id, artist.name, album.name, album.genre, album.year
        ORDER BY AVG(review.rating) DESC;
        """)
    albums = result.fetchall()
    return albums


def get_artist_id(db, artist_name: None | str) -> int:
    sql_id = "SELECT id FROM artist WHERE name = :artist"
    result = db.session.execute(sql_id, { "artist": artist_name } )
    row = result.fetchone()
    if row is None:
        sql_insert = "INSERT INTO artist (name) VALUES (:name);"
        db.session.execute(sql_insert, { "name": artist_name } )
        db.session.commit()
        sql_id = "SELECT id FROM artist WHERE name = :artist"
        result = db.session.execute(sql_id, { "artist": artist_name } )
        row = result.fetchone()
    return row.id

def add_album(db, artist: str | None, name: str | None, genre: str | None, year: str | None):
    artist_id = get_artist_id(db, artist)

    sql = "INSERT INTO album (artist_id, name, genre, year) VALUES (:artist_id, :name, :genre, :year)"
    db.session.execute(sql, { "artist_id": artist_id, "name": name, "genre": genre, "year": year } )
    db.session.commit()

@app.route("/")
def index():
    albums = get_albums(db)
    print(albums)
    return render_template("index.html", count=len(albums), albums=albums)

@app.route("/new-album")
def new():
    return render_template("album.html")

@app.route("/send", methods=["POST"])
def send():
    form = request.form
    print(form)
    artist = none_if_empty(form["artist"])
    name = none_if_empty(form["name"])
    genre = none_if_empty(form["genre"])
    year  = none_if_empty(form["year"])
    add_album(db, artist, name, genre, year)
    return redirect("/")

def add_review(db, reviewer_id, album_id, rating, comments):
   sql = """
        INSERT INTO review (reviewer_id, album_id, rating, comments)
        VALUES (:reviewer_id, :album_id, :rating, :comments);"""
   db.session.execute(sql, { "reviewer_id": reviewer_id, "album_id": album_id, "rating": rating, "comments": comments } )
   db.session.commit()


@app.route("/send-review", methods=["POST"])
def send_review():
    form = request.form
    reviewer_id = none_if_empty(form["reviewer_id"])
    album_id = none_if_empty(form["album_id"])
    rating = none_if_empty(form["rating"])
    comments = none_if_empty(form["comments"])
    add_review(db, reviewer_id, album_id, rating, comments)
    return redirect("/")

@app.route("/review/<album_id>")
def review_album(album_id: str):
    return render_template("review.html", album_id=album_id)


def none_if_empty(x: str) -> str | None:
    if len(x) == 0:
        return None
    else:
        return x

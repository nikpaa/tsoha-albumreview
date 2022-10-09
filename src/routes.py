from app import app
from reviews import get_albums, add_album, add_review
from flask import redirect, render_template, request

def none_if_empty(x: str) -> str | None:
    if len(x) == 0:
        return None
    else:
        return x

@app.route("/")
def index():
    albums = get_albums()
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
    add_album(artist, name, genre, year)
    return redirect("/")

@app.route("/send-review", methods=["POST"])
def send_review():
    form = request.form
    reviewer_id = none_if_empty(form["reviewer_id"])
    album_id = none_if_empty(form["album_id"])
    rating = none_if_empty(form["rating"])
    comments = none_if_empty(form["comments"])
    add_review(reviewer_id, album_id, rating, comments)
    return redirect("/")

@app.route("/review/<album_id>")
def review_album(album_id: str):
    return render_template("review.html", album_id=album_id)

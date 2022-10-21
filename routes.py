from app import app
from queries import add_user, get_albums, get_comments, add_album, add_review, check_login, get_album_name, delete_review, add_follower, delete_follower
from flask import redirect, render_template, request, session

def none_if_empty(x: str) -> str | None:
    if len(x) == 0:
        return None
    else:
        return x


def fix_rating_prec(albums):
    for album in albums:
        if album.rating is not None:
            album.rating = f'{album.rating:.2f}'


@app.route("/")
def index():
    albums = get_albums()
    return render_template("index.html", count=len(albums), albums=albums)

@app.route("/signup-form",methods=["GET"])
def signup_form():
    return render_template("signup-form.html")


@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user_id = check_login(username, password)
    if user_id is not None:
        session["username"] = username
        session["user_id"] = user_id
    return redirect("/")

@app.route("/signup",methods=["POST"])
def signup():
    username = request.form["username"]
    password = request.form["password"]
    add_user(username, password)
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    return redirect("/")

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

@app.route("/comments/<album_id>")
def view_comments(album_id: str):
    comments = get_comments(album_id)
    album_name = get_album_name(album_id)
    return render_template("comments.html", album_name=album_name, comments=comments)

@app.route("/send-review", methods=["POST"])
def send_review():
    form = request.form
    reviewer_id = session["user_id"]
    album_id = none_if_empty(form["album_id"])
    rating = none_if_empty(form["rating"])
    comments = none_if_empty(form["comments"])
    add_review(reviewer_id, album_id, rating, comments)
    return redirect("/")

@app.route("/del-review/<review_id>", methods=["POST"])
def del_review(review_id: str):
    reviewer_id = session["user_id"]
    delete_review(review_id, reviewer_id)
    return redirect("/")

@app.route("/follow/<user_id>", methods=["POST"])
def follow(user_id: str):
    follower_id = session["user_id"]
    add_follower(follower_id, user_id)

@app.route("/unfollow/<user_id>", methods=["POST"])
def unfollow(user_id: str):
    follower_id = session["user_id"]
    delete_follower(follower_id, user_id)

@app.route("/review/<album_id>")
def review_album(album_id: str):
    return render_template("review.html", album_id=album_id)

@app.route("/about")
def show_info():
    return render_template("about.html")


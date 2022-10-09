from db import db
from werkzeug.security import check_password_hash, generate_password_hash

def add_user(username: str, password: str) -> bool:
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO reviewer (name, password) VALUES (:username, :password)"
    try:
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
        return True
    except:
        return False

def check_login(username: str, password: str) -> int | None:
    sql = "SELECT id, password FROM reviewer WHERE name=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user is not None:
        if check_password_hash(user.password, password):
            return user.id
    return None

def get_comments(album_id: str) -> list:
    result = db.session.execute("""
        SELECT
          review.id,
          review.rating,
          review.comments,
          reviewer.name
        FROM review
        INNER JOIN reviewer ON reviewer.id = review.reviewer_id
        WHERE review.album_id = :album_id
    """, {"album_id": album_id})
    comments = result.fetchall()
    return comments

def get_album_name(album_id: str) -> str:
    result = db.session.execute("""
        SELECT name from album WHERE album_id = :album_id
    """, {"album_id": album_id})
    result.fetchone()
    return result.name

def get_albums() -> list:
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


def get_artist_id(artist_name: None | str) -> int:
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

def add_album(artist: str | None, name: str | None, genre: str | None, year: str | None) -> bool:
    artist_id = get_artist_id(artist)

    sql = "INSERT INTO album (artist_id, name, genre, year) VALUES (:artist_id, :name, :genre, :year)"
    try:
        db.session.execute(sql, { "artist_id": artist_id, "name": name, "genre": genre, "year": year } )
        db.session.commit()
        return True
    except:
        return False


def add_review(reviewer_id, album_id, rating, comments) -> bool:
   sql = """
        INSERT INTO review (reviewer_id, album_id, rating, comments)
        VALUES (:reviewer_id, :album_id, :rating, :comments);"""
   try:
       db.session.execute(sql, { "reviewer_id": reviewer_id, "album_id": album_id, "rating": rating, "comments": comments } )
       db.session.commit()
       return True
   except:
       return False

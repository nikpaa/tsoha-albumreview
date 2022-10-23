from typing import Optional
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def add_user(username: str, password: str) -> bool:
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO reviewer (name, password) VALUES (:username, :password)"
    try:
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
        return True
    except:
        return False

def check_login(username: str, password: str) -> Optional[int]:
    sql = "SELECT id, password FROM reviewer WHERE name=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user is not None:
        if check_password_hash(user.password, password):
            return user.id
    return None

def get_profile(user_id: str) -> object:
    sql = """SELECT
      reviewer.id,
      reviewer.name,
      COUNT(DISTINCT follower_id) AS followers
    FROM reviewer
    LEFT JOIN follower ON follower.followee_id = reviewer.id
    WHERE reviewer.id = :user_id
    GROUP BY reviewer.id, reviewer.name;
    """
    result = db.session.execute(sql, {"user_id":user_id})
    profile = result.fetchone()
    return profile

def get_comments(album_id: str) -> list:
    result = db.session.execute("""
        SELECT
          review.id,
          review.rating,
          review.comments,
          reviewer.name,
          reviewer.id AS reviewer_id,
          ROUND(AVG(is_good::int::real)*100) AS pct_helpful
        FROM review
        INNER JOIN reviewer ON reviewer.id = review.reviewer_id
        LEFT JOIN vote ON review.id = vote.review_id
        WHERE review.album_id = :album_id
        GROUP BY review.id, review.rating, review.comments, reviewer.name, reviewer.id
    """, {"album_id": album_id})
    comments = result.fetchall()
    return comments

def get_album_name(album_id: str) -> str:
    result = db.session.execute("""
        SELECT name from album WHERE id = :album_id
    """, {"album_id": album_id})
    album = result.fetchone()
    return album.name

def get_albums() -> list:
    result = db.session.execute("""
        SELECT
          album.id,
          artist.name AS artist,
          album.name,
          album.genre,
          album.year,
          ROUND(AVG(review.rating), 1) AS rating
        FROM album
        INNER JOIN artist ON artist.id = artist_id
        LEFT JOIN review ON album_id = album.id
        GROUP BY album.id, artist.name, album.name, album.genre, album.year
        ORDER BY AVG(review.rating) DESC;
        """)
    albums = result.fetchall()
    return albums

def get_artist_id(artist_name: Optional[str]) -> int:
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

def add_album(artist: Optional[str], name: Optional[str],
              genre: Optional[str], year: Optional[str]) -> bool:
    artist_id = get_artist_id(artist)

    sql = """
    INSERT INTO album (artist_id, name, genre, year)
    VALUES (:artist_id, :name, :genre, :year);
    """
    try:
        db.session.execute(sql, { "artist_id": artist_id, "name": name,
                                  "genre": genre, "year": year } )
        db.session.commit()
        return True
    except:
        return False

def add_review(reviewer_id: str, album_id: str, rating: str, comments: str) -> bool:
    valid = ["1","2","3","4","5"]
    if rating not in valid:
        return False
    sql = """
        INSERT INTO review (reviewer_id, album_id, rating, comments)
        VALUES (:reviewer_id, :album_id, :rating, :comments);"""
    try:
        db.session.execute(sql, { "reviewer_id": reviewer_id,
                                  "album_id": album_id,
                                  "rating": rating,
                                  "comments": comments } )
        db.session.commit()
        return True
    except:
        return False

def delete_review(review_id: str, reviewer_id: str):
    sql = """
          DELETE FROM review WHERE id = :review_id AND reviewer_id = :reviewer_id;
    """
    db.session.execute(sql, { "review_id": review_id, "reviewer_id": reviewer_id } )
    db.session.commit()

def add_follower(follower_id: str, followee_id: str):
    sql = """
          SELECT id FROM follower
          WHERE follower_id = :follower_id AND followee_id = :followee_id;
    """
    result = db.session.execute(sql, { "follower_id": follower_id, "followee_id": followee_id } )
    if len(result.fetchall()) == 0:
        sql = """
              INSERT INTO follower (follower_id, followee_id) VALUES (:follower_id, :followee_id);
        """
        db.session.execute(sql, { "follower_id": follower_id, "followee_id": followee_id } )
        db.session.commit()

def delete_follower(follower_id: str, followee_id: str):
    sql = """
          DELETE FROM follower WHERE follower_id = :follower_id AND followee_id = :followee_id;
          """
    db.session.execute(sql, { "follower_id": follower_id, "followee_id": followee_id } )
    db.session.commit()

def add_vote(review_id: str, voter_id: str, is_good: str):
    sql_del = """
          DELETE FROM vote WHERE review_id = :review_id AND reviewer_id = :reviewer_id;
          """
    sql_ins = """
          INSERT INTO vote (review_id, reviewer_id, is_good)
          VALUES (:review_id, :reviewer_id, :is_good);
          """
    db.session.execute(sql_del, { "review_id": review_id, "reviewer_id": voter_id } )
    db.session.execute(sql_ins, { "review_id": review_id, "reviewer_id": voter_id,
                                  "is_good": is_good } )
    db.session.commit()

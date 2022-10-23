from os import getenv
import re
from flask_sqlalchemy import SQLAlchemy
from app import app

# heroku provides the url in the wrong format
def fix_pg_url(pg_url: str) -> str:
    return re.sub("^postgres:", "postgresql:", pg_url)

app.config["SQLALCHEMY_DATABASE_URI"] = fix_pg_url(getenv("DATABASE_URL"))
db = SQLAlchemy(app)

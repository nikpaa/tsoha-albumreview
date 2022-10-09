from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv
import re

# heroku provides the url in the wrong format
def fix_pg_url(input: str) -> str:
    return re.sub("^postgres:", "postgresql:", input)

app.config["SQLALCHEMY_DATABASE_URI"] = fix_pg_url(getenv("DATABASE_URL"))
db = SQLAlchemy(app)


import os
import flask
from cryptography.fernet import Fernet


app = flask.Flask("app")

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
HOST = os.getenv("HOST")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{HOST}:5432/images"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["IMAGE_ENCRYPTION_KEY"] = Fernet.generate_key()

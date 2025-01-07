import os
import flask
import uuid
from io import BytesIO
import hashlib
from db.image import Image
from create_app import app
from db import db
from cryptography.fernet import Fernet
from datetime import datetime, timedelta

IMAGE_FOLDER = "./images/"

KEY = app.config["IMAGE_ENCRYPTION_KEY"]
CIPHER = Fernet(KEY)

if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)


@app.route("/upload", methods=["POST"])
def upload() -> flask.Response:

    cleanup()

    file = flask.request.files["file"]
    file_uuid = str(uuid.uuid4())
    filename = hashlib.sha256(string=file_uuid.encode()).hexdigest()
    file_data = file.read()

    encrypted_data = CIPHER.encrypt(file_data)

    encrypted_image_path = os.path.join(IMAGE_FOLDER, filename)

    with open(encrypted_image_path, "wb") as f:
        f.write(encrypted_data)

    new_image = Image(filename=filename, timestamp=datetime.now())
    db.session.add(new_image)
    db.session.commit()

    return flask.Response(file_uuid, status=200)


@app.route("/image/<file_uuid>", methods=["GET"])
def image(file_uuid: str) -> flask.Response:

    cleanup()
    filename = hashlib.sha256(string=file_uuid.encode()).hexdigest()
    image_path = os.path.join(IMAGE_FOLDER, filename)

    if not os.path.isfile(image_path):

        return flask.Response("Error: Image not found.", 404)

    with open(image_path, "rb") as f:
        encrypted_image_data = f.read()

    try:
        decrypted_image_data = CIPHER.decrypt(encrypted_image_data)

    except:
        return flask.Response(
            "Error: Image was not able to load due to a server restart.", 404
        )

    return flask.send_file(BytesIO(decrypted_image_data), mimetype="image/jpeg")


@app.route("/cleanup")
def cleanup():

    now = datetime.now()

    threshold_time = now - timedelta(minutes=5)
    old_images = Image.query.filter(Image.timestamp < threshold_time).all()

    for image in old_images:

        image_path = os.path.join(IMAGE_FOLDER, image.filename)
        if os.path.exists(image_path):
            os.remove(image_path)

        db.session.delete(image)

    db.session.commit()

    return flask.Response(f"Deleted {len(old_images)} old images.", status=200)


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=False)

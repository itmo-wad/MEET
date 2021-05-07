import os
from io import BytesIO

from PIL import Image, ImageOps, ImageDraw
from flask import url_for


def getAvatar(username, app):
    default_ava = 'static/img/avatar.png'
    photo = username + '.png'
    photo_path = './static/img/userava/' + photo
    if not os.path.isfile(photo_path):
        with app.open_resource(app.root_path + url_for('static', filename='img/avatar.png'), "rb") as f:
            img = f.read()
    else:
        with app.open_resource(app.root_path + url_for('static', filename='img/userava/' + photo), "rb") as f:
            img = f.read()
    return img


def updateAva(username, img):
    if not img:
        return False
    try:
        filename = username + '.png'
        img = Image.open(BytesIO(img))
        size = (200, 200)
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)

        img = img.resize(size)

        output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        output.thumbnail(size, Image.ANTIALIAS)
        output.save('./static/img/userava/' + filename)
    except:
        return False
    return True


def isPhoto(filename):
    right_ext = ['png', 'jpg', 'jpeg', 'tiff', 'bmp', 'gif']
    ext = filename.rsplit('.', 1)[1]
    ext = ext.lower()
    if ext in right_ext:
        return True
    return False

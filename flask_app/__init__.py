from flask import Flask
from flask_bcrypt import Bcrypt
import os
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = os.path.realpath(
    os.getcwd() + '/flask_app/uploads')

app.secret_key = "thrify is nifty"

bcrypt = Bcrypt(app)

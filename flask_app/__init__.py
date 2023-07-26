from flask import Flask
from flask_bcrypt import Bcrypt
app = Flask(__name__)

import os

app.secret_key = "thrify is nifty"

bcrypt = Bcrypt(app)

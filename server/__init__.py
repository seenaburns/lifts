from flask import Flask

# Config
DATABASE = './data/lift.db'
SECRET_KEY = ''

app = Flask(__name__)
app.config.from_object(__name__)

import server.core

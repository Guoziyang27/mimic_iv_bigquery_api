from flask import Flask
from flask_cors import CORS
import json

from blueprint.icu import icu
from blueprint.core import core

from module.connect import connect

connect()

app = Flask(__name__)
CORS(app)

app.register_blueprint(icu, url_prefix='/icu')
app.register_blueprint(core, url_prefix='/core')


@app.route('/')
def check_access():
    return 'MIMIC-IV API'

if __name__ == '__main__':
    # app.run(host="0.0.0.0")
    app.run()
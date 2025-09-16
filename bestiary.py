import os
from bestiary_funcs import retrieve_beast, retrieve_natures
from dotenv import load_dotenv
from flask import Flask, abort
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

# Env variables
load_dotenv()
BESTIARY_CORS_ALLOWED_ORIGINS = [x.strip() for x in os.environ['BESTIARY_CORS_ALLOWED_ORIGINS'].split(',')]

app = Flask(__name__)
CORS(app=app, origins=BESTIARY_CORS_ALLOWED_ORIGINS);

@app.route("/species")
def species():
    return retrieve_natures()

@app.route("/beast/<string:beast_key>")
def beast(beast_key):
    beast = retrieve_beast(beast_key)
    if beast is not None:
        return beast
    else:
        abort(404)

@app.route("/different-page")
def different_page():
    return "<p>ARE YOU NOT ENTERTAINED</p>"

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
from flask import Flask, abort
from werkzeug.middleware.proxy_fix import ProxyFix
from bestiary_funcs import retrieve_beast, retrieve_natures

app = Flask(__name__)

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
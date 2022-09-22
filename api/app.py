from flask import Flask, redirect, request
from flask_smorest import Api
from flask_wtf.csrf import CSRFProtect

from api.nuvocalc.blueprints import blp as nuvocalc_blp
from api.nuvoutils.blueprints import blp as nuvoutils_blp
from api.settings import DefaultConfig


def create_app():
    app = Flask(__name__)
    csrf = CSRFProtect(app)
    app.config.from_object(DefaultConfig)
    _api = Api(app)

    # exempt from csrf
    csrf.exempt(nuvoutils_blp)
    csrf.exempt(nuvocalc_blp)

    # register blueprints
    _api.register_blueprint(nuvoutils_blp)
    _api.register_blueprint(nuvocalc_blp)

    return app


app = create_app()


@app.route("/")
def home():
    return redirect("/swagger", code=302)


@app.before_request
def log_request():
    if app.debug:
        print(request.headers)
        print(request.data)

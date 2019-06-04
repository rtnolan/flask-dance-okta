import os
from flask import Flask, redirect, url_for
from flask_dance.contrib.okta import make_okta_blueprint, okta


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.config["OKTA_OAUTH_CLIENT_ID"] = os.environ.get("OKTA_OAUTH_CLIENT_ID")
app.config["OKTA_OAUTH_CLIENT_SECRET"] = os.environ.get("OKTA_OAUTH_CLIENT_SECRET")

okta_bp = make_okta_blueprint(
    base_url=os.environ.get("OKTA_BASE_URL"),
    authorization_url=os.environ.get("OKTA_AUTH_URL"),
    token_url=os.environ.get("OKTA_TOKEN_URL")
)
app.register_blueprint(okta_bp, url_prefix="/login")

@app.route("/")
def index():
    if not okta.authorized:
        return redirect(url_for("okta.login"))
    resp = okta.get("/oauth2/default/v1/userinfo")
    assert resp.ok, resp.text
    return "You are {name} on Okta".format(name=resp.json()["name"])
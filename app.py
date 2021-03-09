from logging.config import dictConfig

from flask import Flask, send_file, send_from_directory
from flask import jsonify
from flask import request
from flask_cors import CORS

from aws import ddb
from ghub.actions import process_repo
from logging_config import LOG_CONF

dictConfig(LOG_CONF)

app = Flask(__name__)
CORS(app)

SENTIMENT_COLOR_MAP = {
    "POSITIVE": "green",
    "NEGATIVE": "red",
    "QUEUED": "orange",
    "NOT_FOUND": "grey",
}


@app.route("/", methods=["GET"])
def index(event=None, context=None):
    return send_file("./static/index.html")


@app.route("/denim.png", methods=["GET"])
def denim_png():
    return send_file("./static/denim.png")


@app.route("/gh-logo.png", methods=["GET"])
def gh_logo_png():
    return send_file("./static/gh-logo.png")


@app.route("/s", methods=["GET"])
def shields_badge_for_repo():
    repo_name = request.args.get("gh_repo_name")
    badge_data = ddb.get_item(repo_name)
    if not badge_data:
        badge_data = {"final_sentiment": "NOT_FOUND"}

    final_sentiment = badge_data.get("final_sentiment", "NOT_FOUND")
    sentiment_color = SENTIMENT_COLOR_MAP.get(final_sentiment, "grey")

    return {"schemaVersion": 1, "label": "mood", "message": final_sentiment, "color": sentiment_color}


@app.route("/gh/submit/repo", methods=["POST"])
def submit_repo(event=None, context=None):
    gh_repo_name = request.json.get("gh_repo_name")
    try:
        ddb.save_item(gh_repo_name, "PROCESSING", {}, only_if_absent=True)
    except:
        pass

    data_block = {}
    err_message = ""

    try:
        data_block = process_repo(gh_repo_name)
    except Exception as ex:
        err_message = str(ex)

    if not data_block:
        data_block = {"final_sentiment": "QUEUED", "error": err_message}

    ddb.save_item(gh_repo_name, data_block["final_sentiment"], data_block)
    return {"status": "ok", "message": f"Repo {gh_repo_name} successfully submitted"}


if __name__ == "__main__":
    app.run(debug=True, port=5000)

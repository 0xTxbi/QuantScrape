from flask import Flask, jsonify
from .scraper.scraper_logic import scrape_homepage

app = Flask(__name__)


@app.route("/upcoming-earnings", methods=["GET"])
def get_upcoming_earnings():
    try:
        # execute scrape function
        upcomingEarnings = scrape_homepage()
        print(upcomingEarnings)
        return upcomingEarnings
    except Exception as e:
        return jsonify({"error": f"An error was encountered: {e}"})


if __name__ == "__main__":
    app.run(port=4000, debug=True)

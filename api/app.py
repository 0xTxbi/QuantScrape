from flask import Flask
from scraper.scraper_logic import scrape_homepage

app = Flask(__name__)


@app.route("/upcoming-earnings", methods=["GET"])
def get_upcoming_earnings():
    # execute scrape function
    upcomingEarnings = scrape_homepage()
    print(upcomingEarnings)
    return upcomingEarnings


if __name__ == "__main__":
    app.run(port=4000, debug=True)

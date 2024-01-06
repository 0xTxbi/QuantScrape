from flask import Flask, jsonify
from .scraper.scraper_logic import scrape_homepage
from .utils import cache_result, get_cached_result

app = Flask(__name__)


@app.route("/upcoming-earnings", methods=["GET"])
def get_upcoming_earnings():
    try:
        # first check if we have the value in cache
        cached_upcoming_earnings = get_cached_result("earnCall")

        if cached_upcoming_earnings:
            # if data exists in cache, return it
            return cached_upcoming_earnings

        # else, execute the scrape function
        upcoming_earnings = scrape_homepage()

        # store the scraped data in the cache
        cache_result("earnCall", upcoming_earnings)

        return upcoming_earnings
    except Exception as e:
        return jsonify({"error": f"An error was encountered: {e}"})


if __name__ == "__main__":
    app.run(port=4000, debug=True)

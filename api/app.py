from flask import Flask, jsonify
from flask_cors import CORS
from .scraper.scraper_logic import (
    scrape_homepage,
    scrape_top_gainers,
    scrape_stock_quote,
    scrape_stock_historical_data,
)
from .utils import cache_result, get_cached_result


app = Flask(__name__)
# temp – enable cors for all routes
CORS(app)


# welcome agents
@app.route("/", methods=["GET"])
def index():
    ascii_art = """
    Welcome to QuantScrape!
     __    __     _                            
    / / /\ \ \___| | ___ ___  _ __ ___   ___  
    \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \ 
     \  /\  /  __/ | (_| (_) | | | | | |  __/ 
      \/  \/ \___|_|\___\___/|_| |_| |_|\___| 
                                              
    Harness the power of AI for financial data scraping.
    """
    return "<pre>" + ascii_art + "</pre>"


# retrieve stock's historical data
@app.route("/historical-data/<ticker>", methods=["GET"])
def get_stock_historical_data(ticker):
    try:
        # execute the scrape function
        stock_historical_data = scrape_stock_historical_data(ticker)

        print(stock_historical_data)
        return jsonify({"stock_historical_data": stock_historical_data})
    except Exception as e:
        return jsonify({"error": f"An error was encountered: {e}"})


# retrieve stock's financials
@app.route("/quote/<ticker>", methods=["GET"])
def get_stock_financials(ticker):
    try:
        # execute the scrape function
        stock_quote = scrape_stock_quote(ticker)

        print(stock_quote)
        return jsonify({"stock_info": stock_quote})
    except Exception as e:
        return jsonify({"error": f"An error was encountered: {e}"})


# retrieve market gainers
@app.route("/market-gainers", methods=["GET"])
def get_market_gainers():
    try:
        # first check if we have the value in cache
        cached_market_gainers = get_cached_result("marketGainers")

        if cached_market_gainers:
            # if data exists in cache, return it
            return jsonify({"market_gainers": f"{cached_market_gainers}"})

        # else, execute the scrape function
        market_gainers = scrape_top_gainers()

        # store the scraped data in the cache
        cache_result("marketGainers", market_gainers)

        return jsonify({"market_gainers": market_gainers})
    except Exception as e:
        return jsonify({"error": f"An error was encountered: {e}"})


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

# importing necessary libraries
import requests
from lxml import etree
import json
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import (
    BeautifulSoupTransformer,
    Html2TextTransformer,
)
from langchain_core.pydantic_v1 import BaseModel
from langchain.text_splitter import RecursiveCharacterTextSplitter

# custom modules
from . import setup_environment, setup_language_model, prompt_gen, parse_data

# loading environment variables
setup_environment()

# setting up language model
llm = setup_language_model()


# top market gainers data structure
class TopGainers(BaseModel):
    symbol: str
    company: str
    price: str
    change: str
    percent_change: str


# stock financials data structure
class StockBasic(BaseModel):
    symbol: str
    company: str
    current_price: float
    # represents the previous close value
    previous_close: float
    # represents the open value
    open_price: float
    # represents the day's range value
    days_range: str
    # represents the 52 week range value
    week_range_52: str
    # represents the volume value
    volume: str
    # represents the average volume value
    avg_volume: str
    # represents the market cap value
    market_cap: str
    # represents the pe ratio (TTM) value (optional, as it might be missing)
    pe_ratio_ttm: float
    # represents the eps (TTM) value (optional, as it might be missing)
    eps_ttm: float
    # represents the earnings date value
    earnings_date: str


# parsing data
parsedMarketGainers = parse_data(TopGainers)
parsedStockFinancials = parse_data(StockBasic)


#  function to scrape stock financials
def scrape_stock_financials(ticker=str):
    # defining the URL to scrape
    url = f"https://finance.yahoo.com/quote/{ticker}"
    print(url)
    loader = AsyncHtmlLoader(url, verify_ssl=False)
    pages_html = loader.load()
    # instantiate html transformer
    html2text = Html2TextTransformer()
    transformed_request = html2text.transform_documents(pages_html)

    print(f"Extracting {ticker} financials.....")

    # grab the first 1500 tokens of the page
    content_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=0)

    splitted_content = content_splitter.split_documents(transformed_request)

    # # extract the string
    splitted_content_str = splitted_content[0].page_content[750:2000]

    # Call prompt_and_llm with splitted_content_str as part of the template
    output = prompt_gen(
        "this is the company's basic financial info",
        splitted_content_str,
        parsedStockFinancials,
        llm,
    )

    print(output)

    return output


# function to scrape top gainers
def scrape_top_gainers():
    # defining the URL to scrape
    url = "https://www.google.com/finance/markets/gainers"
    print(url)
    # creating an instance of AsyncHtmlLoader
    loader = AsyncHtmlLoader(url, verify_ssl=False)
    # loading the HTML of the page
    pages_html = loader.load()
    # creating an instance of BeautifulSoupTransformer
    bs_transformer = BeautifulSoupTransformer()

    # transforming the documents
    transformed_request = bs_transformer.transform_documents(
        pages_html, ["scripts", "style", "meta", "link"], ["div"]
    )

    print("Extracting top gainers info.....")

    # splitting the content into chunks
    content_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=0)
    splitted_content = content_splitter.split_documents(transformed_request)

    # extracting the string
    splitted_content_str = splitted_content[0].page_content

    # generating the prompt
    output = prompt_gen(
        "these are top gaining stocks",
        splitted_content_str,
        parsedMarketGainers,
        llm,
    )

    # returning the output as a JSON object
    return output


# function to scrape homepage
def scrape_homepage():
    # defining the URL to scrape
    url = "https://www.google.com/finance/"
    # specifying user agent
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        # sending GET request
        response = requests.get(url, headers=headers, verify=False)

        # checking if the request was successful
        if response.status_code == 200:
            content = response.text
            tree = etree.HTML(content)
            xpath = "/html/body/c-wiz[2]/div/div[4]/div/div/div[2]/c-wiz[3]/section"
            events_calendar = tree.xpath(xpath)

            # extracting details from the events calendar section if found
            if events_calendar:
                for element in events_calendar[0]:
                    month = element.find(".//div[@class='VS9TYb']").text
                    day = element.find(".//div[@class='Z1cdGd']").text
                    company = element.find(".//a[@class='qNqwJf']").text
                    link = element.find(".//a[@class='qNqwJf']").get("href")
                    date = f"{month} {day}"
                    ticker = link.split("/")[2].split(":")[0]

                    # creating a JSON object with the extracted details
                    earningCallResult = json.dumps(
                        {
                            "date": date,
                            "company": company,
                            "ticker": ticker,
                        }
                    )

                    # returning the JSON object
                    return earningCallResult
            else:
                # returning an error message if no events were found
                return json.dumps({"error": "No events found"})
        else:
            # returning an error message if the request failed
            return json.dumps({"error": "Failed to fetch events calendar"})
    except requests.RequestException as e:
        # returning an error message if there was an exception during the request
        return json.dumps({"error": f"Error during request: {e}"})


# testing the scraper logic
if __name__ == "__main__":
    # testing the scraping functions
    result = scrape_stock_financials("lmt")

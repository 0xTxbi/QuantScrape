import requests
from lxml import etree
import os
import json
from dotenv import load_dotenv
from langchain_community.document_loaders import AsyncHtmlLoader

from langchain_community.llms import Together
from langchain_core.output_parsers import JsonOutputParser
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()


# llm
llm = Together(
    model=os.getenv("LLM_PROVIDER_MODEL"),
    temperature=0.7,
    max_tokens=500,
    top_k=1,
    together_api_key=os.getenv("LLM_PROVIDER_API_KEY"),
)


# parsed data structure
class TopGainers(BaseModel):
    symbol: str
    company: str
    price: str
    change: str
    percent_change: str


parser = JsonOutputParser(pydantic_object=TopGainers)


prompt = PromptTemplate(
    template="this is scraped from a website.\n\n\n{splitted_content}\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# prompt llm to populate the data structure
prompt_and_llm = prompt | llm | parser


# transform page
def scrape_top_gainers():
    url = "https://www.google.com/finance/markets/gainers"
    loader = AsyncHtmlLoader(url, verify_ssl=False)
    pages_html = loader.load()
    bs_transformer = BeautifulSoupTransformer()

    transformed_request = bs_transformer.transform_documents(
        pages_html, ["scripts", "style", "meta", "link"], ["div"]
    )

    print("Extracting info.....")

    # grab the first 1500 tokens of the page
    content_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=0)
    splitted_content = content_splitter.split_documents(transformed_request)

    splitted_content_str = splitted_content[0].page_content

    print(splitted_content_str)

    # Call prompt_and_llm with splitted_content_str as part of the template
    output = prompt_and_llm.invoke(
        {
            "query": "extract the first 5 top gaining stocks from it and organise it in key value pairs.",
            "splitted_content": splitted_content_str,
        }
    )

    return output


def scrape_homepage():
    # google finance homepage url
    url = "https://www.google.com/finance/"

    # specify user agent
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, verify=False)

        if response.status_code == 200:
            content = response.text
            tree = etree.HTML(content)
            xpath = "/html/body/c-wiz[2]/div/div[4]/div/div/div[2]/c-wiz[3]/section"
            events_calendar = tree.xpath(xpath)

            # extract details from the events calendar section if found
            if events_calendar:
                for element in events_calendar[0]:
                    month = element.find(".//div[@class='VS9TYb']").text
                    day = element.find(".//div[@class='Z1cdGd']").text
                    company = element.find(".//a[@class='qNqwJf']").text
                    link = element.find(".//a[@class='qNqwJf']").get("href")
                    date = f"{month} {day}"
                    ticker = link.split("/")[2].split(":")[0]

                    earningCallResult = json.dumps(
                        {
                            "date": date,
                            "company": company,
                            "ticker": ticker,
                        }
                    )

                    return earningCallResult
            else:
                return json.dumps({"error": "No events found"})

        else:
            return json.dumps({"error": "Failed to fetch events calendar"})
    except requests.RequestException as e:
        return json.dumps({"error": f"Error during request: {e}"})


# test scraper logic
if __name__ == "__main__":
    #  test intelligent scraping

    result = scrape_top_gainers()
    print(result)

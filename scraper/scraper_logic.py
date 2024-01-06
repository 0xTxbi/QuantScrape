import requests
from lxml import etree


def scrape_homepage():
    # google finance homepage url
    url = "https://www.google.com/finance/"

    # specify user agent
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)

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
                    ticker = link.split("/")[2].split(":")[0]
                    print(f"{month} {day}, {company}, {ticker}")
            else:
                print("No events found")

        else:
            return "Failed to fetch events calendar"
    except requests.RequestException as e:
        return f"Error during request: {e}"


# test scraper logic
if __name__ == "__main__":
    events_deets = scrape_homepage()
    print(f"events deets: {events_deets}")

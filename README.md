# QuantScrape

Welcome to QuantScrape, my personal project tailored for efficient and
intelligent web scraping of financial data. I embarked on this project to
streamline the process of gathering valuable insights for quantitative analysis,
modeling, and research within the finance domain.

## Overview

QuantScrape harnesses the power of Large Language Models (LLMs) to intelligently
parse financial data from diverse web sources. This ensures a high level of
efficiency and accuracy in extracting relevant information for your quantitative
endeavors. The project is implemented in Python and exposes its capabilities
through a Flask API, making it **effortlessly integrable** into various
applications and services.

## Key Features

### 1. Efficient and Intelligent Web Scraping

QuantScrape employs advanced LLMs to comprehend and parse financial data,
ensuring the extraction of pertinent information with precision and speed.

### 2. Flask API Integration

The core functionality of QuantScrape is made accessible through a Flask API,
facilitating seamless integration into other applications and services.

### 3. Intelligent and Efficient Parsing

QuantScrape intelligently parses and validates scraped data, ensuring
consistency and ease of use for downstream applications.

## API Endpoints

QuantScrape provides a set of intuitive and versatile API endpoints to cater to
your diverse financial data needs. Here's a breakdown of each endpoint:

### 1. `GET /historical-data/<ticker>`

Retrieve detailed historical data for a specific stock by replacing `<ticker>`
with the corresponding stock symbol. This endpoint is perfect for conducting
in-depth analysis and trend assessments.

### 2. `GET /quote/<ticker>`

Fetch real-time quote details for a particular stock using its ticker symbol.

### 3. `GET /market-gainers`

Get a curated list of top gaining stocks in the market. Identify potential
investment opportunities and stay ahead of market trends.

### 4. `GET /upcoming-earnings`

Access a comprehensive list of companies with upcoming earnings calls. Stay
informed about crucial financial events that might impact your investment
strategy.

Each endpoint is designed for ease of use, delivering relevant data efficiently
to empower your quantitative analysis and decision-making processes. Simply make
a `GET` request to the desired endpoint and let QuantScrape handle the rest.

## Tech Stack

QuantScrape is crafted using the following technologies:

- **Python**: The primary programming language used.
- **Flask**: A lightweight web framework powering the API.
- **Pydantic**: A data validation library for parsing and validating scraped
  data intelligently.
- **Redis**: A caching database to enhance performance.

## License

This project is licensed under the Apache License.

Feel free to explore, integrate, and enhance QuantScrape for your financial data
needs. Happy coding!

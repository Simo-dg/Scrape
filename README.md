# Project Documentation: Scrape
## Disclaimer

This project is intended for educational purposes only. It demonstrates techniques for web scraping using Python. The code in this project should not be used to scrape websites that explicitly disallow web scraping in their terms of service. Always respect the terms of service of any website you scrape.

## Overview

This project is a web scraping application that collects and compares prices of refurbished mobile phones from two different marketplaces: BackMarket and Refurbed. The application is divided into two main components - the web scraper (`project.py`) and a web interface (`user.py`) built using Flask.

## Table of Contents

1. [Project Structure](#1-project-structure)
2. [Web Scraper (`project.py`)](#2-web-scraper-projectpy)
   - [Dependencies](#dependencies)
   - [Functions](#functions)
   - [Database Structure](#database-structure)
3. [Web Interface (`user.py`)](#3-web-interface-userpy)
   - [Dependencies](#dependencies-1)
   - [Routes](#routes)
4. [Frontend (`index.html` and `results.html`)](#4-frontend-indexhtml-and-resulthtml)
   - [Template Structure](#template-structure)
   - [Dynamic Content with JavaScript](#dynamic-content-with-javascript)
5. [Styles (`styles.css`)](#5-styles-stylescss)
6. [Usage](#6-usage)
   - [Setup](#setup)
   - [Run the Application](#run-the-application)
7. [Conclusion](#7-conclusion)
8. [Important Notes](#8-Important-Notes)

## 1. Project Structure


The project consists of the following components:

- `project.py`: The web scraper script responsible for fetching and parsing data from Back Market and Refurbed.
- `user.py`: The Flask web application serving as a user interface to search and compare prices.
- `index.html`: The HTML template for the main page, displaying available phone models.
- `results.html`: The HTML template for displaying search results and historical price trends.
- `static/`: Directory containing the CSS styles (`styles.css`) used in the web interface.

## 2. Web Scraper (`project.py`)

### Dependencies

The web scraper script utilizes the following Python libraries:

- `BeautifulSoup`: For HTML parsing.
- `urllib3`: For handling HTTP requests.
- `requests_html`: For rendering JavaScript-based content.
- `sqlite3`: For managing the SQLite database.
- `re`: For regular expressions.
- `time`: For introducing delays in scraping to avoid being blocked.

### Functions

The key functions in `project.py` include:

- `fetch_and_parse(url)`: Fetches and parses HTML content from a given URL.
- `get_product_links(soup, codes)`: Extracts product links from the parsed HTML using specified codes.
- `get_color_links(soup, colors)`: Extracts color-specific links from the parsed HTML.
- `insert_into_db(conn, url, pattern, model, storage_capacity, color)`: Inserts scraped data into the SQLite database.
- Price extraction functions (`get_price_backmarket` and `get_price_refurbed`): Extracts prices from Back Market and Refurbed respectively.
- `get_region(url)`: Extracts the region from the given URL.
- `get_options(soup, pattern)`: Extracts options such as colors and storage capacities from Refurbed.

### Database Structure

The SQLite database (`data.db`) consists of two tables:

1. `product_url`: Stores product codes, URLs, and timestamp information.
2. `scrapped_data`: Stores detailed information about each product including model, storage, color, date, time, price, marketplace, and region.

## 3. Web Interface (`user.py`)

### Dependencies

The Flask web application script utilizes the following Python libraries:

- `Flask`: The web framework for creating the user interface.
- `sqlite3`: For connecting to the SQLite database.
- `jsonify`: For converting data to JSON format.
- `session`: For maintaining user session data.

### Routes

- `/`: Renders the index page displaying available phone models.
- `/get_options`: Handles AJAX requests to fetch color and storage options based on the selected model.
- `/search`: Processes form submissions to search for and display price information.
- `/price-trend`: Retrieves historical price data for creating price trend charts.

## 4. Frontend (`index.html` and `results.html`)

### Template Structure

- `index.html`: Displays a form with dropdowns for selecting phone models, colors, and storage capacities.
- `results.html`: Displays search results including the model, storage, color, price, marketplace, and a link to the product.

### Dynamic Content with JavaScript

- Uses jQuery to dynamically update color and storage dropdowns based on the selected phone model.
- Uses Chart.js to display historical price trends in a line chart.

## 5. Styles (`styles.css`)

- Contains CSS styles for the web interface elements, ensuring a visually appealing and responsive design.

## 6. Usage

### Setup

1. Ensure you have Python installed. Then, install the project dependencies:

```bash
pip install -r requirements.txt
```
2. Ensure SQLite is installed.

### Run the Application

1. Run `project.py` to initiate the web scraping process.
   ```bash
   python project.py
   ```
2. Run `user.py` to start the Flask web application.
   ```bash
   python user.py
   ```
3. Access the application in a web browser at `http://localhost:5000`.

## 7. Conclusion

This project provides a comprehensive solution for comparing prices of refurbished mobile phones from Back Market and Refurbed. The web scraper fetches and stores data in an SQLite database, and the Flask web application offers a user-friendly interface for searching and visualizing price trends.

## 8. Important Notes
- Running the scraping script may take some time due to limitations imposed by the target websites. It is recommended to run the script periodically to update data.

- The web application is intended for demonstrative purposes and may require further enhancements for production use.

- Ensure compliance with privacy regulations and the terms of service of the target websites when scraping data.






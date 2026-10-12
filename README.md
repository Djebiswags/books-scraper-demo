# Books Scraper Demo

A portfolio web-scraping demo: paginated catalogue crawl of
[books.toscrape.com](https://books.toscrape.com) with detail-page extraction,
exported to CSV.

## What it does

- Crawls the catalogue page by page (default: 10 pages = 200 books)
- Visits each book's detail page to pull the full description
- Handles relative URLs, mislabeled charset (UTF-8 forced so £ renders),
  and star-rating CSS classes
- Polite by default: 0.15s delay between detail requests

## Run it

```bash
pip install requests beautifulsoup4
python3 scrape_books.py        # 10 pages → books.csv
python3 scrape_books.py 3      # 3 pages → 60 books
```

## Output

`books.csv` — 200 rows with `title, price, rating, in_stock, description, url`.

Sample:

```
A Light in the Attic,£51.77,3,True,"It's hard to imagine a world without...",https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html
```

Built with Python, `requests`, `BeautifulSoup`. Part of my freelance
portfolio — I build scrapers, automation scripts, and bots for clients.

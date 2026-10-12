#!/usr/bin/env python3
"""Scrape books.toscrape.com — paginated catalogue crawl + detail-page extraction.

Usage:
    python3 scrape_books.py [max_pages]   # default 10 pages = 200 books

Output: books.csv with title, price, rating, in_stock, description, url.
"""
import csv
import sys
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE = "https://books.toscrape.com/"
CATALOGUE = urljoin(BASE, "catalogue/")
RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; portfolio-demo/1.0)"}


def get(url):
    r = requests.get(url, timeout=20, headers=HEADERS)
    r.encoding = "utf-8"  # site mislabels charset; force it so £ renders
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")


def parse_listing(soup):
    books = []
    for pod in soup.select("article.product_pod"):
        a = pod.select_one("h3 a")
        books.append({
            "title": a["title"].strip(),
            "price": pod.select_one("p.price_color").get_text(strip=True),
            "rating": RATINGS.get(pod.select_one("p.star-rating")["class"][1], 0),
            "in_stock": "In stock" in pod.select_one("p.instock").get_text(),
            "url": urljoin(CATALOGUE, a["href"]),
        })
    return books


def parse_detail(url):
    soup = get(url)
    desc_h = soup.select_one("#product_description")
    if desc_h and desc_h.find_next_sibling("p"):
        return desc_h.find_next_sibling("p").get_text(strip=True)
    return ""


def main(max_pages=10, out="books.csv"):
    rows = []
    url = urljoin(CATALOGUE, "page-1.html")
    for _ in range(max_pages):
        soup = get(url)
        for b in parse_listing(soup):
            b["description"] = parse_detail(b["url"])
            rows.append(b)
            time.sleep(0.15)  # be polite
        nxt = soup.select_one("li.next a")
        if not nxt:
            break
        url = urljoin(url, nxt["href"])
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f, fieldnames=["title", "price", "rating", "in_stock", "description", "url"]
        )
        w.writeheader()
        w.writerows(rows)
    print(f"Saved {len(rows)} books -> {out}")


if __name__ == "__main__":
    mp = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    main(max_pages=mp)

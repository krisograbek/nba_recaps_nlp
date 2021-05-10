import os

from scraper import get_site_text


def get_articles_from_www():
    articles = get_site_text("20210504", 2)
    sentences = []
    for article in articles:
        starts = []
        print(" - " *20)
        print(article[0])


if __name__ == '__main__':
    get_articles_from_www()

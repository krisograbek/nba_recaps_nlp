import argparse

from scraper import get_site_text
from helpers import store_articles, load_articles


def parse_arguments():
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('--date', type=str, help='ending date in format "YYYYMMDD"')
    my_parser.add_argument('--days', type=int, help='last x days to scrape. Max 7')
    args = my_parser.parse_args()

    return args


def get_articles_from_www(args):
    # store games info with the whole recap articles
    store_articles(get_site_text(args.date, args.days))


def main():
    args = parse_arguments()
    get_articles_from_www(args)

    articles = load_articles()
    for art in articles:
        print(art[0])


if __name__ == '__main__':
    main()

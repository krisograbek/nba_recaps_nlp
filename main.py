import argparse

from scraper import get_site_text
from extractor import extract_stats
from helpers import (
    store_pickle, 
    load_pickle,
    filter_out_upper
)


def parse_arguments():
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('--date', type=str, help='ending date in format "YYYYMMDD"')
    my_parser.add_argument('--days', type=int, help='last x days to scrape. Max 7')
    my_parser.add_argument('--scrape', action="store_true", help='if set, scraping should be performed')
    args = my_parser.parse_args()

    return args


def main():
    f_article = "articles"
    f_extracted= "extracted"
    args = parse_arguments()

    if args.scrape:
        articles = get_site_text(args.date, args.days)
        store_pickle(articles, f_article)

    articles = load_pickle(f_article)
    extracted = []
    for art in articles:
        sentences = []
        starts = []
        print(art[0])
        extract_stats(art[1], sentences, starts)
        text = filter_out_upper(sentences)
        extracted.append((art[0], text))

    store_pickle(extracted, f_extracted)

    # extracted = load_pickle(f_extracted)


if __name__ == '__main__':
    main()

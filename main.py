import argparse

from scraper import get_site_text
from extractor import extract_sentences, get_filtered_articles
from helpers import (
    save_pickle, 
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
    f_final = "final"
    args = parse_arguments()

    # scrape end store NBA recaps
    if args.scrape:
        articles = get_site_text(args.date, args.days)
        save_pickle(articles, f_article)

    # load scraped articles
    articles = load_pickle(f_article)
    extracted = []
    for art in articles:
        sentences = []
        starts = []
        print(art[0])
        extract_sentences(art[1], sentences, starts)
        text = filter_out_upper(sentences)
        extracted.append((art[0], text))
    # save extracted text to a pickle file
    save_pickle(extracted, f_extracted)

    extracted = load_pickle(f_extracted)

    filtered = get_filtered_articles(extracted)




if __name__ == '__main__':
    main()

import argparse

from scraper import get_site_text
from extractor import get_filtered_articles, get_streaks, get_records
from helpers import (
    save_pickle, 
    load_pickle,
    filter_out_upper,
    dump_json
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
    f_filtered= "filtered"
    f_final = "final.json"
    args = parse_arguments()

    # scrape end store NBA recaps
    if args.scrape:
        articles = get_site_text(args.date, args.days)
        save_pickle(articles, f_article)

    # load scraped articles
    articles = load_pickle(f_article)
    filtered = []
    for art in articles:
        starts = []
        print(art[0])
        records = get_records(art[1], starts)
        streaks = get_streaks(art[1], starts)
        # cleaning headers like TIP-INS
        records = filter_out_upper(records)
        streaks = filter_out_upper(streaks)
        filtered.append((art[0], streaks, records))
    # save filtered text to a pickle file
    save_pickle(filtered, f_filtered)

    filtered = load_pickle(f_filtered)

    extracted = get_filtered_articles(filtered)
    finals = []
    for art in extracted:
        final = dict()
        final['score'] = art[0]
        final['rec'] = art[2]
        final['streaks'] = art[1]
        finals.append(final)

    dump_json(finals, f_final)


if __name__ == '__main__':
    main()

import os
import argparse
import pickle

from scraper import get_site_text


def parse_arguments():
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('--date', type=str, help='ending date in format "YYYYMMDD"')
    my_parser.add_argument('--days', type=int, help='last x days to scrape. Max 7')
    args = my_parser.parse_args()

    return args


def store_articles(articles):
    with open('pickle_files/articles', 'ab') as f:
        pickle.dump(articles, f)


def load_articles():
    with open('pickle_files/articles', 'rb') as f:
        articles = pickle.load(f)
    return articles

def get_articles_from_www(args):
    store_articles(get_site_text(args.date, args.days))

    articles = load_articles()
    print("from pickle", len(articles))
    
    # dbfile.close()
    # sentences = []
    # for article in articles:
    #     starts = []
    #     print(" - " *20)
    #     print(article[0])


def main():
    args = parse_arguments()
    get_articles_from_www(args)





if __name__ == '__main__':
    main()

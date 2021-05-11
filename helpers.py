import pickle


def store_articles(articles):
    with open('pickle_files/articles', 'ab') as f:
        pickle.dump(articles, f)


def load_articles():
    with open('pickle_files/articles', 'rb') as f:
        articles = pickle.load(f)
    return articles
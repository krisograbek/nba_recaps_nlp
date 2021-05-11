import requests

import datetime as dt
from datetime import timedelta
from bs4 import BeautifulSoup


def get_games_info(date, days):
    # convert to datetime
    games_date = dt.datetime.strptime(date, "%Y%m%d")
    games_info = []
    if games_date > dt.datetime.now():
        print("Date must be in the past. Ending...")
        return games_info
    # create a list of last x days
    dates = [games_date - dt.timedelta(days=x) for x in range(days)]
    date_strs = [date.strftime("%Y%m%d") for date in dates]
    print(date_strs)
    for game_dt in dates:
        # convert date to format like Wednesday, March 3
        games_date_str = game_dt.strftime("%A, %B %#d")
        print(games_date_str)
        # find container
        schedule_url = "https://www.espn.com/nba/schedule/_/date/"
        games_urls = []
        # url to scrape
        url = schedule_url + game_dt.strftime("%Y%m%d")
        # get content
        req = requests.get(url)
        soup = BeautifulSoup(req.text, "html.parser")
        container = soup.find("div", id="sched-container")
        first_header = container.find("h2")
        first_header_txt = first_header.get_text()
        table_container = first_header.next_sibling
        if table_container.next_sibling.name == 'div':
            table_container = table_container.next_sibling
            print("Went for the next container")
        # print(table_container.next_sibling.name)
        if first_header_txt != games_date_str:
            print("Something went wrong")
            return
        if table_container.get_text() == "No games scheduled":
            print("No games scheduled on this day")
            return games_info
        # TODO: explain, why you're throwing the first one away
        # first one is a header
        rows = table_container.find_all("tr")[1:]
        # We get the cell that we need
        # TODO: Maybe go deeper when explaining

        for row in rows:
            score_cell = row.find_all("td")[2]
            game_score = score_cell.get_text()
            game_url = score_cell.a['href'].replace("game", "recap", 1)
            print(game_url)
            games_info.append((game_score, game_url))

    return games_info


def get_site_text(date, days):
    if not days:
        days = 7
    if not date:
        yesterday = dt.date.today() - timedelta(days=1)
        date = yesterday.strftime("%Y%m%d")
    if days > 7:
        print("Too many days... Reducing to 7")
        days = 7
    url_base = "https://www.espn.com"
    articles = []
    games_info = get_games_info(date, days)
    for info in games_info:
        print("Scraping; ", info[1])
        req = requests.get(url_base + info[1])
        soup = BeautifulSoup(req.text, "html.parser")

        try:
            # Finding the main title tag.
            art_div = soup.find("div", class_ = "article-body")
            paras = art_div.find_all("p")
            # get article text from paragraphs
            articles.append((info[0], " ".join([p.get_text() for p in paras])))
        # sometimes a game recap is not provided. 
        # In that case atr_div is a NoneType and has no find_all() attribute
        except AttributeError as e:
            print("No game recap")

    print("Articles len: ", len(articles))

    return articles
    
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
***
***
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** github_username, repo_name, twitter_handle, email, project_title, project_description
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->


<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Game recaps are articles containing highlights of the game. 
They provide a lot of interesting information. 
However, they are long and reading everything for every game is very time consuming.

The purpose of this project was to extract most important information from NBA games' recaps.
Most important information include any kind of records or streaks. 
E.g. any kind of season/career best performances, or winning/losing streaks, or games missed due injuries.

First step is scraping articles and getting their text along with scores.
Then Information Extraction is performed on the articles' text. 
They get filtered only to sentences containing any kind of records or streaks.
Record sentences stay as they are. Streak sentences get even more limited.
E.g. Sentence "Rudy Gobert added 15 points and 20 rebounds for the Jazz, who lost their second straight game." 
-> "the Jazz lost their second straight game"


### Built With

* [spacy](https://spacy.io/)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

We assume you have Python version > 3.5 installed on your computer

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/krisograbek/nba_recaps_nlp.git
   ```
2. Install packages
   ```sh
   pip install -r requirements.txt
   ```
3. Install language model
   ```sh
   python -m spacy download en_core_web_sm
   ```
  See [spacy documentation](https://spacy.io/usage) for more info about different language models


<!-- USAGE EXAMPLES -->
## Usage

1. By default, the program scrapes NBA recaps from ESPN's website from yesterday's games

   Basic usage
   ```sh
   py main.py --scrape
   ```

2. In order to scrape games from many days add `--days` and a number (max 10 days)

   Customizing number of days
   ```sh
   py main.py --scrape --days <1-10>
   ```

3. `--date` argument is the most recent day, from which we want to get games. It has `YYYYMMDD` format.

   Customizing the most recent day
   ```sh
   py main.py --scrape --date <YYYYMMDD>
   ```

4. Example

   ```sh
   py main.py --scrape --date 20210512 --days 4
   ```
   In this example, 12 May 2021 is the most previous day, and we want 4 days in total.
   This means games from 9th, 10th, 11th and 12th May 2021 will be extracted.


<!-- LICENSE -->
## License

Distributed under the MIT License. See [License File](https://github.com/krisograbek/nba_recaps_nlp/blob/main/LICENSE.md) for more information.


<!-- CONTACT -->
## Contact

Project Link: [This repo](https://github.com/krisograbek/nba_recaps_nlp.git)
LinkedIn: [Profile](https://www.linkedin.com/in/kris-ograbek-nlp/)


<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* This README file is bootstrapped from - [Template](https://github.com/othneildrew/Best-README-Template/blob/master/BLANK_README.md#built-with)

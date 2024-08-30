# TweetGen
## Description
A GUI application that scrapes a given Twitter username's last 50 tweets and then allows the user to cycle between them in a random order.

## Installation
In order to use this program we need the [ntscraper](https://github.com/bocchilorenzo/ntscraper) library.

To install ntscraper:
```
pip install ntscraper
```
## How to use
to run this program you have to clone this repository to your local machine using:
```
git clone https://github.com/arshjameel/TweetGen.git
cd TweetGen
```
Then:
```
python .\tweetgen.py
```

## Notes
* This project uses the ntscraper library to fetch tweets from various [Nitter](https://github.com/zedeus/nitter?tab=readme-ov-file) instances, which are used as an alternative Twitter frontend.
* Some Nitter instances may not work properly due to recent changes in Twitter's [Terms of Service](https://x.com/en/tos). If a given username's tweets do not load, you can try to fetch tweets again.
* Moreover, due to the previously mentioned updated Twitter ToS policies, it is strictly recommended to treat this project in an academic manner, and not to misuse the code in any way. This ensures that you, or any remaining Nitter instances, do not get banned.

import feedparser
import time

from utils import config, database, helpers, reddit

CONFIG = config.load_config()
REDDIT = reddit.initialize_reddit(CONFIG)
CONNECTION = database.connect_to_db()

FEED_URL = "https://feeds.simplecast.com/54nAGcIl"

def post(article_data):
    subreddit_name = 'Thedaily'

    subreddit = REDDIT.subreddit(subreddit_name)
    if not subreddit.user_is_moderator:
        print(f"You must be a mod in r/{subreddit_name} to run this script.")
        exit()

    print(f"Posting to r/{subreddit_name}...")

    title = article_data['title']
    body = helpers.generate_post_text(article_data)

    subreddit.submit(
        title=title,
        selftext=body
    )

def main():
    feed_data = feedparser.parse(FEED_URL)

    latest_article = feed_data['entries'][0]

    article_data = helpers.retrieve_article_data(latest_article)

    if not helpers.is_article_new(CONNECTION, article_data):
        print("No new article at the moment.")
        time.sleep(4)
        exit()

    post(article_data)

    database.update_article(CONNECTION, article_data)

    print("New article has been posted.")

    database.close_connection(CONNECTION)

if __name__ == '__main__':
    main()
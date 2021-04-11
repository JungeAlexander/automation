import datetime
import logging
from os import environ
import time

from dotenv import load_dotenv
import tweepy
import typer


load_dotenv()

user_name = environ.get("TWITTER_USER_NAME")
api_key = environ.get("TWITTER_API_KEY")
api_secret = environ.get("TWITTER_API_SECRET")
access_token = environ.get("TWITTER_ACCESS_TOKEN")
access_secret = environ.get("TWITTER_ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(
    auth,
    wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True,
    retry_count=3,
    retry_delay=5,
    retry_errors=set([401, 404, 500, 503]),
)


def main(min_favorite_count: int = 3, max_age_days: int = 730, debug: bool = False):
    """
    Delete tweets that are:

    * favorited by fewer than min_favorite_count

    * older than max_age_days

    * not favorited by myself
    """
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    current_date = datetime.datetime.now()
    # Iterate over tweets
    kept = 0
    deleted = 0
    for status in tweepy.Cursor(api.user_timeline, screen_name="@" + user_name).items():
        time.sleep(5)
        id_ = status._json["id"]
        favorite_count = status._json["favorite_count"]
        favorited = status._json["favorited"]
        date = datetime.datetime.strptime(
            status._json["created_at"], "%a %b %d %H:%M:%S +0000 %Y"
        )
        age_days = (current_date - date).days
        if (
            favorite_count < min_favorite_count
            and age_days > max_age_days
            and not favorited
        ):
            logging.debug(f"Delete: {id_}")
            api.destroy_status(id_)
            deleted += 1
        else:
            logging.debug(f"Keep: {id_}")
            kept += 1
    logging.info(f"Kept: {kept}")
    logging.info(f"Deleted: {deleted}")


if __name__ == "__main__":
    typer.run(main)
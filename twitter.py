import datetime
from os import environ

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


def main(min_favorite_count: int = 3, max_age_days: int = 100):
    """
    Delete tweets that are:
    
    * favorited by fewer than min_favorite_count

    * older than max_age_days
    
    * not favorited by myself
    """
    current_date = datetime.datetime.now()
    # Iterate over tweets
    for status in tweepy.Cursor(api.user_timeline, screen_name="@" + user_name).items():
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
            print(id_)
            # api.destroy_status(id_)


if __name__ == "__main__":
    typer.run(main)
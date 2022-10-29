import json
import time
import unicodedata

import tweepy

auth = tweepy.OAuth1UserHandler(
    "CAEKNwKWoXI4nsOnyq4nJDC9e",
    "2ahuvdTDFAR9d7hku66YYhOONWvyMfD72OHlD1I5n5L0tlDIWG",
    "1296746024237555713-ND1AkemLqW5KGvXhY4OIJWkcdl8h9y",
    "n0Tjneth7aELYA8rSRIThgagSXwJW2kVihp13kPmtNO2W",
)

# calling an api
api = tweepy.API(auth)
public_tweets = api.user_timeline(screen_name="@fabrizioRomano", tweet_mode="extended")

# function to extract user tweets details
def get_tweets(check: bool) -> list[dict]:
    """
    Extracting the tweets for a particular user
    Args:
        check(bool): checks for the updated tweets of a user
    Returns:
        tweet_list(list[dict]): List of tweets
    """
    tweet_list: list[dict] = []
    for _tweet in public_tweets:
        tweet: dict = {}
        tweet["author"] = str(_tweet.author.name)
        tweet["content"] = str(
            unicodedata.normalize("NFKD", _tweet.full_text).encode("ascii", "ignore")
        )
        tweet["tweet_time"] = _tweet.created_at.strftime("%d/%m/%Y , %H:%M:%S")
        tweet["tweet_id"] = _tweet.id
        tweet["no_of_likes"] = _tweet.favorite_count
        tweet["no_of_retweets"] = _tweet.retweet_count
        tweet_list.append(tweet)
        if check == True:
            break

    return tweet_list


# function to write tweets in json
def write_to_json(tweet_list):
    """
    Stores the data in the json file
    Args:
        tweet_list(list[dict]): List of tweets
    Returns:
        None
    """
    tweets: dict = {"tweets": tweet_list}
    json_object = json.dumps(tweets, indent=2)
    with open("data.json", "w") as outfile:
        outfile.write(json_object)


if __name__ == "__main__":
    tweet_list: list[dict] = get_tweets(False)
    write_to_json(tweet_list)

    tweets: dict = {"tweets": tweet_list}
    json_object: dict = json.dumps(tweets, indent=2)
    print(json_object)
    print("Tweets written to data.json")
    last_tweet_id = tweet_list[0]["tweet_id"]
    time.sleep(60)

    while 1:
        new_tweet = get_tweets(True)

        if new_tweet[0]["tweet_id"] != last_tweet_id:
            print("New Tweets Found")
            tweet_list = get_tweets(False)
            for _tweet in tweet_list:
                print(json.dumps(_tweet, indent=2))
                if _tweet["tweet_id"] == last_tweet_id:
                    break
            write_to_json(tweet_list)
            print("New tweets written to data.json")
            time.sleep(60)

        else:
            print("No new Tweets found")
            time.sleep(60)

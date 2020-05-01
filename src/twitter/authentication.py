import tweepy


def authenticate_1(consumer_key, consumer_secret, token_key, token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(token_key, token_secret)
    return auth


def authenticate_2(consumer_key, consumer_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    return auth

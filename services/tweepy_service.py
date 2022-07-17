import logging
import tweepy
import os

try:
    from dotenv import load_dotenv
    load_dotenv(override=False)
except:
    pass

logging.basicConfig(filename='tweepy_logs.log', format='%(asctime)s(%(levelname)s): %(message)s', level=logging.INFO)

class Tweepy:
    def __init__(self):
        __consumer_key = os.getenv('API_KEY')
        __consumer_secret = os.getenv('API_KEY_SECRET')
        __access_token = os.getenv('ACCESS_TOKEN')
        __access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
        __bearer_token = os.getenv('BEARER_TOKEN')
        
        self.client = tweepy.Client(
            bearer_token = __bearer_token, 
            consumer_key = __consumer_key, 
            consumer_secret = __consumer_secret, 
            access_token = __access_token, 
            access_token_secret = __access_token_secret
        )
    
    def search_like_tweet(self, query, transformer):
        tweets = self.client.search_recent_tweets(query=query, max_results=10)

        for index, tweet in enumerate(tweets.data):
            try:
                paraphrased_tweet = transformer.get_paraphrased_tweets(tweet.text, num_return_sequences=1)
                self.client.like(tweet.id)
                content = paraphrased_tweet[0] + ' #tweet_from_tweepy_bot'
                response = self.client.create_tweet(text=content, quote_tweet_id=tweet.id)
                if response.data['id'] and len(response.errors)==0: logging.info(f'{self.__class__.__name__} - {index+1} Posted a quoted tweet:\n{paraphrased_tweet[0]}')
            except Exception as error:
                logging.error(f'{self.__class__.__name__} - {index+1} {error}')

if __name__ == '__main__':
    client = Tweepy().client
    
    # tweepy will search for tweets that has either one of the hashtags in the parentheses that are written in english and NOT retweet
    query = '#AWS lang:en -is:retweet'
    tweets = client.search_recent_tweets(query=query, max_results=10)
    
    if tweets.data is not None:
        print(f'Total tweets found: {len(tweets.data)}')
        for tweet in tweets.data:
            client.like(tweet.id)
            response = client.retweet(tweet.id)
            print(response)

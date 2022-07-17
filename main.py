from services.tweepy_service import Tweepy
from services.transformer_service import Pegasus_Transformer
from services.joke_service import Joker
import logging

logging.basicConfig(filename='tweepy_logs.log', format='%(asctime)s(%(levelname)s): %(message)s', level=logging.INFO)

def main():
    logging.info('Tweepy started!')
    try:
        tweepy = Tweepy()
        transformer = Pegasus_Transformer()
        query = '(#AI OR #AWS) lang:en -is:retweet'
        logging.info('Main - 1 of 2: Retweeting!')
        tweepy.search_like_tweet(query, transformer)
    
        logging.info('Main - 2 of 2: Tweeting jokes!')
        joker = Joker()
        joker.tweet_jokes(tweepy.client)
    except Exception as error:
        logging.error(f'Main - {error}')

if __name__ == '__main__': main()

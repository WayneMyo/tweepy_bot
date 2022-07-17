import requests
import logging
import os

try:
    from dotenv import load_dotenv
    load_dotenv(override=False)
except:
    pass

logging.basicConfig(filename='tweepy_logs.log', format='%(asctime)s(%(levelname)s): %(message)s', level=logging.INFO)

class Joker:
    def __init__(self):
        self.joke_api = os.getenv('JOKE_API')

    def get_random_joke(self):
        try:
            response = requests.get(self.joke_api)
            if response.status_code != 200: return
            data = response.json()[0]
            return data['question'] + '\n' + data['punchline'] + ' source - ' + self.joke_api
        except Exception as error:
            logging.error(f'{self.__class__.__name__} - {error}')

    def tweet_jokes(self, tweepy_client):
        for index in range(10):
            try:
                joke = self.get_random_joke()
                if joke is None: continue

                content = joke + ' #tweet_from_tweepy_bot'
                response = tweepy_client.create_tweet(text=content)
                if response.data['id'] and len(response.errors)==0: logging.info(f'{index+1} - Posted a joke:\n{joke}')
            except Exception as error:
                logging.error(f'{self.__class__.__name__} - {index+1} {error}')

if __name__ == '__main__':
    joker = Joker()
    joke = joker.get_random_joke()
    print(joke)

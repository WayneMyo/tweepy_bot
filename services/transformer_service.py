from transformers import PegasusForConditionalGeneration, PegasusTokenizerFast
import tensorflow as tf
import logging
import pickle
import os

try:
    from dotenv import load_dotenv
    load_dotenv(override=False)
except:
    pass

logging.basicConfig(filename='tweepy_logs.log', format='%(asctime)s(%(levelname)s): %(message)s', level=logging.INFO)

class Pegasus_Transformer:
    def __init__(self):
        tf.random.set_seed(0)
        self.pickle_dir = os.getenv('PICKLE_DIR')
        self.model_file_name = 'pegasus_model.pkl'
        self.tokenizer_file_name = 'pegasus_tokenizer.pkl'

        # use pickled model if available
        try:
            __pickled_model = pickle.load(open(self.pickle_dir + self.model_file_name, 'rb'))
            __pickled_tokenizer = pickle.load(open(self.pickle_dir + self.tokenizer_file_name, 'rb'))
            self.model = __pickled_model
            self.tokenizer = __pickled_tokenizer
            logging.info(f'{self.__class__.__name__} - Using pickled models.')
        except OSError as error:
            self.model = PegasusForConditionalGeneration.from_pretrained('tuner007/pegasus_paraphrase')
            self.tokenizer = PegasusTokenizerFast.from_pretrained('tuner007/pegasus_paraphrase')

            pickle.dump(self.model, open(self.pickle_dir + self.model_file_name, 'wb'))
            pickle.dump(self.tokenizer, open(self.pickle_dir + self.tokenizer_file_name, 'wb'))
            logging.info(f'{self.__class__.__name__} - {error}')
            logging.info(f'{self.__class__.__name__} - Pickled models not found. Generating from fresh and save to pickle.')

    def get_paraphrased_tweets(self, tweet, num_return_sequences=3):
        input_tokens = self.tokenizer([tweet], truncation=True, padding='longest', return_tensors='pt') # tokenize the tweet to be form of a list of token IDs

        # generate the paraphrased tweets
        outputs = self.model.generate(
            **input_tokens,
            do_sample=True, 
            top_k=50, 
            top_p=0.95,
            max_length=250, # twitter character limit is 280
            num_return_sequences=num_return_sequences
        )
        # decode the generated tweets using the tokenizer to get them back to text
        return self.tokenizer.batch_decode(outputs, skip_special_tokens=True)

if __name__ == '__main__':
    sentence = 'Customer Obsession - Leaders start with the customer and work backwards, they work vigorously to earn and keep customer trust. Although leaders pay attention to competitors, they obsess over customers.'
    transformer = Pegasus_Transformer()
    paraphrased_sentences = transformer.get_paraphrased_tweets(sentence, num_return_sequences=5)
    print(paraphrased_sentences)

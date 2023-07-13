import os
import tweepy
import logging
import openai
from dotenv import load_dotenv
load_dotenv()
consumer_key = os.getenv('API_K')
consumer_secret_key = os.getenv('API_S')
access_token = os.getenv('ACCESS_T')
access_token_secret = os.getenv('ACCESS_S')
bearer_token = os.getenv('TOKEN')
client = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key,
                       consumer_secret=consumer_secret_key, access_token=access_token,
                       access_token_secret=access_token_secret, return_type=dict)
bot =None
try:
    bot_id = os.getenv('ACCOUNT_ID')
    print("Authentication Successful")
except Exception as e:
    print(e)
    print("Authentication Error")

# For adding logs in application
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)

#function for generating reply from Chatgpt
def get_quote(text):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": text}], temperature=0, max_tokens=200)
    quote = response['choices'][0]['message']['content']
    quote = quote.strip()
    print("Dasdadasda", quote[:250])
    return quote[:250]
#function for getting last replied account id
def get_last_tweet(file):
    f = open(file, 'r')
    lastId = int(f.read().strip())
    f.close()
    return lastId
#function for writing the last replied account id
def put_last_tweet(file, Id):
    f = open(file, 'w')
    f.write(str(Id))
    f.close()
    logger.info("Updated the file with the latest tweet Id")
    return 

def respondToTweet(file='tweets.txt'):
    last_id=None
    try: 
        last_id = get_last_tweet(file)
    except:
        pass
    mentions = client.get_users_mentions(id=bot_id, since_id=last_id, expansions=['author_id', 'referenced_tweets.id'])
    if not mentions.get('data'):
        return
    new_id = 0
    logger.info("someone mentioned me...")
    for mention, user, tweet in zip(mentions['data'], mentions['includes']['users'], mentions['includes']['tweets']):
        logger.info(str(mention['id']) + '-' + tweet['text'])
        new_id = mention['id']
        try:
            logger.info("replying to tweet")
            quote = get_quote(tweet['text'])
            username = user['username']
            client.create_tweet(in_reply_to_tweet_id=mention['id'], text=f"@{username} {quote}") #for posting reply to mentioned id
            print("reply done")
        except Exception as e:
            print(e)
            logger.info("Already replied to {}".format(mention["id"]))
    put_last_tweet(file, new_id)

if __name__=="__main__":
    respondToTweet()



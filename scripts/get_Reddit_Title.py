import praw
import configparser
# from utils import redis_connection
import sys
from datetime import date,datetime
sys.path.append('/home/awpeng/DataScience_Reddit_Analysis')
from utils.redis_util import redis_connection
from utils.mongoDB_util import mongodb_connection
import logging

path_to_settings = '/home/awpeng/DataScience_Reddit_Analysis/secrets.ini'

# read configuration from settings
Configs = configparser.ConfigParser()

Configs.read(path_to_settings)

# reddit related variable

reddit_userid = Configs['reddit_cred']['client_id'] 
reddit_secret = Configs['reddit_cred']['client_secret']
reddit_useragent = "lubongivan"
reddit_topic = "datascience"
reddit_thread_limit = 10
mongo_username = Configs['MongoDB']['user_name']
mongo_pwd = Configs['MongoDB']['pwd']
mongo_conn_str = f"mongodb+srv://{mongo_username}:{mongo_pwd}@cluster0.pfuwrvp.mongodb.net/?retryWrites=true&w=majority"

def upload_redditPost(reddit_userid: str, reddit_secret: str, reddit_useragent: str, reddit_topic: str, num_of_threads: str, redis_conn, mongodb_url, mongo_dbname, mongo_collection_name):
    """
    Description: extract reddit posts, deduplicats posts and upload to mongoDB
    reddit_userid: string, your reddit id
    redis_conn: stable redis connection client
    """
    
    # connect to reddit
    reddit = praw.Reddit(
        client_id=reddit_userid,
        client_secret=reddit_secret,
        user_agent=reddit_useragent,
    )
    
    # rc = redis_connection(redis_host=redis_host, redis_port=redis_port, redis_db_num=redis_db_num)

    # go into redis and grab existing reddit post ids
    logging.info("Starting grabbing uniques ids from redis...")
    all_keys_list = redis_conn.get_all_members("all_ids")
    print(all_keys_list)
    logging.info(f"Process complted, grabbed {len(all_keys_list)} from redis")
    logging.info("---" * 20)

    post_title = []
    # iterate and print out hot reddit topics
    for submission in reddit.subreddit(reddit_topic).hot(limit=num_of_threads):
        #check if post id existed, if existed, do not add to redis, if not add to redis
        if submission.id not in all_keys_list:
            redis_conn.add_members("all_ids", submission.id)
            post_title.append(submission.title)
    
    # save to mongodb
    submission_doc = {
        "TimeStamp": str(date.today()),
        "subreddit": reddit_topic,
        "Titles": post_title
    }

    print(submission_doc)

    mc = mongodb_connection(url=mongodb_url, db_name=mongo_dbname, collection_name=mongo_collection_name)
    mc.add_documents(submission_doc)

    # return reddit.subreddit(reddit_topic).hot(limit=num_of_threads)
    return

# logic, get id for the reddit post, check if id already existed in redis, if existed, do not add, else we can add

def run_get_reddit_title():
    redis_db_num = 7
    redis_host = 'localhost'
    redis_port = 6379
    db_name = "Reddit_Post"
    collection_name = "RedditPost_DS"
    rc = redis_connection(redis_host=redis_host, redis_port=redis_port, redis_db_num=redis_db_num)
    upload_redditPost(reddit_userid, reddit_secret, reddit_useragent, reddit_topic, reddit_thread_limit, rc, mongo_conn_str, db_name, collection_name)
    

if __name__ == "__main__":
    run_get_reddit_title()
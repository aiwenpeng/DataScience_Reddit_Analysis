import praw
import configparser
# from utils import redis_connection
import sys
sys.path.append('/home/awpeng/DataScience_Reddit_Analysis')
from utils.redis_util import redis_connection

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

def upload_redditPost(reddit_userid: str, reddit_secret: str, reddit_useragent: str, reddit_topic: str, num_of_threads: str, redis_conn):
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
    
    rc = redis_connection(redis_host=redis_host, redis_port=redis_port, redis_db_num=redis_db_num)

    # go into redis and grab existing reddit post ids
    all_keys_list = redis_conn.get_all_members("all_ids")
    print(all_keys_list)

    # iterate and print out hot reddit topics
    for submission in reddit.subreddit(reddit_topic).hot(limit=num_of_threads):
        #check if post id existed, if existed, do not add to redis, if not add to redis
        # if submission.id not in all_keys_list:
        #     rc.add_members(submission.id)
            #save to mongodb
        print(submission.title)

    # return reddit.subreddit(reddit_topic).hot(limit=num_of_threads)
    return

# logic, get id for the reddit post, check if id already existed in redis, if existed, do not add, else we can add

if __name__ == "__main__":
    redis_db_num = 7
    redis_host = 'localhost'
    redis_port = 6379
    rc = redis_connection(redis_host=redis_host, redis_port=redis_port, redis_db_num=redis_db_num)
    upload_redditPost(reddit_userid, reddit_secret, reddit_useragent, reddit_topic, 20, rc)
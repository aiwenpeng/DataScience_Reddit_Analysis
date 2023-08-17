import praw
import configparser

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

def upload_redditPost(reddit_userid: str, reddit_secret: str, reddit_useragent: str, reddit_topic: str, num_of_threads: str) -> None:
    """
    Description: extract reddit posts, deduplicats posts and upload to mongoDB
    reddit_userid: string, your reddit id
    """
    
    # connect to reddit
    reddit = praw.Reddit(
        client_id=reddit_userid,
        client_secret=reddit_secret,
        user_agent=reddit_useragent,
    )

    # iterate and print out hot reddit topics
    for submission in reddit.subreddit(reddit_topic).hot(limit=num_of_threads):
        # save to db
        print(submission.title, submission.id)

# logic, get id for the reddit post, check if id already existed in redis, if existed, do not add, else we can add

if __name__ == "__main__":
    upload_redditPost(reddit_userid, reddit_secret, reddit_useragent, reddit_topic, reddit_thread_limit)
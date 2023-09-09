import redis
import logging
from datetime import datetime

LOG_FILENAME = datetime.now().strftime('/home/awpeng/log/getRedisLog_%H_%M_%S_%d_%m_%Y.log')
for handler in logging.root.handlers[:]:
      logging.root.removeHandler(handler)
logging.basicConfig(filename=LOG_FILENAME, filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
datetime.now().strftime('mylogfile_%H_%M_%d_%m_%Y.log')
logger=logging.getLogger(__name__)

class redis_connection():
    """
    """

    def __init__(self, redis_host, redis_port, redis_db_num) -> None:
        # initailize all connection paramters
        self.db_num = redis_db_num
        self.host = redis_host
        self.port = redis_port

        # try to connect to redis using paramters
        try:
            self.redis_client = redis.Redis(host=self.host, port=self.port, decode_responses=True, db=self.db_num)
            self.redis_client.ping()
        except Exception as e:
            print(f"{e}")
            logger.error(e)
            logging.info("error connect to redis")
    
    def add_members(self, key, value):
        """
        description: adds member to a Redis set using sadd command
        key: set to hold values
        value: string
        return: Redis set
        """
        # if method == "set":
        #     sadd
        # elif method  == "string":
        #     set
        # elif method == "list":


        try:

            self.redis_client.sadd(key, value)
        except Exception as e:
            print(e)
            logger.error(e)
            logging.info("error add member in redis")
    
    def get_all_members(self, key):
        """
        description: retrieves all members of a Redis set using the smembers command
        key: set to get members
        return: a set of all members retrieved
        """
        try:
            all_members = self.redis_client.smembers(key)
        except Exception as e:
            print(e)
            logger.error(e)
            logging.info("error get all members")
        
        return [mem for mem in all_members] # optimize point: change list to set, because it consumes less memory
    
    def delete_members(self, key, remove_entire_set = True, element_to_remove = []):
        """
        description:delete members of a Redis set using the delete command. If remove_entire_set is True, the entire set is deleted using the delete command. If remove_entire_set is False, specific elements are removed using the srem command.
        key: set to get members
        remove_entire_set: If required to remove the entire set
        element_to_remove: If required to remove specific elements
        return: whether members are deleted
        """
        logger.info("Starting deleting ", "entire set " if remove_entire_set else f"elements ", f"from redis {key}")
        try:
            1/0
            if remove_entire_set:
                delete_members = self.redis_client.delete(key)
                print("Deleted:", "success" if delete_members == 1 else "failed")
            else:
                num_removed = self.redis_client.srem(key, *element_to_remove)
                print("Removed:", num_removed)
                logger.info(f"Dropping element successful, removed {num_removed} elements")
        except Exception as e:
            print(e)
            logger.error(e)
            logging.info("error delete members")




if __name__ == "__main__":
    redis_db_num = 0
    redis_host = 'localhost'
    redis_port = 6379
    rc = redis_connection(redis_host=redis_host, redis_port=redis_port, redis_db_num=redis_db_num)
    # rc.add_members("class:b", "name:haha")
    # print(rc.get_all_members("class:b"))
    # myset = rc.redis_client.set('foo', 'bar')
    # rc.redis_client.sadd('all_ids', 111,2,3)
    # print(rc.redis_client.get('foo'))
    rc.delete_members("hello-1")
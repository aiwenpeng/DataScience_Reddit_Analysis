import redis

class redis_connection():

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
    
    def add_members(self, key, value):
        """
        """
        try:
            self.redis_client.sadd(key, value)
        except Exception as e:
            print(e)
    
    def get_all_members(self, key):
        try:
            all_members = self.redis_client.smembers(key)
        except Exception as e:
            print(e)
        
        return [mem for mem in all_members]


if __name__ == "__main__":
    redis_db_num = 0
    redis_host = 'localhost'
    redis_port = 6379
    rc = redis_connection(redis_host=redis_host, redis_port=redis_port, redis_db_num=redis_db_num)
    rc.add_members("class:b", "name:haha")
    print(rc.get_all_members("class:b"))
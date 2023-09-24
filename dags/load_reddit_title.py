# python
# 
import sys
import pendulum, datetime

sys.path.append('/home/awpeng/DataScience_Reddit_Analysis')
from scripts.get_Reddit_Title import run_get_reddit_title
from utils.mongoDB_util import check_mongo_conn
from utils.redis_util import check_redis_conn

from airflow import DAG
from airflow.operators.python import PythonOperator

def say_hello():
    print("Hello!")

# set up common paramters for the DAG
with DAG(
    dag_id="Load_Reddit_Thread",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2023, 9, 23, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
    tags=["data_load", "mongodb"],
) as dag:
    
    check_redis_connection = PythonOperator(
        task_id="check_redis_conn",
        python_callable=check_redis_conn,
        
    )

    check_mongoDB_connection = PythonOperator(
        task_id="check_mongodb_conn",
        python_callable=check_mongo_conn
        
    )

    # Define dag tasks
    load_to_mongodb = PythonOperator(
        task_id="load_to_mongo",
        python_callable=run_get_reddit_title,
        
    )

# build dag dependencies with tasks
[check_redis_connection, check_mongoDB_connection] >> load_to_mongodb
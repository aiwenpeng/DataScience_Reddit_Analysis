# DataScience_Reddit_Analysis

## Project Overview
This project goes through Reddit posts about datascience, finds the sentiment of the data science market


## Project Steps
Get Reddit post  

Data validation
- check post duplication

Upload data to mongoDB

Schedule tasks with Airflow 

## Data Source
Reddit-subreddit: [datascience](https://www.reddit.com/r/datascience/)

## How to Run:
#### Virtual Enviroment
Set up a virtualenv that contains all the packages we needed to run our pipeline
This will make sure our pipeline can run stable without any issues

Python3.10 [version of python] -m venv <virtual env name>  
To activate: source <path to virtual env>/bin/activate  
To deactivate: deactivate

#### Setup Configuration
```
pip install praw
python3 DataScience_Reddit_Analysis/scripts/get_Reddit_Title.py
```
#### Redis
caching post id from Reddit in Redis 

#### MongoDB


#### Airflow
build DAG dependencies with tasks: load data to mongodb only when redis and mongodb connections have been established successfully.  


![image](https://github.com/aiwenpeng/DataScience_Reddit_Analysis/assets/141974047/47cd02f8-7ae4-426f-9501-5564c76eecaa)

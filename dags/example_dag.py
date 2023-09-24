from __future__ import annotations

import datetime

import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="eva_bash_operator",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
    tags=["test"],
    params={"example_key": "example_value"},
) as dag:
    run_this = BashOperator(
        task_id="run_after_loop",
        bash_command="echo 1",
    )

run_this
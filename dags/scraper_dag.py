import datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator


def get_name():
    return "Axel"


def hello(ti):
    name = ti.xcom_pull(task_ids="get_name_task")
    return f"Hello {name}"


def goodbye(ti):
    name = ti.xcom_pull(task_ids="get_name_task")
    return f"Goodbye {name}"


with DAG(
    "hello_world-0.1.1",
    description="Simple tutorial DAG",
    schedule_interval="0 12 * * *",
    start_date=datetime.datetime.now(),
    catchup=False,
) as dag:

    get_name_operator = PythonOperator(task_id="get_name_task", python_callable=get_name)
    hello_operator = PythonOperator(task_id="hello_task", python_callable=hello)
    goodbye_operator = PythonOperator(task_id="goodbye_task", python_callable=goodbye)

    get_name_operator >> hello_operator >> goodbye_operator

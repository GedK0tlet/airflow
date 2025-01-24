from datetime import timedelta, datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable

from scripts.get_jokes_api_ai.getter import get_jokes_api_ai
from scripts.bot_sandler_scripts.bot import send_messages

tokenYaGPT = Variable.get("tokenYaGPT")
tokenTgBot = Variable.get("tokenTgBot")
list_ids = Variable.get("list_ids").split(",")

default_args = {
    'owner': 'Evgenii',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id = 'dag_fetch_new_an_v01',
    default_args = default_args,
    start_date = datetime(2025, 1, 23),
    tags = ['tg_bot_ankdot_fetcher'],
    schedule_interval = timedelta(minutes=5),
) as dag:
    task_fetch_data = PythonOperator(
        task_id = 'task_fetch_data',
        provide_context = True,
        python_callable = get_jokes_api_ai,
        op_kwargs = {'api_key': tokenYaGPT, 'examples': ['Почему собака лижет сибе попу? Потому она покакала.', 'Программист всегда знает сколько времени, Ведь у него есть часы.'], 'theme': ['армян', 'программистов', 'музыкантов', 'бомжей']}
    )

    task_send_anekdot_to_channels = PythonOperator(
        task_id = 'task_send_anekdot_to_channels',
        provide_context = True,
        python_callable = send_messages,
        op_kwargs = {'token': tokenTgBot, 'list_ids': list_ids},
    )

    task_fetch_data >> task_send_anekdot_to_channels
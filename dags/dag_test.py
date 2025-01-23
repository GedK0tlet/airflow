from datetime import timedelta, datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable

from scripts.get_jokes_api_ai.getter import get_jokes_api_ai
from scripts.bot_sandler_scripts.bot import send_messages

tokenYaGPT = Variable.get("tokenYaGPT")
tokenTgBot = Variable.get("tokenTgBot")

default_args = {
    'owner': 'Evgenii',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def take_an(ti):
    an = ti.xcom_pull(task_ids = 'task_fetch_data', key="text_anekdot")
    print(f"\n\n\n\n\n\n\n\n\n\n{an}\n\n\n\n\n\n\n\n\n\n")
    return an

with DAG(
    dag_id = 'dag_fetch_new_an_v01',
    default_args = default_args,
    start_date = datetime(2025, 1, 23),
    tags = ['tg_bot_ankdot_fetcher'],
    schedule_interval = "0 * * * *",
) as dag:
    task_fetch_data = PythonOperator(
        task_id = 'task_fetch_data',
        provide_context = True,
        python_callable = get_jokes_api_ai,
        op_kwargs = {'api_key': tokenYaGPT, 'examples': ['Почему собака лижет сибе попу? Потому она покакала.', 'Программист всегда знает сколько времени, Ведь у него есть часы.'], 'theme': 'армян'}
    )

    task_send_anekdot_to_channels = PythonOperator(
        task_id = 'task_send_anekdot_to_channels',
        provide_context = True,
        python_callable = send_messages,
        op_kwargs = {'token': tokenTgBot, 'list_ids': [-1002311333309,-1002275206963]},
    )

    task_fetch_data >> task_send_anekdot_to_channels
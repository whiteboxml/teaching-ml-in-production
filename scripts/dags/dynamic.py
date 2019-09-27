import random
import airflow
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.email_operator import EmailOperator
from datetime import timedelta

# settings

MAIL_LIST = []  # set your email here!

N_TASKS_LEVEL_1 = 2
N_LEVELS = 3
N_TASKS = 4

DEFAULT_ARGS = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(1),
    'email': MAIL_LIST,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 5,
    'retry_delay': timedelta(minutes=15),
}


# pipeline functions and helpers

def generate_levels(n_tasks, previous_level_tasks, level_start, n_levels):
    if n_levels == 0:
        return previous_level_tasks
    generated_tasks = []

    for task in previous_level_tasks:
        task_id = task.task_id
        for n_task in range(n_tasks):
            task_ln = DummyOperator(task_id=task_id + '_' + f'task_level_{level_start}_{n_task}', dag=dag)
            task >> task_ln
            generated_tasks.append(task_ln)

    return generate_levels(n_tasks=n_tasks,
                           previous_level_tasks=generated_tasks,
                           level_start=level_start + 1,
                           n_levels=n_levels - 1)


# dag definition

dag = DAG('crazy_maze',
          default_args=DEFAULT_ARGS,
          schedule_interval='0 8 * * MON')

# task dynamic definition

start = DummyOperator(task_id='start', dag=dag)
join = DummyOperator(task_id='join', dag=dag)
end = DummyOperator(task_id='end', dag=dag)

task_execution_success_mail = EmailOperator(
    to=MAIL_LIST,
    task_id="mail_execution",
    subject="Airflow - Big Data Master",
    html_content="crazy maze executed successfully!",
    dag=dag)

for n_task in range(N_TASKS_LEVEL_1):
    task_l1 = DummyOperator(task_id=f'task_level_1_{n_task}', dag=dag)
    start >> task_l1
    task_l2 = DummyOperator(task_id=f'task_level_1_{n_task}_level_2_1', dag=dag)
    task_l1 >> task_l2
    task_l2 >> join

    if random.random() > 0.5:
        task_l2_extra = DummyOperator(task_id=f'task_level_1_{n_task}_level_2_2', dag=dag)
        task_l1 >> task_l2_extra
        task_l2_extra >> join

last_level_tasks = generate_levels(n_tasks=N_TASKS,
                                   previous_level_tasks=[join],
                                   level_start=2,
                                   n_levels=N_LEVELS)

for task in last_level_tasks:
    task >> task_execution_success_mail

task_execution_success_mail >> end

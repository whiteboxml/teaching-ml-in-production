import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import timedelta

###############################################################################
# DAG

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

dag = DAG(dag_id='simple_dag',
          schedule_interval='@hourly',
          catchup=False,
          default_args=default_args)

###############################################################################
# TASKS

start = DummyOperator(task_id='start', dag=dag)
end = DummyOperator(task_id='end', dag=dag)

# example task 1

task_1 = BashOperator(
    task_id='task_1',
    bash_command="echo 'executing bash command: cd {{ params.dir }} && ./{{ params.script }}'",
    params={'dir': '/path/to/your/directory/',
            'script': 'script.sh'},
    dag=dag)

# example task 2

task_2_command = """
echo 'executing bash command: cd {{ params.dir }} \
&& sudo -u {{ params.user }} ./{{ params.script }} \
--process={{ params.process }} \
"""

task_2 = BashOperator(
    task_id='task_2',
    bash_command=task_2_command,
    params={'dir': '/path/to/your/directory/',
            'user': 'user',
            'script': 'script.sh',
            'process': 'process_name'},
    dag=dag)

start >> [task_1, task_2] >> end

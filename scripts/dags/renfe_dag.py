import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import timedelta

###############################################################################
# SETTINGS

CENTERS = ['MADRID']
DESTINATIONS = ['BARCELONA', 'SEVILLA', 'VALENCIA', 'GRANADA', 'PONFERRADA']

PYTHON_INTERPRETER_PATH: str = '/path/to/python/interpreter/'
RUN_SCRIPT: str = '/path/to/script.py'

###############################################################################
# DAG

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(dag_id='renfe_production',
          schedule_interval=None,
          catchup=False,
          default_args=default_args)

###############################################################################
# TASKS

start = DummyOperator(task_id='start', dag=dag)
end = DummyOperator(task_id='end', dag=dag)

command = """
{{ params.interpreter_path }} \
{{ params.script_path }} \
-o {{ params.origin }} \
-d {{ params.destination }} \
"""

for c in CENTERS:
    for d in DESTINATIONS:

        task_c_d = BashOperator(
            task_id='alarms' + '_' + c + '_' + d,
            bash_command=command,
            params={
                'interpreter_path': PYTHON_INTERPRETER_PATH,
                'script_path': RUN_SCRIPT,
                'origin': c,
                'destination': d
                    },
            dag=dag,
        )

        task_d_c = BashOperator(
            task_id='alarms' + '_' + d + '_' + c,
            bash_command=command,
            params={
                'interpreter_path': PYTHON_INTERPRETER_PATH,
                'script_path': RUN_SCRIPT,
                'origin': d,
                'destination': c
                    },
            dag=dag,
        )

        start >> task_c_d >> task_d_c >> end

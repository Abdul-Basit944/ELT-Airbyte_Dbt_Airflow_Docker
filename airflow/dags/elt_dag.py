# from datetime import datetime, timedelta
# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from airflow.operators.bash import BashOperator
# from airflow.providers.docker.operators.docker import DockerOperator
# import subprocess
# from airflow.types import Mount


# default_args = {
#     'owner': 'airflow',
#     'depends_on_past': False,
#     'email_on_failure': False,
#     'email_on_retry': False,
# }

# def run_elt_script():
#     script_path = '/opt/airflow/elt/elt_script.py'
#     result = subprocess.run(['python', script_path], capture_output=True, text=True)
#     if result.returncode != 0:
#         raise Exception(f"Script failed with error: {result.stderr}")
#     else:
#      print(result.stdout)

# dag = DAG(
#     'elt_and_dbt',
#     default_args=default_args,
#     description='A simple ELT DAG',
#     schedule_interval=timedelta(days=1),
#     start_date=datetime(2025, 8, 31),
#     catchup=False,
# )

# t1 = PythonOperator(
#     task_id='run_elt_script',
#     python_callable=run_elt_script,
#     dag=dag,
# )

# t2 = DockerOperator(
#     task_id='dbt_run',
#     image='ghcr.io/dbt-labs/dbt-postgres:1.4.7',
#     command=[
#         "run",
#         "profiles-dir",
#         "/root",
#         "--project-dir",
#         "/dbt"
#     ],
#     auto_remove=True,
#     docker_url='unix://var/run/docker.sock',
#     network_mode='bridge',
#     mounts=[
#         Mount(source='/Learning/Airbyte/custom_postgres', target='/dbt', type='bind'),
#         Mount(source='/Learning/Airbyte/.dbt', target='/root', type='bind')
#     ],
#     dag=dag
# )

# t1 >> t2



from datetime import datetime 
from airflow import DAG 
from airflow.providers.docker.operators.docker import DockerOperator 
from airflow.operators.bash import BashOperator 
import subprocess 
from docker.types import Mount

CONN_ID = 'decd338e-5647-4c0b-adf4-da0e75f5a750'   
 
 
default_args = { 
    'owner': 'airflow', 
    'depends_on_past': False, 
    'email_on_failure': False, 
    'email_on_retry': False, 
    'retries': 1, 
} 
 
dag = DAG( 
    'elt_and_dbt', 
    default_args=default_args, 
    description='ELT pipeline with Airbyte and dbt', 
    start_date=datetime(2025, 9, 1), 
    catchup=False, 
) 
 
# Airbyte Cloud ELT task using API
t1 = BashOperator(
    task_id="airbyte_postgres_postgres",
    bash_command=f"""
    # For Airbyte Cloud, you need to use their API with authentication
    # This is a placeholder - you'll need to get your API key from Airbyte Cloud
    echo "Note: Update this with your Airbyte Cloud API key and use their API endpoint"
    echo "Connection ID: {CONN_ID}"
    echo "Simulating successful Airbyte sync for now..."
    """,
    dag=dag,
) 
 
# dbt transformation task 
t2 = DockerOperator( 
    task_id='dbt_run', 
    image='ghcr.io/dbt-labs/dbt-postgres:1.4.7', 
    command=['debug', '--profiles-dir', '/root/.dbt', '--project-dir', '/dbt'],
    auto_remove='success', 
    docker_url='unix://var/run/docker.sock', 
    network_mode='airbyte_elt_network',
    working_dir='/dbt',
    mount_tmp_dir=False,
    mounts=[
        Mount(
            source='E:/Learning/Airbyte/custom_postgres',  
            target='/dbt',
            type='bind'
        ),
        Mount(
            source='E:/Learning/Airbyte/.dbt',
            target='/root/.dbt',
            type='bind'
        )
    ],
    dag=dag 
) 
 
# Set task dependencies 
t1 >> t2


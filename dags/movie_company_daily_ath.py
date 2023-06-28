from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.providers.amazon.aws.operators.athena import AthenaOperator
from datetime import datetime, timedelta


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2023, 6, 27),
    "retries": 1,
    "retry_delay": timedelta(minutes=1)
}

with DAG("movie_company_daily_ath", default_args=default_args, schedule_interval= '@once') as dag:

    insert = AthenaOperator(
        task_id='insert',
        database='athena_db',
        query='''INSERT INTO "athena_db".movie_company
SELECT DISTINCT t.*
FROM "athena_db".movie_company_temp t
LEFT JOIN "athena_db".movie_company s ON t.movieCd = s.movieCd
WHERE s.movieCd IS NULL;''',
        output_location='s3://team3-athena-results/athena-dag-insert/',
        aws_conn_id='project3_aws_conn_id'
    )
    


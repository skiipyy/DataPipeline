import yaml

from datetime import datetime
from airflow import DAG
from airflow.operators import dummy_operator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator


# Default task parameters
args = {
    'retries':0, 'provide_context': True 
}

def import_dag(env, yaml_path, tags):
    '''
        It creates an import dag.
        It will import files from Google Cloud Storage to BigQuery

        Parameters:
            env (str): Environment
            yaml_path (str): Path to the yaml config of this dag
            tags ([str]): List of tags of this dag

        Returns:
            dag (Dag): Dag
    '''

    with DAG(
        dag_id=f'import_{env}',
        schedule_interval=None,
        start_date=datetime(2021,1,1),
        catchup=False,
        max_active_runs=1,
        dagrun_timeout=60,
        tags=tags
        ) as dag:

        start = dummy_operator.DummyOperator(
            task_id='start',
            dag=dag
        )

        end = dummy_operator.DummyOperator(
            task_id='end',
            dag=dag
        )

        # Process files: load files to BQ
        process_file_tasks = []

        with open(yaml_path) as yaml_file:
            config = yaml.full_load(yaml_file)

        for c in config:
            process_file = GCSToBigQueryOperator(
                task_id=f'gcs_to_bigquery_{c["FILENAME"]}',
                bucket='bucket_name',
                source_objects=['file.csv'],
                destination_project_dataset_table=f"DATASET_NAME.TABLE_NAME",
                write_disposition='WRITE_TRUNCATE',
                dag=dag
                )
            process_file_tasks.append(process_file)
        
        start >> process_file_tasks >> end

    return dag
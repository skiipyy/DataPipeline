from airflow import DAG
from airflow.operators import dummy_operator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from datetime import datetime


def orchestrator_dag(env, yaml_path, tags):
    '''
        It creates an orchestrator dag.
        It will trigger multiple dags

        Parameters:
            env (str): Environment
            yaml_path (str): Path to the yaml config of this dag
            tags ([str]): List of tags of this dag

        Returns:
            dag (Dag): Dag
    '''
    with DAG(
        dag_id=f'orchestrator_{env}',
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

        import_dag = TriggerDagRunOperator(
            task_id=f'import_{env}',
            trigger_dag_id=f'import_{env}',
            dag=dag
        )
        process_dag = TriggerDagRunOperator(
            task_id=f'process_{env}',
            trigger_dag_id=f'process_{env}',
            dag=dag
        )
        start >> import_dag >> process_dag >> end

    return dag

from import_dag import import_dag
from process_dag import process_dag
from orchestrator_dag import orchestrator_dag

import yaml
import json

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

# Create dynamic dags
def create_dag(dag_type, env, yaml_path, tags):
    '''
        Choose which type of dag you need to create

        Parameters:
            dag_type (str): Type of dag you want to create
            env (str): Environment
            yaml_path (str): Path to the yaml config of this dag
            tags ([str]): List of tags of this dag

        Returns:
            dag (Dag): Dag
    '''

    if dag_type == 'import':
        print(import_dag(env, yaml_path, tags))
        return import_dag(env, yaml_path, tags)
    elif dag_type == 'process':
        print(process_dag(env, yaml_path, tags))
        return process_dag(env, yaml_path, tags)
    elif dag_type == 'orchestrator':
        print(orchestrator_dag(env, yaml_path, tags))
        return orchestrator_dag(env, yaml_path, tags)

env = 'dv'

# Read config needed to create dynamic dags
with open('./config/dag_config.yaml') as dag_file:
    dag_config = yaml.safe_load(dag_file)
with open('./config/projects_list.json') as json_file:
    projects_config = json.load(json_file)

# Iterate over all the projects
for project in projects_config:
    # Iterate over type of dag needed to be created for this project
    for dag in project['dags']:
        # Create dag
        print(f'{project["project"]}_{dag}')
        print(dag)
        print(env)
        print(dag_config[dag]['path_config'])
        print(dag_config[dag]['tags'])
        globals()[f'{project["project"]}_{dag}'] = create_dag(dag, env, dag_config[dag]['path_config'], dag_config[dag]['tags'])


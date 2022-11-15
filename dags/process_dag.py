import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import json
import yaml
import os

from networkx.readwrite import json_graph
from datetime import datetime
from airflow import DAG
from airflow.operators import dummy_operator, python_operator


class Graph():
    def __init__(self):
        '''
        It will initialize the Graph object

        Parameters:

        Returns:
        '''
        self.G = nx.MultiDiGraph()

    def from_json(self, json_graph):
        '''
        It will set G from a json

        Parameters:
            json_graph (json): The json graph

        Returns:
            self (Graph)
        '''
        self.G = nx.node_link_graph(json_graph)
        return self

    def add_drug(self, drug):
        '''
        It will add one drug to the graph

        Parameters:
            drug (Row): drug Row of DataFrame

        Returns:
        '''
        self.G.add_node(f"drug_{drug['atccode']}", name=drug['drug'], type='drug')

    def add_drugs(self, df_drugs):
        '''
        It will add drugs to the graph

        Parameters:
            df_drugs (DataFrame): drug DataFrame

        Returns:
        '''
        for index, drug in df_drugs.iterrows():
            self.add_drug(drug)

    def add_pubmed(self, pubmed):
        '''
        It will add one pubmed to the graph

        Parameters:
            pubmed (Row): pubmed Row of DataFrame

        Returns:
        '''
        pubmed_node_name = f"pubmed_{pubmed['id']}"
        journal_node_name = f"journal_{pubmed['journal']}"
        self.G.add_node(pubmed_node_name, name=pubmed['title'], type='pubmed')
        self.G.add_node(journal_node_name, name=pubmed['journal'], type='journal')
        # Find drugs with name in pubmed title
        drug_nodes = [node for node, attr in self.G.nodes(data=True) if attr['type']=='drug' and attr['name'].lower() in pubmed['title'].lower()]
        for drug_node in drug_nodes:
            self.G.add_edge(pubmed_node_name, drug_node)
            self.G.add_edge(journal_node_name, pubmed_node_name)
            self.G.add_edge(journal_node_name, drug_node)

    def add_pubmeds(self, df_pubmeds):
        '''
        It will add pubmeds to the graph

        Parameters:
            df_pubmeds (DataFrame): pubmeds DataFrame

        Returns:
        '''
        for index, pubmed in df_pubmeds.iterrows():
            self.add_pubmed(pubmed)

    def add_clinical_trial(self, clinical_trial):
        '''
        It will add one clinical_trial to the graph

        Parameters:
            clinical_trial (Row): clinical_trial Row of DataFrame

        Returns:
        '''
        clinical_trial_node_name = f"clinical_trial_{clinical_trial['id']}"
        journal_node_name = f"journal_{clinical_trial['journal']}"
        self.G.add_node(clinical_trial_node_name, name=clinical_trial['scientific_title'], type='clinical_trial')
        self.G.add_node(journal_node_name, name=clinical_trial['journal'], type='journal')
        # Find drugs with name in clinical_trial title
        drug_nodes = [node for node, attr in self.G.nodes(data=True) if attr['type']=='drug' and attr['name'].lower() in clinical_trial['scientific_title'].lower()]
        for drug_node in drug_nodes:
            self.G.add_edge(clinical_trial_node_name, drug_node)
            self.G.add_edge(journal_node_name, clinical_trial_node_name)
            self.G.add_edge(journal_node_name, drug_node)

    def add_clinical_trials(self, df_clinical_trials):
        '''
        It will add clinical_trials to the graph

        Parameters:
            df_clinical_trials (DataFrame): df_clinical_trials DataFrame

        Returns:
        '''
        for index, clinical_trial in df_clinical_trials.iterrows():
            self.add_clinical_trial(clinical_trial)

    def to_json(self):
        '''
        Get json version of the G

        Parameters:

        Returns:
        '''
        return json_graph.node_link_data(self.G)

    def get_drugs_of_journal(self, journal):
        '''
        Get drugs of one journal

        Parameters:
            journal (str): The journal id in the graph

        Returns:
            ([str]): List of drugs of one journal
        '''
        return [node for node, attr in self.G.nodes(data=True) if attr['type']=='drug' and nx.has_path(self.G, journal, node)]

    def get_journals(self):
        '''
        Get journals of the graph

        Parameters:

        Returns:
            ([str]): List of journals og the graph
        '''
        return [node for node, attr in self.G.nodes(data=True) if attr['type']=='journal']

    def get_journal_with_most_drugs(self):
        '''
        Get journal with the most drugs.
        Multiple journals if same number of drugs

        Parameters:

        Returns:
            ([str]): List of journals
        '''
        journals = self.get_journals()
        max = 0
        res = []
        drugs = []
        for journal in journals:
            drugs = self.get_drugs_of_journal(journal)
            if len(drugs) > max:
                max = len(drugs)
                res = [journal]
            elif len(drugs) == max:
                res.append(journal)
        return res


def generate_json_graph(path_drugs, path_clinical_trials, path_pubmeds, dest_name):
    '''
        It will generate a json graph of drugs, pubmed, cilinical trials and journals

        Parameters:
            path_drugs (str): Path of drugs df
            path_clinical_trials (str): Path of clinical_trials df
            path_pubmeds (str): Path of pubmeds df
            dest_name (str): Path destination result

        Returns:
            json_g (json): The json graph
    '''

    G = Graph()
    df = pd.read_parquet(path_drugs)
    G.add_drugs(df)

    df = pd.read_parquet(path_clinical_trials)
    G.add_clinical_trials(df)

    df = pd.read_parquet(path_pubmeds)
    G.add_pubmeds(df)

    json_g = G.to_json()
    os.makedirs(os.path.dirname(dest_name), exist_ok=True)
    with open(dest_name, 'w') as fp:
        json.dump(json_g, fp)

    print(f'Journals with the most drugs: {G.get_journal_with_most_drugs()}')
    
    return json_g


def process_dag(env, yaml_path, tags):
    '''
        It creates an process dag.
        It will process data to generate a json graph of drugs, pubmed, cilinical trials and journals

        Parameters:
            env (str): Environment
            yaml_path (str): Path to the yaml config of this dag
            tags ([str]): List of tags of this dag

        Returns:
            dag (Dag): Dag
    '''

    with DAG(
        dag_id=f'process_{env}',
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

        with open(yaml_path) as yaml_file:
            c = yaml.safe_load(yaml_file)

        python_task	= python_operator.PythonOperator(
            task_id='python_task',
            python_callable=generate_json_graph,
            provide_context=True,
            op_kwargs={
                "path_drugs": c['drugs']['path'],
                "path_clinical_trials": c['clinical_trials']['path'],
                "path_pubmeds": c['pubmeds']['path'],
                "dest_name": c['output']['path']
            },
            dag=dag
        )

        start >> python_task >> end
    
    return dag
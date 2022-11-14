# DataPipeline

This repository provides a pipeline to process data.


Table of Contents
=================

   * [DataPipeline](#pipeline)
      * [Table of Contents](#table-of-contents)
      * [Project structure](#project-structure)
      * [Quickstart](#quickstart)
         * [Local steps](#local-steps)
         * [Run local](#run-local)
         * [With Airflow](#with-airflow)
    
## Project structure
```
.
├── config
│   ├── dag_config.yaml
│   ├── file_to_import.yaml
│   ├── file_to_process.yaml
│   └── projects_list.json
├── dags
│   ├── create_dags.py
│   ├── import_dag.py
│   ├── orchestrator_dag.py
│   └── process_dag.py
├── import
│   ├── cloudbuild.yaml
│   ├── Dockerfile
│   ├── config
│   │   └── config.ini
│   └── src
│       ├── csvsource.py
│       ├── import.py
│       ├── jsonsource.py
│       ├── mylogger.py
│       ├── source.py
│       └── utils.py
├── .gitignore
├── README.md
├── requirements.txt
├── run_import.sh
└── run_process.py
```

Some explanations regarding structure:
- `config` - folder is where config files about environments and execution context is located.
- `dags` - Airflow dags
- `import` - Import job code
- `run_import.sh` - SH script to run import job
- `run_process.py` - PY script to process data and generate json graph

## Quickstart

### Local steps
Perform the following actions in your development environment:
- Create new venv environment and activate it:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
- Install development dependencies:
```bash
pip install -r /path/to/requirements.txt
```
- Install Airflow:
```bash
pip install "apache-airflow[celery]==2.4.2" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.4.2/constraints-3.7.txt"
```
- Set AIRFLOW_HOME to your local current directory:
```bash
export AIRFLOW_HOME=/path/to/repo/
```
- Init Airflow Database:
```bash
airflow db init
```
- In the '`airflow.cfg`' file set:
```bash
load_examples = False
```
- Create Airflow user:
```bash
airflow users create --username admin --password admin --firstname admin --lastname admin --role Admin --email admin@admin.com
```

### Run local
Run import job:
- Import files from path to local or `GCS`
```bash
./run_import.sh
```
Process data and generate JSON graph locally
```bash
python run_process.py
```
### With Airflow
- Import dag: Load data imported by the import job, from locally or GCS to BQ.
> **_NOTE:_**  
The import dag is available but it will not work because I do not have real GCS buckets and BQ.
This is just to show you.

- Process dag: Process data imported locally, on GCS or on BQ and generate json graph file.
- Orchestrator dag: Trigger import dag then process dag.

Ideally we would run the orchestrator dag so it will trigger the import dag then the process dag.
To do so, run the airflow webserver
```bash
airflow webserver -D -p 8888
```
Then, run the airflow scheduler
```bash
airflow scheduler -D
```

Go to your browser http://localhost:8888/

Dags are created
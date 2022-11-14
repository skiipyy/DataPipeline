python3 import/src/import.py --config_file import/config/config.ini --source_type csv --source_id Clinical_Trials --source ./sample_data/clinical_trials.csv --dest_table tbl_clinical_trials --output_folder ./imported_data

python3 import/src/import.py --config_file import/config/config.ini --source_type csv --source_id Drug            --source ./sample_data/drugs.csv           --dest_table tbl_drugs           --output_folder ./imported_data

python3 import/src/import.py --config_file import/config/config.ini --source_type csv --source_id Pubmed          --source ./sample_data/pubmed.csv          --dest_table tbl_pubmed          --output_folder ./imported_data

# docker run -v /Users/timliu/Documents/projects/DataPipeline/sample_data:/usr/src/sample_data image_test:test python src/import.py --source_type csv --source_id Clinical_Trials --source ../sample_data/clinical_trials.csv --dest_table tbl_clinical_trials --output_folder ./test_landing
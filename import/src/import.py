import argparse
import sys
import logging
import os

from configparser import ConfigParser
from datetime import datetime
from utils import getMilliseconds

from mylogger import getLogger
from csvsource import CSV
from jsonsource import JSON


parser = argparse.ArgumentParser(description='Convert tables to parquet files from a source')


parser.add_argument(
    '--config_file',
    type=str,
    default='config/config.ini',
    dest='config_file',
    help='Path of the config file giving all data sources')

parser.add_argument(
    '--source_type',
    type=str,
    dest='source_type',
    help='Type of the source to import')

parser.add_argument(
    '--source_id',
    type=str,
    dest='source_id',
    help='Source id of the source file to import')

parser.add_argument(
    '--source',
    type=str,
    dest='source',
    help='Path or table name of the source file to import')

parser.add_argument(
    '--dest_table',
    type=str,
    dest='dest_table',
    help='Name of the destination table')

parser.add_argument(
    '--bucket_name',
    type=str,
    dest='bucket_name',
    help='Bucket name to import in GCS')

parser.add_argument(
    '--output_folder',
    type=str,
    dest='output_folder',
    help='Output folder, file will be stored in GCS by default')

parser.add_argument(
    '-d', '--debug',
    action='store_true',
    dest='debug',
    help='set debug level')

parser.add_argument(
    '--env',
    dest='env',
    help='Environment')


args = parser.parse_args()

logger = getLogger('import', logging.DEBUG)

config_file = args.config_file
source_id = args.source_id
source = args.source
source_type = args.source_type.upper()
bucket_name = args.bucket_name
dest_table = args.dest_table
output_folder = args.output_folder
env = args.env

def land_file(tablesource, dest_table):
    '''
        It will land tablesource to dest_table.

        Parameters:
            tablesource (Source): Source Class table
            dest_table (str): Path to the destination table

        Returns:
    '''
    logger.info(f'{tablesource.source} > Start landing this table')

    try:
        df = tablesource.getData()

        line_count = df.shape[0]
        if line_count > 0:
            if output_folder:
                # Save file to local folder
                os.makedirs(output_folder, exist_ok=True)
                filename = os.path.join(output_folder, f'{dest_table}.parquet')
            else:
                filename = f'gs://{bucket_name}/{dest_table}.parquet'

            with open(filename, 'wb') as fout:
                start = datetime.now()
                logger.info(f'{tablesource.source} > Start loading to {filename}')
                df.to_parquet(engine='pyarrow', path=fout)
                logger.info(f'{tablesource.source} > Saved to parquet at {filename} in {getMilliseconds(datetime.now() - start)} ms')
                fout.close()

            logger.info(f'{tablesource.source} > Successfully landed in {filename}')
    except Exception as err:
        logger.error(f'Error while landing {tablesource.source} - {err}')
    return



if __name__ == '__main__':
    logger.info(f'Start import {env} ...')

    logger.info(
        f'Importing with config: {config_file}, source id: {source_id}, source: {source}, source type: {source_type}, bucket: {bucket_name}, destination table: {dest_table}'
    )

    # Read config
    config = ConfigParser()
    logger.info(f'Reading config from {config_file}')
    try:
        with open(config_file) as f:
            config.read_file(f)
    except IOError as err:
        logger.error(f'Error while reading {config_file} file - {err}')
        sys.exit(1)

    if source_id not in config and source_type not in ('EXCEL', 'CSV'):
        logger.error(f'Missing config for {source_id} in config file')

    if source_type == 'CSV':
        tablesource = CSV(config[source_id], source, source_type, debug=args.debug)
    elif source_type == 'JSON':
        tablesource = JSON(config[source_id], source, source_type, debug=args.debug)
    else:
        logger.error(f'Source type {source_type} not supported for the moment')

    land_file(tablesource, dest_table)
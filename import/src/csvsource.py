import pandas as pd
import os
import sys
import logging

from datetime import datetime
from utils import getMilliseconds
from source import FileSource
from mylogger import getLogger

logger = getLogger(__name__)

class CSV(FileSource):
    def __init__(self, config, source, sourceType, debug):
        super().__init__(config, source, sourceType, debug)
        self.extension = '.csv'
        self.name =os.path.splitext(source)[0]
    
    def getData(self):
        '''
            Get data from CSV source

            Parameters:

            Returns:
                data (DataFrame): Dataframe of the CSV data
        '''
        start = datetime.now()

        logger.info(f'{self.source} > Start getData from the source')

        # Check extension
        if not self.source.endswith(self.extension):
            logger.error(f'{self.source} extension should be {self.extension}')
            sys.exit(1)
        if not os.path.exists(self.source):
            logger.error(f'{self.source} file does not exist')
            sys.exit(1)
        data = pd.read_csv(self.source, encoding='utf8')

        logger.info(f'{self.source} > getData {getMilliseconds(datetime.now() - start)} ms')

        return data
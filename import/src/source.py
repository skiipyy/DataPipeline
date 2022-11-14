from mylogger import getLogger
from abc import ABC, abstractmethod

logger = getLogger(__name__)

class Source(ABC):
    def __init__(self, config, source, sourceType, debug):
        self.config = config
        self.source = source
        self.sourceType = sourceType

    @abstractmethod
    def getData(self):
        pass

class FileSource(Source):
    def __init__(self, config, source, sourceType, debug):
        super().__init__(config, source, sourceType, debug)

class SQLSource(Source):
    def __init__(self, config, source, sourceType, debug):
        super().__init__(config, source, sourceType, debug)

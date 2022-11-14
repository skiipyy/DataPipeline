import logging

def getLogger(name, debug = False):
    '''
        Get cutom loger

        Parameters:
            debug (Bool): If debug mode activated

        Returns:
            logger (Logger): The custom logger
    '''
    logging.getLogger(name).setLevel(logging.DEBUG if debug else logging.INFO)
    logger = logging.getLogger(name)

    if len(logger.handlers) == 0:
        logger.setLevel(logging.getLogger(name).getEffectiveLevel())
        sh = logging.StreamHandler()
        sh.setFormatter(logging.Formatter('[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s'))
        logger.addHandler(sh)
    
    return logger
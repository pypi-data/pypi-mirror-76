import logging
from logging.handlers import TimedRotatingFileHandler

# logger.debug('debug message')
# logger.info('info message')
# logger.warning('warn message')
# logger.error('error message')
# logger.critical('critical message')

def initOneDayLog(name1,logfile):
    logger = logging.getLogger(name1)
    logger.setLevel(logging.INFO)
    ch = TimedRotatingFileHandler(logfile, when='D', encoding="utf-8")
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


import logging
import logging.config

def get_logger(name, level=logging.DEBUG):
    # ignore warning from other module
    logging.config.dictConfig({
      'version': 1,
      'disable_existing_loggers': True
    })

    logger = logging.getLogger(name)
  
    # remove exsiting handlers -> prevents logged twice
    for hdlr in logger.handlers[:]:
        logger.removeHandler(hdlr)
  
    # set output to file
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter('%(asctime)s, %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', datefmt='%H:%M:%S'))
    logger.addHandler(sh)
    logger.setLevel(level)
  
    return logger

logger =get_logger(__name__)
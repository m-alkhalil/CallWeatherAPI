import logging
from logging.config import dictConfig



def configure_logger(logger_name: str)-> logging.Logger:
    '''
    This function expects the logger name as string, configure a logger using dictionary and return a logger object

    Parameters: 
        Logger_name: string

    Raises:
        ValueError, KeyError, TypeError,AttributeError, ImportError

    Returns:
        Returns a logger object with the name Logger_name:str
    '''

    config_dict = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters':{
            'standard': {
                'format': '%(asctime)s - %(name)s-%(levelname)-8s:%(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },
        'handlers':{
            'file': {
                'level': 'DEBUG',
                'formatter':'standard',
                'class': 'logging.FileHandler',
                'filename': 'logs/weather_data.log',
                'mode':'a',
            },
        },
        'loggers':{
            logger_name:{
                'level': 'DEBUG',
                'handlers':['file'],
                'propagate': False,
            },
        },
    }
    app_logger= None
    try:
        dictConfig(config_dict)
        app_logger = logging.getLogger(logger_name)
        app_logger.info("logCoOnfigure Module:: Logger has been configured successfully...")

    except (ValueError, KeyError, TypeError,AttributeError, Exception) as exp_error :
        print(f"Logging configuration failed: {exp_error}")

    # app_logger = logging.getLogger(logger_name)

    return app_logger
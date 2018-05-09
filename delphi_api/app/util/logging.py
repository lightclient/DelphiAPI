import logging
import logging.config

def pretty_print(list):

    if(type(list) is dict):
        tmp = []
        for k,v in list.items():
            tmp.append( (k,v) )

        list = tmp

    longest_key = 0
    longest_val = 0
    for el in list:
        longest_key = len(el[0]) if len(el[0]) > longest_key else longest_key
        longest_val = len(el[1]) if len(el[1]) > longest_val else longest_val

    for el in list:
        print( "+" + "-" * (longest_key + 2) + "+" + "-" * (longest_val + 2) + "+" )
        print( "| " + el[0] + " " * (longest_key - len(el[0])) + " | " + el[1] + " " * (longest_val - len(el[1])) + " |" )


    print( "+" + "-" * (longest_key + 2) + "+" + "-" * (longest_val + 2) + "+" )

class GunicornFilter(logging.Filter):
    def filter(self, record):
        # workaround to remove the duplicate access log
        if '"- - HTTP/1.0" 0 0' in record.msg:
            return False
        else:
            return True


def setup_logging():
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "gunicorn_filter": {
                "()": GunicornFilter
            }
        },
        "formatters": {
            "standard": {
                # "format": settings.get("LOG_FORMAT"),
                # "datefmt": settings.get("LOG_DATE_FORMAT")
            }
        },
        "handlers": {
            "console": {
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "filters": ["gunicorn_filter"],
            }
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                # "level": settings.get("LOG_LEVEL")
            }
        }
    }

    logging.config.dictConfig(config)

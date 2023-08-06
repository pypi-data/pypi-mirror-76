from datetime import datetime
import sys
from traceback import format_tb

from .models import Exc


def save_exc():
    exc, exc_value, tb = sys.exc_info()
    Exc(
        exc_type=exc.__module__ + '.' + exc.__name__ if exc.__module__ else exc.__name__,
        exc_value=exc_value if exc_value else '',
        exc_traceback='\n'.join(format_tb(tb))
    ).save()

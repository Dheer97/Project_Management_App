from ast import Try
import logging
import traceback
from datetime import datetime
from urllib import response

logger=logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response

    def __call__(self, request):
        
        user=request.user if request.user.is_authenticated else 'Anonymous'
        method=request.method
        path=request.get_full_path()

        logger.info(f"Incoming Request:{method} {path}|User:{user}")
        try:
            response=self.get_response()
            return response
        except Exception as e:
            logger.error(f"Exception occured wile processing request: \n {e}")
            logger.error(traceback.format_exc)
            raise
from rest_framework.views import exception_handler
from rest_framework.response import Response
import logging


logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        return response

    logger.exception("Unhandled exception in DRF view: %s", exc)
    return Response({"code": 500, "data": '服务器发生错误'}, status=500)
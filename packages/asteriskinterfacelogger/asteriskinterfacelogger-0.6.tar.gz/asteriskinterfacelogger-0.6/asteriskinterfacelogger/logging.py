import os
import inspect
import logging
import logstash
from pythonjsonlogger.jsonlogger import JsonFormatter


def get_parent_module():
    for frame in inspect.stack():
        code = frame.code_context
        if code is not None:
            if code[0].strip() == "from asteriskinterfacelogger.logging import logger":
                module = inspect.getmodule(frame[0])
                package = module.__package__
                return package.split(".")[0]


logstach_host = os.environ.get("LOGSTACH_HOST". "logstash")

module_name = get_parent_module()
logger = logging.getLogger(module_name)
logger.setLevel(logging.DEBUG)
handler = logstash.TCPLogstashHandler(logstach_host, 5959, version=1)
logger.addHandler(handler)
handler.setFormatter(
    JsonFormatter(
        "%(asctime)s %(name)-12s %(levelname)+8s %(message)s [%(pathname)s %(module)s %(filename)s:%(lineno)s - %(funcName)20s() ]"
    )
)

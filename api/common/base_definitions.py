import datetime, os, logging
from flask import Flask, jsonify, Response
from flask.json import JSONEncoder
from flask_cors import CORS

log_level = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}
class BaseJSONEncoder(JSONEncoder):
    """
    Encodes JSON
    """
    def default(self, obj):
        print(obj)
        try:
            if isinstance(obj, datetime.date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

class BaseResponse(Response):
    """
    Base response
    """
    default_mimetype = 'application/json'

    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(BaseResponse, cls).force_type(rv, environ)
    

class BaseFlask(Flask):
    """
    Construct base application module
    """
    response_class = BaseResponse
    json_encoder = BaseJSONEncoder

    def __init__(
        self,
        import_name
    ):
        Flask.__init__(
            self,
            import_name
        )
        self.config.from_object('api.common.config.BaseConfig')
        # configure logging
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler(os.getenv('LOGGING_LOCATION', 'logs/log.log'), 'a', 1 * 1024 * 1024, 10)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        )
        self.logger.setLevel(log_level[os.getenv('LOGGING_LEVEL', 'DEBUG')])
        file_handler.setLevel(log_level[os.getenv('LOGGING_LEVEL', 'DEBUG')])
        self.logger.addHandler(file_handler)

        CORS(self, resources={r"/*": {"origins": "*"}})
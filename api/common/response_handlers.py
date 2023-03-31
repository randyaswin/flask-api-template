import datetime
from api.common.utils.helpers import get_curret_flask_url_path, get_curret_method
from flask import jsonify, json
from werkzeug.exceptions import NotFound, Unauthorized, Forbidden, MethodNotAllowed, NotImplemented, BadRequest
from api.common.utils.exceptions import APIException, ServerErrorException, NotFoundException, UnauthorizedException, \
    ForbiddenException, MethodNotAllowedException, NotImplementedException, BadRequestException

def handle_exception(error: APIException):
    """
    Handle specific raised API Exception
    """
    # current_app.logger.debug(error.message)
    e = {"status": "error",
         "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
         "data": {
             "name": error.name,
             "description": error.message,
         },
         "method": get_curret_method(),
            "url_path": get_curret_flask_url_path(),
            }
    response = jsonify(e)
    response.status_code = error.status_code
    return response

def handle_general_exception(e):
    """
    Handle general exceptions
    """
    # current_app.logger.debug(e)
    return handle_exception(ServerErrorException())

def handle_werkzeug_exception(e):
    """
    Handle Werkzeug Exceptions: return JSON instead of HTML for HTTP errors.
    """
    # current_app.logger.debug(e)
    if isinstance(e, NotFound):
        return handle_exception(NotFoundException(message=e.description))
    if isinstance(e, Unauthorized):
        return handle_exception(UnauthorizedException(message=e.description))
    if isinstance(e, Forbidden):
        return handle_exception(ForbiddenException(message=e.description))
    if isinstance(e, MethodNotAllowed):
        return handle_exception(MethodNotAllowedException(message=e.description))
    if isinstance(e, NotImplemented):
        return handle_exception(NotImplementedException(message=e.description))
    if isinstance(e, BadRequest):
        return handle_exception(BadRequestException(message=e.description))

    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "status": "error",
        "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
        "data":{
        "name": e.name,
        "description": e.description,
        },
        "method": get_curret_method(),
        "url_path": get_curret_flask_url_path(),
    })
    response.content_type = "application/json"
    return response
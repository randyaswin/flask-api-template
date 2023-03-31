from contextlib import contextmanager
import flask
from sqlalchemy import exc
from urllib import parse

from api.common.utils.exceptions import ServerErrorException, InvalidPayloadException, NotFoundException, \
    ValidationException


@contextmanager
def session_scope(session):
    """
    Provide a transactional scope around a series of operations.
    """
    try:
        yield session
        session.commit()
    except (InvalidPayloadException, NotFoundException, ValidationException) as e:
        session.rollback()
        raise e
    except exc.SQLAlchemyError:
        session.rollback()
        raise ServerErrorException()


def get_curret_method():
    return flask.request.method

def get_curret_flask_url_path():
    return flask.request.path

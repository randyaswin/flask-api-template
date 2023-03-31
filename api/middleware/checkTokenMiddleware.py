from flask import Flask, request, make_response, jsonify
from api.common.utils.exceptions import ForbiddenException
from functools import wraps
import psycopg2
import jwt
import datetime
import os
import requests
import json
import logging as logger


class checkTokenMiddleware:
    def token_required(f):
        @wraps(f)
        def decorate(*args, **kwargs):
            token = None
            if "Authorization" in request.headers:
                try:
                    token = request.headers["Authorization"].split()[1]
                except:
                    raise ForbiddenException(message='Token is Missing')
            else:
                raise ForbiddenException(message='Token is Invalid')
            if not token:
                raise ForbiddenException(message='Token is Invalid')
            try:
                token_data = jwt.decode(
                    token, os.environ.get("JWT_SECRET_KEY"), algorithms="HS256"
                )
                kwargs["token_data"] = token_data
            except:
                raise ForbiddenException(message='Token is Missing')

            return f(*args, **kwargs)

        return decorate

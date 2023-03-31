from typing import Any
from api.common.utils import exceptions
from api.common import error_handlers
from api.module.ModuleOne.ModuleOne import ModuleOne
import datetime
from werkzeug.exceptions import HTTPException
from flask import request, jsonify, make_response, Response
from flask_sqlalchemy import SQLAlchemy
from api.common.base_definitions import BaseFlask, BaseResponse
import api.tasks as tasks

from api.middleware.checkTokenMiddleware import checkTokenMiddleware

db = SQLAlchemy()

app = BaseFlask(__name__)
app.register_error_handler(exceptions.InvalidPayloadException, error_handlers.handle_exception)
app.register_error_handler(exceptions.BadRequestException, error_handlers.handle_exception)
app.register_error_handler(exceptions.UnauthorizedException, error_handlers.handle_exception)
app.register_error_handler(exceptions.ForbiddenException, error_handlers.handle_exception)
app.register_error_handler(exceptions.NotFoundException, error_handlers.handle_exception)
app.register_error_handler(exceptions.ServerErrorException, error_handlers.handle_exception)
app.register_error_handler(Exception, error_handlers.handle_general_exception)
app.register_error_handler(HTTPException, error_handlers.handle_werkzeug_exception)
db.init_app(app)

############### dengan background process ###############
@app.route("/api/v1.0/module/add", methods=["POST"])
@checkTokenMiddleware.token_required
def module1(**kwargs):
    token_data = kwargs.get("token_data", {})
    request_json = request.get_json()
    job = tasks.add.delay(x=1, y=2)
    return {"job_id": job.id}

@app.route("/api/v1.0/module/add/status", methods=["GET"])
@checkTokenMiddleware.token_required
def module1_status(**kwargs):
    token_data = kwargs.get("token_data", {})
    job_id = request.args.get("job_id")
    job = tasks.get_job(job_id)
    return {"status": job.state}

@app.route("/api/v1.0/module/add/result", methods=["GET"])
@checkTokenMiddleware.token_required
def module1_result(**kwargs):
    token_data = kwargs.get("token_data", {})
    job_id = request.args.get("job_id")
    job = tasks.get_job(job_id)
    if job.state != "SUCCESS":
        return {"message": "job not finished"}
    response = {"result": job.result}
    return response

########################################################

############### tanpa background process ###############

@app.route("/api/v1.0/module/subtract", methods=["GET"])
@checkTokenMiddleware.token_required
def module1_substract(**kwargs):
    token_data = kwargs.get("token_data", {})
    x = int(request.args.get("x"))
    y = int(request.args.get("y"))
    m = ModuleOne(x, y)
    result = m.subtract()
    return {"result": result}

@app.route("/api/v1.0/module/get_data", methods=["GET"])
@checkTokenMiddleware.token_required
def get_data(**kwargs):
    token_data = kwargs.get("token_data", {})
    m = ModuleOne(None, None)
    result = m.getData(db.engine)
    return {"result": result}

@app.route("/api/v1.0/module/get_data_post", methods=["POST"])
@checkTokenMiddleware.token_required
def get_data(**kwargs):
    token_data = kwargs.get("token_data", {})
    request_json = request.get_json()
    m = ModuleOne(None, None)
    result = m.getData(db.engine)
    return {"result": result}

@app.route("/api/v1.0/module/health")
def health():
    return make_response(jsonify({"message": "healty"}), 200)
########################################################

if __name__ == "__main__":
    app.run(host="0.0.0.0")

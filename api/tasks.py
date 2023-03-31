from celery import Celery, Task
from celery.result import AsyncResult
from api.module.ModuleOne.ModuleOne import ModuleOne
from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker
import os


CELERY = Celery(
    "tasks",
    backend="db+postgresql://{}:{}@{}:{}/{}".format(
    os.getenv("DB_USERNAME"),
    os.getenv("DB_PASSWORD"),
    os.getenv("DB_HOST"),
    os.getenv("DB_PORT"),
    os.getenv("DB_NAME"),
),
    broker=os.getenv("BROKER_URL"),
)

CELERY.conf.accept_content = ["json", "msgpack"]
CELERY.conf.result_serializer = "msgpack"
CELERY.conf.update(result_extended=True)
CELERY.conf.database_table_schemas = {
    "task": os.getenv("CELERY_SCHEME"),
    "group": os.getenv("CELERY_SCHEME"),
}


class CustomBase(Task):
    _db_session = None
    _db_engine = None

    def before_start(self, task_id, args, kwargs):
        self._db_engine = create_engine(
            f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
        )
        engine = self._db_engine.connect()
        Session = sessionmaker(bind=engine)
        self._db_session = Session()

    def after_return(self, *args, **kwargs):
        if self._db_engine is not None:
            self._db_engine.dispose()
        self._db_engine = None

    def on_success(self, retval, task_id, args, kwargs):
        if self._db_engine is not None:
            self._db_engine.dispose()
        self._db_engine = None
        pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        self._db_session.commit()
        if self._db_engine is not None:
            self._db_engine.dispose()
        self._db_engine = None

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        self._db_session.commit()


def get_job(job_id):

    """
    To be called from our web app.
    The job ID is passed and the celery job is returned.
    """
    return AsyncResult(
        job_id,
        app=CELERY,
    )


def revoke_job(job_id):
    """
    To be called from our web app.
    The job ID is passed and the celery job is returned.
    """

    return CELERY.control.revoke(job_id, terminate=True, signal="SIGKILL")


@CELERY.task(
    base=CustomBase,
    bind=True,
    name="moduleOne_" + os.getenv("ENVIRONMENT"),
    queue="moduleOne_" + os.getenv("ENVIRONMENT"),
)
def add(self, *args, **kwargs):
    x, y = kwargs.get("x"), kwargs.get("y")
    m1 = ModuleOne(x, y)
    return m1.add()
    

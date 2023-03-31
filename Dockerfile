FROM python:3.8.2

WORKDIR /api
ADD requirements.txt /api/requirements.txt
RUN pip install -r requirements.txt

COPY . /api
RUN chmod +x /api/scripts/run_celery.sh
RUN chmod +x /api/scripts/run_web.sh

# create unprivileged user
RUN adduser --disabled-password --gecos '' api  
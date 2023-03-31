#!/bin/sh
export USE_PYGEOS=0
export $(grep -v '^#' .env | xargs)
cd /api
su -m api -c  "uwsgi --ini app.ini"
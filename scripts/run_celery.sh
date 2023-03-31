#!/bin/sh
export USE_PYGEOS=0
export $(grep -v '^#' .env | xargs)
cd /api
su -m api -c "celery -A api.tasks worker --loglevel INFO -Q moduleOne_$ENVIRONMENT --autoscale=10,0" 

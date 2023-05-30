#!/bin/bash

# pip install -r requirements.txt
# kill ` lsof -i:8084 | awk '{NR==2 ;print $2}' ` 

pkill -f "gunicorn api:app -b 0.0.0.0:8085"
nohup gunicorn api:app -b 0.0.0.0:8085 -w 1 --threads 20 -k uvicorn.workers.UvicornWorker > logs/api.log.txt 2>&1 &

lsof -i:8085

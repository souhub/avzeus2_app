#!/bin/bash

until mysql -h$DB_HOST -u$DB_USER -p$DB_PASSWORD &> /dev/null
do
    echo "Waiting for mysql to start..."
    sleep 1
done

cd /usr/src/app/app && uvicorn main:app --reload --port=8080 --host=0.0.0.0

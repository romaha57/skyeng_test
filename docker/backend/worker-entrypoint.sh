#!/bin/sh

until cd /app/backend
do
    echo "Waiting for server volume..."
done

# run a worker :)
celery -A check_file worker --loglevel=info --concurrency 1 -E

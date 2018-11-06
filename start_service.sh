#!/bin/bash
# celery worker -A app -l INFO
gunicorn  --config=gunicorn.conf wsgi_gunicorn:app --log-level=info

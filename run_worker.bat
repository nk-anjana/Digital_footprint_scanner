@echo off
echo Starting Celery Worker for Windows...

:: Set PYTHONPATH so it can find the backend module from the root directory
set PYTHONPATH=%cd%

:: Run Celery with pool=solo (required for Windows)
celery -A backend.celery_worker.celery_app worker --loglevel=info --pool=solo

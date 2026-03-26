@echo off
echo Starting FastAPI OSINT Backend...

:: Set PYTHONPATH so it can find the backend module from the root directory
set PYTHONPATH=%cd%

uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

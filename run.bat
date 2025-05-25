@echo off
echo Activando entorno virtual y ejecutando app FastAPI...
call venv\Scripts\activate
uvicorn main:app --reload

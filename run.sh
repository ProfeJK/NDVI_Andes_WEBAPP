#!/bin/bash
echo "Activando entorno virtual y ejecutando app FastAPI..."
source venv/bin/activate
uvicorn main:app --reload

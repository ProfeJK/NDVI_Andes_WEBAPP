from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from utils.NDVI_analysis import analizar_ndvi_desde_tiff
import openai
import shutil
from pathlib import Path

# Cargar API Key desde .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
print("🔍 Clave cargada:", api_key)
openai.api_key = api_key

# Inicializar FastAPI
app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas estáticas y plantillas
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Configuración de carpetas
UPLOAD_DIR = "data/uploads"
BIN_OUTPUT = "static/ndvi_binaria.png"
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
async def analyze_image(
    file: UploadFile = File(...),
    crop_type: str = Form(""),
    crop_stage: str = Form("")
):
    try:
        # Guardar imagen subida
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Analizar imagen NDVI
        resultados = analizar_ndvi_desde_tiff(file_location, threshold=0.6, save_path=BIN_OUTPUT)
        ndvi_mean = resultados["ndvi_promedio"]
        high_ndvi_percent = resultados["porcentaje_ndvi_alto"]

        # Generar prompt para GPT
        prompt = (
            f"Tengo una imagen NDVI para un cultivo de {crop_type} en etapa {crop_stage}. "
            f"El NDVI promedio es {ndvi_mean:.3f} y el {high_ndvi_percent:.2f}% del área tiene NDVI > 0.6. "
            f"¿Qué interpretación agronómica puedes ofrecer?"
        )

        # Llamada a OpenAI con nueva API (v1)
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Eres NDVI_ANDES, un experto en interpretación de imágenes NDVI para agricultura de precisión. Responde siempre en español con claridad técnica."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7
        )

        answer = response.choices[0].message.content

        return JSONResponse({
            "ndvi_promedio": ndvi_mean,
            "porcentaje_ndvi_alto": high_ndvi_percent,
            "imagen_binaria_url": "/static/ndvi_binaria.png",
            "respuesta": answer
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

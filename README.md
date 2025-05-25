# NDVI_ANDES WebApp

Esta aplicación permite subir una imagen NDVI (formato `.jpg` o `.png`), calcular su valor promedio y obtener una interpretación automática a través de un modelo GPT especializado en agricultura de precisión.

---

## 🔧 Requisitos

- Python 3.10+
- Clave API de OpenAI (https://platform.openai.com/account/api-keys)
- Imagen NDVI en escala de grises

---

## 📦 Instalación de dependencias

```bash
pip install fastapi uvicorn openai python-multipart python-dotenv pillow numpy
```

---

## 🔐 Configura tu clave API

Crea un archivo `.env` en el mismo directorio que `main.py` con el siguiente contenido:

```env
OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

---

## 🚀 Ejecución del backend

```bash
uvicorn main:app --reload
```

La API estará disponible en:

- `http://127.0.0.1:8000` → Ruta raíz
- `http://127.0.0.1:8000/docs` → Documentación Swagger
- `http://127.0.0.1:8000/analyze` → Endpoint POST para subir imágenes NDVI

---

## 🌐 Uso del Frontend

1. Abre `index.html` en tu navegador.
2. Sube una imagen NDVI procesada.
3. Verás el valor promedio de NDVI y la respuesta de **NDVI_ANDES GPT** con recomendaciones personalizadas.

---

## 📁 Estructura del Proyecto

```
.
├── main.py           ← API con FastAPI
├── index.html        ← Interfaz web
├── .env              ← Clave secreta (no subir a GitHub)
└── README.md         ← Esta guía
```

---

## 🧠 Modelo conectado

Este proyecto se conecta con un GPT personalizado llamado **NDVI_ANDES**, diseñado para interpretar imágenes NDVI capturadas con drones y generar recomendaciones para agricultura de precisión.


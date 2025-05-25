import numpy as np
import rasterio
from PIL import Image

def analizar_ndvi_desde_tiff(path_tiff, threshold=0.6, save_path=None):
    """
    Analiza una imagen TIFF que puede tener diferentes formatos:
    - NDVI reales (float32, 1 banda)
    - Imágenes RGB o RGBA en uint8 normalizadas a escala 0-1

    Devuelve estadísticas NDVI simuladas y guarda imagen binaria si se solicita.
    """
    with rasterio.open(path_tiff) as src:
        band_count = src.count
        dtype = src.dtypes[0]

        # Caso 1: NDVI real (float32, 1 banda)
        if band_count == 1 and dtype == 'float32':
            ndvi = src.read(1)

        # Caso 2: Imagen RGB/RGBA (uint8 o uint16)
        elif band_count >= 3 and dtype in ['uint8', 'uint16']:
            # Usamos solo la primera banda como proxy (p. ej. rojo o verde)
            base_band = src.read(1).astype(np.float32)
            # Normalizamos a 0–1
            ndvi = (base_band - base_band.min()) / (base_band.max() - base_band.min())
        else:
            raise ValueError("Formato de imagen no compatible: se requiere TIFF con 1 banda NDVI o RGB/RGBA.")

    ndvi_mean = float(np.mean(ndvi))
    high_ndvi_percent = float(np.sum(ndvi > threshold) / ndvi.size * 100)

    # Generar imagen binaria
    binary_mask = (ndvi > threshold).astype(np.uint8) * 255
    binary_img = Image.fromarray(binary_mask)

    if save_path:
        binary_img.save(save_path)

    return {
        "ndvi_promedio": round(ndvi_mean, 3),
        "porcentaje_ndvi_alto": round(high_ndvi_percent, 2)
    }

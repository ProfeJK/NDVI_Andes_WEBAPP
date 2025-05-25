import numpy as np
import rasterio
from PIL import Image

def analizar_ndvi_desde_tiff(path_tiff, threshold=0.5, save_path=None):
    """
    Lee una imagen NDVI en formato .tiff, calcula estadísticas y genera una imagen binaria si se desea.

    Parámetros:
        - path_tiff: ruta al archivo NDVI en formato TIFF
        - threshold: umbral NDVI para clasificar como 'zona saludable'
        - save_path: si se indica, guarda la imagen binaria en esa ruta

    Retorna:
        - Diccionario con promedio de NDVI y porcentaje de área con NDVI > threshold
    """
    with rasterio.open(path_tiff) as src:
        ndvi = src.read(1).astype(np.float32)

    ndvi_mean = float(np.mean(ndvi))
    high_ndvi_percent = float(np.sum(ndvi > threshold) / ndvi.size * 100)

    # Generar imagen binaria en PIL
    binary_mask = (ndvi > threshold).astype(np.uint8) * 255
    binary_img = Image.fromarray(binary_mask)

    if save_path:
        binary_img.save(save_path)

    return {
        "ndvi_promedio": round(ndvi_mean, 3),
        "porcentaje_ndvi_alto": round(high_ndvi_percent, 2)
    }

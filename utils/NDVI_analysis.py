import numpy as np
import rasterio
from PIL import Image

def analizar_ndvi_desde_tiff(path_tiff, threshold=0.6, save_path=None):
    """
    Analiza imágenes TIFF en múltiples formatos:
    - Monocanal NDVI reales (float32, float64)
    - Imágenes RGB/RGBA en uint8
    - Imágenes clasificadas tipo KMeans en uint8/uint16

    Genera mapa binario y estadísticas adaptadas a cada tipo.
    """
    with rasterio.open(path_tiff) as src:
        band_count = src.count
        dtype = src.dtypes[0]

        # Caso 1: RGB o RGBA
        if band_count >= 3 and dtype == 'uint8':
            # Convertir a NDVI sintético desde banda 1 (Rojo) como proxy
            red_channel = src.read(1).astype(np.float32)
            ndvi = (red_channel - red_channel.min()) / (red_channel.max() - red_channel.min())
            ndvi = ndvi * 2 - 1  # Escalar a [-1, 1]

        # Caso 2: Monocanal, valores NDVI reales (float)
        elif band_count == 1 and dtype.startswith("float"):
            ndvi = src.read(1)
            # Validar si está en rango [-1, 1], si no, normalizar
            if np.max(ndvi) > 1.0 or np.min(ndvi) < -1.5:
                ndvi = (ndvi - np.min(ndvi)) / (np.max(ndvi) - np.min(ndvi))
                ndvi = ndvi * 2 - 1

        # Caso 3: Monocanal tipo máscara (uint8/uint16)
        elif band_count == 1 and dtype in ['uint8', 'uint16']:
            band = src.read(1).astype(np.float32)
            ndvi = (band - band.min()) / (band.max() - band.min())
            ndvi = ndvi * 2 - 1

        else:
            raise ValueError("Formato no compatible: RGB, monocanal float o uint8/16.")

    # Cálculos NDVI
    ndvi_mean = float(np.mean(ndvi))
    high_ndvi_percent = float(np.sum(ndvi > threshold) / ndvi.size * 100)

    # Mapa binario (255 si NDVI > threshold)
    try:
        binary_mask = (ndvi > threshold).astype(np.uint8) * 255
        binary_img = Image.fromarray(binary_mask)
        if save_path:
            binary_img.save(save_path)
    except Exception as e:
        print("❌ Error al generar imagen binaria:", e)

    return {
        "ndvi_promedio": round(ndvi_mean, 3),
        "porcentaje_ndvi_alto": round(high_ndvi_percent, 2)
    }

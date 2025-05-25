from PIL import Image
import numpy as np

def calculate_ndvi(multiband_image):
    """
    Calcula el NDVI de una imagen multibanda. 
    Se espera que la imagen tenga al menos dos bandas: una roja y una infrarroja cercana (NIR).
    """
    image_array = np.array(multiband_image)

    if len(image_array.shape) < 3 or image_array.shape[2] < 2:
        raise ValueError("La imagen debe tener al menos dos bandas (Rojo y NIR).")

    red = image_array[:, :, 0].astype(float)
    nir = image_array[:, :, 1].astype(float)

    numerator = nir - red
    denominator = nir + red
    ndvi = np.divide(numerator, denominator, out=np.zeros_like(numerator), where=denominator != 0)

    ndvi_mean = float(np.mean(ndvi))
    return ndvi_mean

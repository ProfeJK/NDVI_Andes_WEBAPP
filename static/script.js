document.getElementById('uploadForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const fileInput = document.getElementById('image');
    const cropTypeInput = document.getElementById('crop_type');
    const cropStageInput = document.getElementById('crop_stage');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('crop_type', cropTypeInput.value);
    formData.append('crop_stage', cropStageInput.value);

    const resultText = document.getElementById('resultText');
    const ndviImage = document.getElementById('ndviImage');

    resultText.textContent = "Procesando...";
    ndviImage.style.display = "none";

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.ndvi_promedio !== undefined && data.porcentaje_ndvi_alto !== undefined) {
            resultText.textContent = `NDVI promedio: ${data.ndvi_promedio.toFixed(3)}\nPorcentaje NDVI > 0.6: ${data.porcentaje_ndvi_alto}%`;

            if (data.imagen_binaria_url) {
                ndviImage.src = data.imagen_binaria_url;
                ndviImage.style.display = "block";
            }

            if (data.respuesta) {
                resultText.textContent += `\n\nGPT responde:\n${data.respuesta}`;
            }

        } else {
            resultText.textContent = "Error: " + (data.error || "Desconocido");
        }

    } catch (err) {
        resultText.textContent = "Error de conexión con el servidor.";
    }
});

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from pdf2image import convert_from_bytes
from PIL import Image
import io
import zipfile

app = FastAPI()

@app.post("/convert-pdf/")
async def convert_pdf(file: UploadFile = File(...), format: str = "png"):
    if format.lower() not in ["png", "jpeg", "jpg"]:
        return {"error": "Formato no soportado. Usa png o jpeg."}

    # Leer archivo PDF
    pdf_bytes = await file.read()

    # Convertir PDF a imágenes
    images = convert_from_bytes(pdf_bytes)

    if len(images) == 1:
        img_bytes = io.BytesIO()
        images[0].save(img_bytes, format=format.upper())
        img_bytes.seek(0)
        return StreamingResponse(img_bytes, media_type=f"image/{format}")

    # Si hay varias páginas, devolver archivo ZIP
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for i, image in enumerate(images):
            img_io = io.BytesIO()
            image.save(img_io, format=format.upper())
            img_io.seek(0)
            zip_file.writestr(f"page_{i+1}.{format}", img_io.read())

    zip_buffer.seek(0)
    return StreamingResponse(zip_buffer, media_type="application/zip", headers={
        "Content-Disposition": "attachment; filename=converted_images.zip"
    })

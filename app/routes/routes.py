import os
import shutil

from fastapi import APIRouter, FastAPI, File, UploadFile
from app.handlers.google_document_ai import GoogleDocumentAI
from app.handlers.cache import get_cached_data, set_cached_data

router = APIRouter()


@router.get("/status")
async def read_status():
    return {"status": "running"}


@router.post("/file_upload")
async def file_upload(file: UploadFile = File(...)):
    document = await get_cached_data(file.filename)
    if document is None:
        upload_folder = "app/uploads/"
        os.makedirs(upload_folder, exist_ok=True)

        with open("app/uploads/" + file.filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        document_ai = GoogleDocumentAI(
            os.getenv("PROJECT_ID"),
            os.getenv("LOCATION"),
            os.getenv("PROCESSOR_ID"),
            os.getenv("PROCESSOR_VERSION"),
        )

        document = document_ai.process_document(
            "app/uploads/" + file.filename, "application/pdf"
        )

        await set_cached_data(file.filename, document, expiry=3600 * 24)

        # Delete the file
        try:
            os.remove("app/uploads/" + file.filename)
        except OSError as e:
            print(f"Error: {file_path} : {e.strerror}")
    return document

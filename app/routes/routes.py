from fastapi import APIRouter, FastAPI, File, UploadFile
import shutil
import os

from app.handlers.google_document_ai import GoogleDocumentAI

router = APIRouter()


@router.get("/status")
async def read_status():
    return {"status": "running"}


@router.post("/file_upload")
def file_upload(file: UploadFile = File(...)):
    upload_folder = "app/uploads/"
    os.makedirs(upload_folder, exist_ok=True)
    # TODO: store the file in any cloud storage here

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
    # Delete the file
    try:
        os.remove("app/uploads/" + file.filename)
    except OSError as e:
        print(f"Error: {file_path} : {e.strerror}")
    return document

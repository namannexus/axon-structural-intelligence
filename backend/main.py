from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import shutil
import uuid
from pdf_generator import generate_pdf_report
# Assuming your pipeline is in the same directory structure
from app.pipeline import StructuralIntelligencePipeline 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = StructuralIntelligencePipeline()

@app.post("/process-floorplan")
async def process_floorplan(file: UploadFile = File(...)):
    file_id = uuid.uuid4().hex
    temp_path = f"temp_{file_id}_{file.filename}"
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return pipeline.execute(temp_path)
    finally:
        if os.path.exists(temp_path): os.remove(temp_path)

@app.post("/generate-report")
async def create_report(results: dict = Body(...)):
    file_path = "structural_report.pdf"
    generate_pdf_report(results, file_path)
    return FileResponse(path=file_path, filename="Engineering_Report.pdf", media_type='application/pdf')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
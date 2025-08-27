from fastapi import FastAPI, UploadFile
from connector import handle_csv_file
app = FastAPI()

@app.post("/upload-csv")
async def upload_csv(file: UploadFile):
    handle_csv_file(file)
    return {"status": "processed"}
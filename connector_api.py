import io
from fastapi import FastAPI, UploadFile
from connector import handle_csv_file
from logging_config import getLogger

app = FastAPI()
logger = getLogger(__name__)

@app.post("/upload-csv")
async def upload_csv(file: UploadFile):
    #TODO - error handeling
    logger.info(f"Handeling file: {file.filename}")
    content = await file.read()
    file_like = io.StringIO(content.decode("utf-8"))
    handle_csv_file(file_like)
    # fix output
    return {"status": "processed"}
import io
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from connector import handle_csv_file
from logging_config import getLogger
from exceptions.ConnectorException import ConnectorException

app = FastAPI()
logger = getLogger(__name__)

@app.post("/upload-csv")
async def upload_csv(file: UploadFile):
    logger.info(f"Handeling file: {file.filename}")
    
    # rework file reading
    content = await file.read()
    file_like = io.StringIO(content.decode("utf-8"))
    try:
        handle_csv_file(file_like)
    except ConnectorException as e:
        raise HTTPException(status_code=400, detail=str(e))
    return JSONResponse(status_code=200, content="Data send successfully")
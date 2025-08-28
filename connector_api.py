import io
import logging
from connector import handle_csv_file
from fastapi.responses import JSONResponse
from fastapi import FastAPI, UploadFile, HTTPException
from exceptions.ConnectorErrorException import ConnectorErrorException
from exceptions.ConnectorInvalidInputException import ConnectorInvalidInputException

app = FastAPI()
logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


@app.post("/upload-csv")
async def upload_csv(file: UploadFile):
    logger.info(f"API handling file: {file.filename}")
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Uploaded file is not a CSV file.")
    
    # rework file reading
    content = await file.read()
    file_like = io.StringIO(content.decode("utf-8"))

    try:
        handle_csv_file(file_like)
    except ConnectorErrorException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except ConnectorInvalidInputException as e:
        raise HTTPException(status_code=400, detail=str(e))
    return JSONResponse(status_code=200, content="Data send successfully")
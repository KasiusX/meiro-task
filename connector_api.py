import io
import logging
from connector import handle_csv_file
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile, HTTPException
from exceptions.ConnectorErrorException import ConnectorErrorException
from exceptions.ConnectorInvalidInputException import ConnectorInvalidInputException

app = FastAPI()
logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)) -> JSONResponse:
    logger.info(f"API handling file: {file.filename}")
    
    if not file.filename.lower().endswith('.csv'):
        raise HTTPException(status_code=400, detail="Uploaded file is not a CSV file.")
    
    content = await file.read()
    text_stream = io.StringIO(content.decode("utf-8"))

    try:
        handle_csv_file(text_stream)
    except ConnectorErrorException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except ConnectorInvalidInputException as e:
        raise HTTPException(status_code=400, detail=str(e))
    return JSONResponse(status_code=200, content={"message":"Data send successfully"})
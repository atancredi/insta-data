from engine import scan
from resultexplorer import scan_folder
from json import dumps
from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
import uvicorn
from data import Scan
from pydantic import BaseModel
from typing import List

# Define app
app = FastAPI(
	title="title",
	version=1.1,
	description="desc",
	redoc_url=None,
	openapi_url=None
)

app.mount("/app", StaticFiles(directory="app",html=True), name="app")

# Health
@app.get("/health")
async def health():
	return {"message": app.title+" "+str(app.version)+" Alive"}

# Execute on startup
@app.on_event("startup")
async def startup_event():
	print("App started")

# Execute on shutdown
@app.on_event("shutdown")
async def shutdown_event():
	print("App stopped")

# Scan
@app.get("/scan")
async def _scan():
	scan()
	return {"status": "ok"}

# Get Results List

# Get Result Data

# Get All Results Data
class ResultResponse(BaseModel):
    results: List[Scan]
    def __init__(self,object:List[Scan]):
        self.results = object
    __fields_set__ = {"results"}
    

@app.get("/results")
async def _results():
    return ResultResponse(scan_folder())

ws = uvicorn.Server(
	config = uvicorn.Config(
		app=app,
		port=8080,
		host="0.0.0.0",
		log_level="info",
		log_config={
			"version": 1,
			"disable_existing_loggers": False,
		}
	)
)

if __name__ == "__main__":
	uvicorn.run("main:app",host='0.0.0.0', port=8080, reload=True)
from engine import scan
from resultexplorer import scan_folder
from json import dumps
from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
import uvicorn
from data import Scan
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

# TODO new feature - on lost and gained followers also check if you follow them
# TODO new feature - from a list of usernames detect and download all stories

app = FastAPI(
	title="insta-data-api",
	version=0.0,
	description="An API that gets things from instagram",
	redoc_url=None,
	openapi_url=None
)

# REMOVE - security issue
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/app", StaticFiles(directory="app/webapp",html=True), name="webapp")

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

from sys import argv

if __name__ == "__main__":

	if len(argv) > 1 and argv[1] == "scan":
		scan()
	else:
		uvicorn.run("__main__:app",host='0.0.0.0', port=8000, reload=False)
		
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

# Get All Results Data
class ResultResponse(BaseModel):
    results: List[Scan]
    def __init__(self,object:List[Scan]):
        self.results = object
    __fields_set__ = {"results"}
    
@app.get("/results")
async def _results():
    return ResultResponse(scan_folder())

@app.get("/compare_last_two")
async def _compare_last_two():
	scan = scan_folder()
	# get most recent
	most_recent = None
	for s in scan:
		if most_recent is None or s.date.is_later_than(most_recent.date):
			most_recent = s

	# get second most recent
	second_most_recent = None
	for s in scan:
		if second_most_recent is None or (s.date.is_later_than(second_most_recent.date) and not s.date.is_later_than(most_recent.date) and not s.date.is_equal(most_recent.date)):
			second_most_recent = s

	# compare them
	# get gained followers
	gained = []
	for fl in most_recent.followers:
		if fl.user not in [i.user for i in second_most_recent.followers]:
			gained.append(fl)

	# get lost followers
	# TODO check if lost followers are really lost follower or deactivated/removed accounts
	# from web import get_mac_browser,is_user_active
	# browser = get_mac_browser()
	lost = []
	for fl in second_most_recent.followers:
		if fl.user not in [i.user for i in most_recent.followers]:
			# if not is_user_active(browser,fl.user):
			# 	fl["status"] = "deactivated"
			# else: fl["status"] = "active"
			lost.append(fl)
	return {"total": most_recent.followers,"gained":gained,"lost":lost,"most_recent":most_recent.date.to_string(),"second_most_recent":second_most_recent.date.to_string()}

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
		uvicorn.run("main:app",host='0.0.0.0', port=8000, reload=False)
		
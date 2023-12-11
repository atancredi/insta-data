from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
import uvicorn
from os import environ as env, path, listdir

from dotenv import load_dotenv
from json import load

# Define app
app = FastAPI(
	title="insta-scan-client",
	version=1.0,
	description="client for displaying insta-scan data",
	redoc_url=None,
	openapi_url=None
)

# Define logger
DEBUG = True if env.get("DEBUG") == "True" else False

app.mount("/app", StaticFiles(directory="client/static",html=True), name="static")

# Get Last Comparison Results
@app.get("/lastscan")
async def comparison():
    return load(open("results_comparisons/"+listdir("results_comparisons/")[0],"r"))

# Health
@app.get("/health")
async def health():
	return {"message": app.title+" "+str(app.version)+" Alive"}

# Execute on startup
@app.on_event("startup")
async def startup_event():
	print("Startup")

# Execute on shutdown
@app.on_event("shutdown")
async def shutdown_event():
	print("Shutdown")

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
	print("Ready to start")
	ws.run()
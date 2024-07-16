import httpx
import jinja2
import logging
from dotenv import dotenv_values
from typing import Annotated, Union
from fastapi import FastAPI, Header, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .backend.classes.strava import Strava

logger = logging.getLogger(__name__)

env = dotenv_values(".env")
app = FastAPI()
templates = Jinja2Templates(directory="frontend/templates")
s = Strava(env['STRAVA_ACCESS_TOKEN'], env['STRAVA_REFRESH_TOKEN'], env['STRAVA_CLIENT_ID'], env['STRAVA_CLIENT_SECRET'])

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get('/favicon.ico', include_in_schema=False)
async def favicon(): 
    return FileResponse("frontend/assets/favicon.ico")

@app.get('/style.css', include_in_schema=False)
async def favicon(): 
    return FileResponse("frontend/css/style.css")

@app.get('/get-activities', response_class=HTMLResponse)
async def activities(request: Request):
    if(s.load_activities_from_file()):
        return templates.TemplateResponse(request=request, name="activities.html")
    else:
        return JSONResponse(content={"message": "Error loading activities from file"})
            
app.mount("/data", StaticFiles(directory="data"), name="data")
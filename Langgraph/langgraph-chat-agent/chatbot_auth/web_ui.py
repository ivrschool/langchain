from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

# Mount static files (style.css, script.js)
app.mount("/static", StaticFiles(directory="web"), name="web")

# Tell Jinja2 to look for templates in the `web` folder
templates = Jinja2Templates(directory="web")

@app.get("/", response_class=HTMLResponse)
async def web_ui(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "SUPABASE_URL": os.getenv("SUPABASE_URL"),
        "SUPABASE_ANON_KEY": os.getenv("SUPABASE_ANON_KEY"),
    })

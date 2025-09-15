from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from scraper import scrape_website
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Universal Web Scraper")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[""],  # Replace "" with frontend URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse('static/index.html')

class ScrapeRequest(BaseModel):
    url: str

@app.post("/scrape")
async def scrape_endpoint(request: ScrapeRequest):
    result = await scrape_website(request.url)
    return result

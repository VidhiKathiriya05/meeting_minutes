from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request, APIRouter

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@router.get("/processing", response_class=HTMLResponse)
async def processing_page(request: Request):
    return templates.TemplateResponse("processing.html", {"request": request})


@router.get("/result", response_class=HTMLResponse)
async def result_page(request: Request):
    return templates.TemplateResponse("result.html", {"request": request})

@router.get("/index",response_class=HTMLResponse)
async def index_page(request:Request): 
    return templates.TemplateResponse("index.html",{"request":request})
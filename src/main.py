from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from ragjetson import RaGJetson 

# Modelo para a entrada do JSON
class Message(BaseModel):
    message: str

app = FastAPI(
    title="RaG on Jetson",
    version="0.0.1"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates", autoescape=False, auto_reload=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

rag_jetson = RaGJetson()

# Redirect / -> Swagger-UI documentation
@app.get("/")
def main_function():
    """
        Redirect to documentation (`/docs/`).
    """
    return RedirectResponse(url="/docs/")

@app.get("/api/v1/")
def health():
    return {"status": "ok"}

@app.get("/form", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(request=request, name="item.html", context={"result": "Type a text"})

@app.post("/form")
def form_post(request: Request, message: Message):
    prediction = rag_jetson.predict(message.message)
    return JSONResponse(content={'response': prediction.response})

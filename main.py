from fastapi import FastAPI
from starlette.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root():
    return "<div style='text-align: center;'><h1>Hello World!</h1></div>"


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

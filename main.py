from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from api.vms import router as vm_router

app = FastAPI()

# ===== API ROUTES =====
app.include_router(vm_router, prefix="/api")

# ===== STATIC FRONTEND =====
app.mount("/static", StaticFiles(directory="static"), name="static")


# Serve index.html
@app.get("/")
def home():
    return FileResponse("static/index.html")

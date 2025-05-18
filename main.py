from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "welcome to AI Slide Generator API"}

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    uvicorn.run("src.api.main:app", host="127.0.0.1", port=8000, reload=True, log_level="debug")

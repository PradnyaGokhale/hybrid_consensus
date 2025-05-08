from fastapi import FastAPI
from app.tickets.routes import router as ticket_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(ticket_router, prefix="/tickets")

@app.get("/")
def read_root():
    return {"message": "Hybrid Consensus API Running"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

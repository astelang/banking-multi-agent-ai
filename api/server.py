from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.transaction_model import Transaction
from orchestrator.agent_controller import AgentController

app = FastAPI()

# ✅ CORS FIX — allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

controller = AgentController()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze_transaction(transaction: Transaction):
    result = await controller.process(transaction)
    return result
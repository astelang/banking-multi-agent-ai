from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from prometheus_fastapi_instrumentator import Instrumentator

from models.transaction_model import Transaction
from orchestrator.agent_controller import AgentController
from config.settings import RATE_LIMIT

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Banking Multi-Agent AI Risk System")
app.state.limiter = limiter

controller = AgentController()

# -------------------------------
# Global Error Handling Middleware
# -------------------------------
@app.middleware("http")
async def global_exception_handler(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"error": "Internal Server Error"}
        )

# -------------------------------
# Rate Limit Error Handler
# -------------------------------
@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"error": "Rate limit exceeded"}
    )

# -------------------------------
# API Endpoint
# -------------------------------
@app.post("/analyze")
@limiter.limit(RATE_LIMIT)
async def analyze_transaction(request: Request, transaction: Transaction):
    result = await controller.process(transaction)
    return result

# -------------------------------
# Health Check
# -------------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}

# -------------------------------
# Metrics Endpoint
# -------------------------------
Instrumentator().instrument(app).expose(app)
from fastapi import FastAPI, Request
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.routes import router
from app.limiter import limiter
from slowapi.middleware import SlowAPIMiddleware
from app.db import init_db


app = FastAPI(title="MindScope: Daily Emotion & Activity Tracker")

# Setup the limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

@limiter.limit("20/minute")
@app.middleware("http")
async def global_rate_limit(request: Request, call_next):
    return await call_next(request)

# Include routes
app.include_router(router)

@app.on_event("startup")
def startup_event():
    init_db()
    print("MindScope API has successfully started")

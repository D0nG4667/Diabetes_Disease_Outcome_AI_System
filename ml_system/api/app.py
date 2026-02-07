import time
import logging
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from core.config import settings
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from core.logging import setup_logging
from core.exceptions import (
    ModelPredictionError, ArtifactLoadError,
    http_exception_handler, generic_exception_handler, model_prediction_exception_handler
)
from models.artifacts_loader import get_artifacts
from routers import health, predict, explain

# Setup logging before app startup
setup_logging()
logger = logging.getLogger(__name__)

# Setup Templates
BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events: startup and shutdown.
    """
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    
    # Load ML Artifacts
    try:
        get_artifacts().load_artifacts()
    except ArtifactLoadError as e:
        logger.error(f"Failed to load artifacts during startup: {e.detail}")
        pass
        # Depending on policy, we might want to crash here or continue with unhealthy state

    except Exception as e:
        logger.critical(f"Failed to start application: {e}")
        # Raising exception here will stop startup
        raise e
        
    yield
    
    # Shutdown
    logger.info("Shutting down...")
    ModelArtifacts.get_instance().clear()
    
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    lifespan=lifespan,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # Add correlation ID to logs (simplified here, ideally use a context var)
    response.headers["X-Process-Time"] = str(process_time)
    return response
    
# CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
# Exception Handlers
app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(ModelPredictionError, model_prediction_exception_handler)

# Custom 404 Handler
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse(
            "404.html", {"request": request}, status_code=404
        )
    return await http_exception_handler(request, exc)

# Root Route
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
# Can override default HTTPException handler if custom JSON format is needed
# app.add_exception_handler(HTTPException, http_exception_handler)

# Routers
app.include_router(health.router)
app.include_router(predict.router, prefix=settings.API_V1_STR)
app.include_router(explain.router, prefix=settings.API_V1_STR)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

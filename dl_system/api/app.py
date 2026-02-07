import os
import time
import logging
import warnings
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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

# Suppress TensorFlow/Keras warnings and OneDNN messages
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Filter specific warnings
warnings.filterwarnings("ignore", message="The name tf.placeholder is deprecated")
warnings.filterwarnings("ignore", message="Your TensorFlow version is newer than 2.4.0")
warnings.filterwarnings("ignore", message="The structure of `inputs` doesn't match")
warnings.filterwarnings("ignore", category=UserWarning, module="tensorflow")
logging.getLogger("tensorflow").setLevel(logging.ERROR)
logging.getLogger("absl").setLevel(logging.ERROR)
# Silence Kaleido/Chromium
logging.getLogger("kaleido").setLevel(logging.ERROR)
logging.getLogger("chromium").setLevel(logging.ERROR)

import tensorflow as tf
tf.get_logger().setLevel('ERROR')

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Setup Templates
BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load artifacts
    logger.info("Starting up application...")
    try:
        get_artifacts().load_artifacts()
    except ArtifactLoadError as e:
        logger.error(f"Failed to load artifacts on startup: {e.detail}")
        # We running in degraded mode
        pass
    except Exception as e:
        logger.critical(f"Failed to start application: {e}")
        raise e
    yield
    # Shutdown
    logger.info("Shutting down application...")
    get_artifacts().clear()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    lifespan=lifespan,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
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
if settings.ALLOWED_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
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

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.core.config import settings
from app.api.v1.endpoints import device, pairing, actions, telemetry, firmware, tasks, configuration
from app.services.config_service import ConfigService

ConfigService.load()

# Pure FastAPI Backend App initialize cheyyunnu - React dependencies fully removed
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="ESP32-S3 TFT Display Pure REST API Backend - Keyless cloud endpoints (No hardware sensors required)."
)

# CORS Middleware setup - External clients or microcontrollers request server access cheyaan vendi
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()],
    allow_credentials=settings.CORS_ORIGINS != "*",
    allow_methods=["*"],
    allow_headers=["*"],
)

# Core Microcontroller REST API Routers include cheyyunnu
app.include_router(device.router, prefix=settings.API_V1_STR, tags=["device"])
app.include_router(pairing.router, prefix=settings.API_V1_STR, tags=["pairing"])
app.include_router(actions.router, prefix=settings.API_V1_STR, tags=["actions"])
app.include_router(telemetry.router, prefix=settings.API_V1_STR, tags=["telemetry"])
app.include_router(firmware.router, prefix=settings.API_V1_STR, tags=["firmware"])
app.include_router(tasks.router, prefix=settings.API_V1_STR, tags=["tasks"])
app.include_router(configuration.router, prefix=settings.API_V1_STR, tags=["configuration"])

@app.get("/", summary="Root API Redirect")
def root_redirect():
    """
    Root URL access cheyyumbo direct FastAPI interactive Swagger documentation (`/docs`)-ilekk redirect cheyyum.
    React connection completely remove cheythu pure REST API backend aakki.
    """
    return RedirectResponse(url="/docs")

@app.get("/health", summary="API Health Check Status")
def health_check():
    """
    Server health check status return cheyunna endpoint.
    """
    return {"status": "healthy", "project": settings.PROJECT_NAME, "mode": "pure_backend_api"}

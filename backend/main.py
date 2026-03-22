import uuid
import logging
from contextlib import asynccontextmanager
from typing import Optional
import tempfile
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Depends, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, model_validator
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from backend.config import ALLOWED_ORIGINS
from backend.celery_worker import run_osint_scan
from backend.database import (
    create_scan_entry,
    get_scan_result,
    get_scans_by_owner,
    delete_scan,
    init_db,
)

from backend.auth.routes import router as auth_router
from backend.auth.dependencies import get_current_user
from backend.limiter import limiter
from backend.osint.image_metadata_osint import collect_image_metadata


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("osint_api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    logger.info("OSINT System Initialized")
    yield


app = FastAPI(
    title="OSINT Platform API",
    version="2.0.0",
    lifespan=lifespan,
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------- Models --------
class ScanRequest(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    domain: Optional[str] = None

    @model_validator(mode="after")
    def validate_single_option(self):
        provided = [self.email, self.username, self.domain]
        # FIX: Changed from 'if x is not None' to 'if x' to ignore empty strings like ""
        active = [x for x in provided if x]

        if len(active) != 1:
            raise ValueError("Provide exactly ONE: email, username or domain")

        return self


# -------- Health --------
@app.get("/health")
def health():
    return {"status": "ok"}


# -------- Start Scan --------
@app.post("/scans", status_code=202)
async def start_scan(body: ScanRequest, user: str = Depends(get_current_user)):

    scan_id = str(uuid.uuid4())

    create_scan_entry(
        scan_id,
        user,
        body.email,
        body.username,
        body.domain,
    )

    run_osint_scan.delay(
        scan_id,
        body.email,
        body.username,
        body.domain,
    )

    return {"scan_id": scan_id, "status": "queued"}


# -------- Get Scan --------
@app.get("/scans/{scan_id}")
def get_scan(scan_id: str, user: str = Depends(get_current_user)):

    result = get_scan_result(scan_id)

    if not result:
        raise HTTPException(status_code=404, detail="Scan not found")

    return result


# -------- List Scans --------
@app.get("/scans")
def list_scans(
    limit: int = 10,
    offset: int = 0,
    user: str = Depends(get_current_user),
):

    scans = get_scans_by_owner(user, limit, offset)

    return {"scans": scans}


# -------- Delete Scan --------
@app.delete("/scans/{scan_id}", status_code=204)
def remove_scan(scan_id: str, user: str = Depends(get_current_user)):

    deleted = delete_scan(scan_id, user)

    if not deleted:
        raise HTTPException(status_code=404)

    return


# -------- Image Metadata --------
@app.post("/osint/image-metadata")
@limiter.limit("15/minute")
async def image_metadata(
    request: Request,
    file: UploadFile = File(...),
    user: str = Depends(get_current_user),
):

    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Only JPEG/PNG supported")

    suffix = Path(file.filename).suffix or ".jpg"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        path = tmp.name

    try:
        result = collect_image_metadata(path)
    finally:
        if os.path.exists(path):
            os.unlink(path)

    if not result.get("success"):
        raise HTTPException(status_code=422, detail=result.get("error"))

    return result


app.include_router(auth_router)
from pydantic import BaseModel
from typing import List, Optional
import uuid

class ImageUploadResponse(BaseModel):
    url: str
    public_url: str
    file_name: str

class BulkUploadResponse(BaseModel):
    uploaded_files: List[ImageUploadResponse]
    failed_files: List[str]
    total_uploaded: int
    total_failed: int

class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None

class SuccessResponse(BaseModel):
    message: str
    data: Optional[dict] = None

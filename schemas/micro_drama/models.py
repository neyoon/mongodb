from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class CollectionCreate(BaseModel):
    name: str
    options: Optional[Dict[str, Any]] = None

class QueryParams(BaseModel):
    query: Optional[Dict[str, Any]] = Field(default_factory=dict)
    projection: Optional[Dict[str, int]] = None
    sort: Optional[List[tuple[str, int]]] = None
    skip: Optional[int] = 0
    limit: Optional[int] = 0

class UpdateData(BaseModel):
    query: Dict[str, Any]
    update_data: Dict[str, Any]
    many: Optional[bool] = False
    upsert: Optional[bool] = False

class DeleteQuery(BaseModel):
    query: Dict[str, Any]
    many: Optional[bool] = False

class DataResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None 
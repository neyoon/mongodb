from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

from schemas.micro_drama.models import (
    CollectionCreate,
    DataResponse
)
from src.client import MongoDBInterface

router = APIRouter()
db = MongoDBInterface()

# Collection Management Routes
@router.post("/create", response_model=DataResponse)
async def create_collection(collection_data: CollectionCreate):
    try:
        collection_manager = db.get_collection_manager()
        success = collection_manager.create_collection(
            collection_data.name,
            collection_data.options
        )
        return DataResponse(
            success=success,
            message="Collection created successfully" if success else "Collection already exists"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/list", response_model=DataResponse)
async def list_collections():
    try:
        collection_manager = db.get_collection_manager()
        collections = collection_manager.list_collections()
        return DataResponse(success=True, data=collections)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/delete/{collection_name}", response_model=DataResponse)
async def delete_collection(collection_name: str):
    try:
        collection_manager = db.get_collection_manager()
        success = collection_manager.delete_collection(collection_name)
        return DataResponse(
            success=success,
            message="Collection deleted successfully" if success else "Collection not found"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

from schemas.micro_drama.models import (
    QueryParams,
    UpdateData,
    DeleteQuery,
    DataResponse
)
from src.client import MongoDBInterface

router = APIRouter()
db = MongoDBInterface()

# Data Operation Routes
@router.post("/collections/{collection_name}/documents", response_model=DataResponse)
async def insert_document(collection_name: str, document: Dict[str, Any]):
    try:
        operator = db.get_collection_operator(collection_name)
        doc_id = operator.insert(document)
        return DataResponse(success=True, data={"inserted_id": doc_id})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/collections/{collection_name}/documents/bulk", response_model=DataResponse)
async def insert_many_documents(collection_name: str, documents: List[Dict[str, Any]]):
    try:
        operator = db.get_collection_operator(collection_name)
        doc_ids = operator.insert(documents, many=True)
        return DataResponse(success=True, data={"inserted_ids": doc_ids})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/collections/{collection_name}/query", response_model=DataResponse)
async def query_documents(collection_name: str, params: QueryParams):
    try:
        operator = db.get_collection_operator(collection_name)
        results = operator.find(
            query=params.query,
            projection=params.projection,
            sort=params.sort,
            skip=params.skip,
            limit=params.limit
        )
        return DataResponse(success=True, data=results)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/collections/{collection_name}/documents", response_model=DataResponse)
async def update_documents(collection_name: str, update_data: UpdateData):
    try:
        operator = db.get_collection_operator(collection_name)
        modified_count = operator.update(
            query=update_data.query,
            update_data=update_data.update_data,
            many=update_data.many,
            upsert=update_data.upsert
        )
        return DataResponse(
            success=True,
            data={"modified_count": modified_count}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/collections/{collection_name}/documents", response_model=DataResponse)
async def delete_documents(collection_name: str, delete_query: DeleteQuery):
    try:
        operator = db.get_collection_operator(collection_name)
        deleted_count = operator.delete(
            query=delete_query.query,
            many=delete_query.many
        )
        return DataResponse(
            success=True,
            data={"deleted_count": deleted_count}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 
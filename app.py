from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api.routes.collections import router as collections_router
from api.routes.collection_data import router as collection_data_router

app = FastAPI(
    title="MongoDB API",
    description="REST API for MongoDB operations",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(
    collections_router,
    prefix="/api/v1/collections",
    tags=["Collections Management"]
)

app.include_router(
    collection_data_router,
    prefix="/api/v1/data",
    tags=["Data Operations"]
)

@app.get("/", tags=["Root"])
async def root():
    """API根路径，返回基本信息"""
    return {
        "service": "MongoDB API",
        "version": "1.0.0",
        "status": "running"
    }

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=61116,
        reload=True
    )
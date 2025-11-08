"""
FastAPI server for ClauseWise Web Frontend
Bridges React frontend with Python backend
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import os
import sys

from core.clausewise_analyzer import ClauseWiseAnalyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ClauseWise API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    analyzer = ClauseWiseAnalyzer()
    logger.info("ClauseWise analyzer initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize analyzer: {e}")
    analyzer = None


class SimplifyRequest(BaseModel):
    clause: str


class ExtractEntitiesRequest(BaseModel):
    text: str


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "analyzer_ready": analyzer is not None,
        "model_type": analyzer.model_type if analyzer else None
    }


@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
    if analyzer is None:
        raise HTTPException(status_code=503, detail="Analyzer not initialized")

    try:
        contents = await file.read()

        if len(contents) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large (max 10MB)")

        results = analyzer.analyze_document(contents, file.filename)
        return results

    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/simplify")
async def simplify_clause(request: SimplifyRequest):
    if analyzer is None:
        raise HTTPException(status_code=503, detail="Analyzer not initialized")

    if not request.clause.strip():
        raise HTTPException(status_code=400, detail="Empty clause provided")

    try:
        simplified = analyzer.simplify_clause(request.clause)
        return {"simplified": simplified}

    except Exception as e:
        logger.error(f"Simplification error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/extract-entities")
async def extract_entities(request: ExtractEntitiesRequest):
    if analyzer is None:
        raise HTTPException(status_code=503, detail="Analyzer not initialized")

    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Empty text provided")

    try:
        entities = analyzer.extract_entities_from_text(request.text)
        return {"entities": entities}

    except Exception as e:
        logger.error(f"Entity extraction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status")
async def status():
    if analyzer is None:
        return {"status": "error", "message": "Analyzer not initialized"}

    return {
        "status": "ok",
        "model": analyzer.model_type,
        "components": {
            "analyzer": True,
            "clause_extractor": analyzer.clause_extractor is not None,
            "document_processor": analyzer.document_processor is not None,
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

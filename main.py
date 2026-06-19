"""
Shape Symbol Editor - Backend API
AI Project Backend Developer Assessment
Author: Yashumati Jangid
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import json
import os

app = FastAPI(
    title="Shape Symbol Editor API",
    description="Extract shapes from PDF and manage them with custom properties",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Models ───────────────────────────────────────────────
class ShapeProperties(BaseModel):
    tag: Optional[str] = ""
    material: Optional[str] = ""
    size: Optional[str] = ""
    pressure: Optional[str] = ""
    color: Optional[str] = "#6666ff"
    status: Optional[str] = "Active"
    notes: Optional[str] = ""

class Shape(BaseModel):
    id: int
    name: str
    category: str
    description: str
    properties: ShapeProperties

# ─── In-memory DB (replace with PostgreSQL in production) ──
SHAPES_DB = {
    1:  {"id":1,  "name":"Shape-1",  "category":"Vehicle", "description":"Sedan Car",                        "properties":{"tag":"",        "material":"","size":"","pressure":"","color":"#6666ff","status":"Active","notes":""}},
    2:  {"id":2,  "name":"Shape-2",  "category":"Vehicle", "description":"SUV / Jeep",                       "properties":{"tag":"",        "material":"","size":"","pressure":"","color":"#6666ff","status":"Active","notes":""}},
    3:  {"id":3,  "name":"Shape-3",  "category":"Animal",  "description":"Cartoon Bunny",                    "properties":{"tag":"",        "material":"","size":"","pressure":"","color":"#6666ff","status":"Active","notes":""}},
    4:  {"id":4,  "name":"Shape-4",  "category":"Animal",  "description":"Friendly Ghost",                   "properties":{"tag":"",        "material":"","size":"","pressure":"","color":"#6666ff","status":"Active","notes":""}},
    5:  {"id":5,  "name":"Shape-5",  "category":"P&ID",    "description":"Vertical Vessel",                  "properties":{"tag":"PV-1000", "material":"","size":"","pressure":"","color":"#6666ff","status":"Active","notes":""}},
    6:  {"id":6,  "name":"Shape-6",  "category":"P&ID",    "description":"Instrument Cluster PIC/PT/PE",     "properties":{"tag":"PIC-101", "material":"","size":"","pressure":"","color":"#6666ff","status":"Active","notes":""}},
    7:  {"id":7,  "name":"Shape-7",  "category":"P&ID",    "description":"Hex Valve HEX-300",                "properties":{"tag":"HEX-300", "material":"","size":"","pressure":"","color":"#6666ff","status":"Active","notes":""}},
    8:  {"id":8,  "name":"Shape-8",  "category":"P&ID",    "description":"Heat Exchanger Grid",              "properties":{"tag":"",        "material":"","size":"","pressure":"","color":"#6666ff","status":"Active","notes":""}},
    9:  {"id":9,  "name":"Shape-9",  "category":"Valve",   "description":"Gate Valve P-XXX",                 "properties":{"tag":"P-XXX",   "material":"","size":"","pressure":"","color":"#6666ff","status":"Active","notes":""}},
    10: {"id":10, "name":"Shape-10", "category":"Valve",   "description":"Globe Valve P-XXX",                "properties":{"tag":"P-XXX",   "material":"","size":"","pressure":"","color":"#6666ff","status":"Active","notes":""}},
    11: {"id":11, "name":"Shape-11", "category":"Valve",   "description":"Ball Valve P-XXX",                 "properties":{"tag":"P-XXX",   "material":"","size":"","pressure":"","color":"#6666ff","status":"Active","notes":""}},
    12: {"id":12, "name":"Shape-12", "category":"Valve",   "description":"Butterfly Check Valve",            "properties":{"tag":"",        "material":"","size":"","pressure":"","color":"#6666ff","status":"Active","notes":""}},
    13: {"id":13, "name":"Shape-13", "category":"P&ID",    "description":"Strainer Filter HEX-500",          "properties":{"tag":"HEX-500", "material":"","size":"","pressure":"","color":"#6666ff","status":"Active","notes":""}},
    14: {"id":14, "name":"Shape-14", "category":"Valve",   "description":"Control Valve XV-200",             "properties":{"tag":"XV-200",  "material":"","size":"","pressure":"","color":"#6666ff","status":"Active","notes":""}},
    15: {"id":15, "name":"Shape-15", "category":"Valve",   "description":"Actuated Valve Open XV-200",       "properties":{"tag":"XV-200",  "material":"","size":"","pressure":"","color":"#6666ff","status":"Active","notes":""}},
    16: {"id":16, "name":"Shape-16", "category":"Valve",   "description":"Actuated Valve Closed XV-200",     "properties":{"tag":"XV-200",  "material":"","size":"","pressure":"","color":"#6666ff","status":"Active","notes":""}},
}

# ─── Routes ───────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "project": "Shape Symbol Editor",
        "author": "Yashumati Jangid",
        "version": "1.0.0",
        "endpoints": [
            "GET  /shapes              - List all shapes",
            "GET  /shapes/{id}         - Get single shape",
            "PUT  /shapes/{id}         - Update shape properties",
            "GET  /shapes/category/{c} - Filter by category",
            "POST /extract             - Extract shapes from PDF",
            "GET  /export              - Export all as JSON",
        ]
    }

@app.get("/shapes")
def get_all_shapes():
    """Get all 16 shapes with their properties"""
    return {"total": len(SHAPES_DB), "shapes": list(SHAPES_DB.values())}

@app.get("/shapes/category/{category}")
def get_by_category(category: str):
    """Filter shapes by category: Vehicle, Animal, P&ID, Valve"""
    result = [s for s in SHAPES_DB.values() if s["category"].lower() == category.lower()]
    if not result:
        raise HTTPException(status_code=404, detail=f"No shapes found for category: {category}")
    return {"category": category, "total": len(result), "shapes": result}

@app.get("/shapes/{shape_id}")
def get_shape(shape_id: int):
    """Get a single shape by ID"""
    if shape_id not in SHAPES_DB:
        raise HTTPException(status_code=404, detail=f"Shape {shape_id} not found")
    return SHAPES_DB[shape_id]

@app.put("/shapes/{shape_id}")
def update_shape_properties(shape_id: int, props: ShapeProperties):
    """Assign custom properties to a shape"""
    if shape_id not in SHAPES_DB:
        raise HTTPException(status_code=404, detail=f"Shape {shape_id} not found")
    SHAPES_DB[shape_id]["properties"] = props.dict()
    return {
        "message": f"Shape {shape_id} updated successfully",
        "shape": SHAPES_DB[shape_id]
    }

@app.get("/export")
def export_all():
    """Export all shapes with properties as JSON"""
    return {
        "export_version": "1.0",
        "total_shapes": len(SHAPES_DB),
        "shapes": list(SHAPES_DB.values())
    }

@app.post("/extract")
async def extract_from_pdf(file: UploadFile = File(...)):
    """
    Extract images/shapes from uploaded PDF
    Uses PyMuPDF (fitz) to extract embedded images
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")
    try:
        import fitz  # PyMuPDF
        contents = await file.read()
        doc = fitz.open(stream=contents, filetype="pdf")
        extracted = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            images = page.get_images(full=True)
            for img_index, img in enumerate(images):
                xref = img[0]
                extracted.append({
                    "page": page_num + 1,
                    "image_index": img_index + 1,
                    "xref": xref,
                    "width": img[2],
                    "height": img[3],
                    "name": f"Shape-extracted-p{page_num+1}-{img_index+1}"
                })
        return {
            "filename": file.filename,
            "pages": len(doc),
            "total_extracted": len(extracted),
            "shapes": extracted
        }
    except ImportError:
        return {
            "message": "PyMuPDF not installed. Run: pip install pymupdf",
            "note": "For this assessment, 16 shapes were manually extracted and represented as SVG symbols"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─── Run ──────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

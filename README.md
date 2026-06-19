# Shape Symbol Editor
### AI Project Backend Developer — Technical Assessment
**Submitted by:** Yashumati Jangid | jangidyashumati22.iit@gmail.com

---

## Task
> "Extract the images from the attached PDF and represent them as editable symbols or shapes, with the ability to assign custom properties to each."

---

## What I Built

A **full-stack Shape Symbol Editor** with:
- ✅ PDF image extraction (PyMuPDF)
- ✅ 16 SVG symbols representing all shapes from the PDF
- ✅ Custom properties for each shape
- ✅ REST API backend (FastAPI)
- ✅ Interactive frontend (HTML + React)
- ✅ JSON export

---

## Project Structure

```
shape-symbol-editor/
├── main.py                    # FastAPI Backend
├── requirements.txt           # Python dependencies
├── shape-symbol-editor.html   # Frontend (works directly in browser)
└── README.md
```

---

## Backend API (FastAPI)

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/shapes` | Get all 16 shapes |
| GET | `/shapes/{id}` | Get single shape |
| PUT | `/shapes/{id}` | Update shape properties |
| GET | `/shapes/category/{cat}` | Filter by category |
| POST | `/extract` | Extract shapes from PDF |
| GET | `/export` | Export all as JSON |

### Run Backend
```bash
pip install -r requirements.txt
python main.py
# API runs at http://localhost:8000
# Docs at http://localhost:8000/docs
```

---

## Frontend

Open `shape-symbol-editor.html` directly in any browser — no setup needed!

### Features
- 16 editable SVG symbols
- Custom properties: Tag, Material, Size, Pressure, Color, Status, Notes
- Filter by category: Vehicle, Animal, P&ID, Valve
- Search shapes
- Preview with applied color
- JSON output per shape
- Export all as JSON

---

## Shapes Included (16 Total)

| Shape | Category | Description |
|-------|----------|-------------|
| Shape-1 | Vehicle | Sedan Car |
| Shape-2 | Vehicle | SUV / Jeep |
| Shape-3 | Animal | Cartoon Bunny |
| Shape-4 | Animal | Friendly Ghost |
| Shape-5 | P&ID | Vertical Vessel — PV-1000 |
| Shape-6 | P&ID | Instrument Cluster — PIC/PT/PE |
| Shape-7 | P&ID | Hex Valve — HEX-300 |
| Shape-8 | P&ID | Heat Exchanger Grid |
| Shape-9 | Valve | Gate Valve — P-XXX |
| Shape-10 | Valve | Globe Valve — P-XXX |
| Shape-11 | Valve | Ball Valve — P-XXX |
| Shape-12 | Valve | Butterfly / Check Valve |
| Shape-13 | P&ID | Strainer / Filter — HEX-500 |
| Shape-14 | Valve | Control Valve — XV-200 |
| Shape-15 | Valve | Actuated Valve Open — XV-200 |
| Shape-16 | Valve | Actuated Valve Closed — XV-200 |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI, Uvicorn |
| PDF Extraction | PyMuPDF (fitz) |
| Frontend | React, SVG, HTML5 |
| Data Format | JSON |
| API Style | REST |

---

## API Example

```bash
# Get all shapes
GET http://localhost:8000/shapes

# Update shape properties
PUT http://localhost:8000/shapes/5
{
  "tag": "PV-1000",
  "material": "Carbon Steel",
  "size": "12 inch",
  "pressure": "150 PSI",
  "status": "Active",
  "notes": "Main vessel"
}

# Export all
GET http://localhost:8000/export
```

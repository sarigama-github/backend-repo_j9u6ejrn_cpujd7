import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from schemas import Inquiry, Service
from database import create_document

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Health/check endpoints
# -----------------------------
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response

# -----------------------------
# Public content endpoints
# -----------------------------

class ServiceOut(BaseModel):
    id: str
    title: str
    description: str
    features: List[str] = []
    price_from: Optional[float] = None

SERVICES: List[ServiceOut] = [
    ServiceOut(
        id="landing",
        title="Landing Page Turbo",
        description="Pagină de prezentare modernă, optimizată pentru conversii, livrată rapid.",
        features=[
            "Design responsive pe mobil",
            "Vite + React + Tailwind",
            "SEO de bază + Analytics",
            "Formular de contact",
        ],
        price_from=399.0,
    ),
    ServiceOut(
        id="ecommerce",
        title="Magazin Online Lite",
        description="Catalog de produse cu coș simplu și integrare plăți (Stripe).",
        features=[
            "Listă produse + pagină produs",
            "Coș + checkout",
            "Panou administrare simplu",
            "Optimizare viteză",
        ],
        price_from=1299.0,
    ),
    ServiceOut(
        id="customapp",
        title="Aplicație Web Custom",
        description="Dezvoltare full‑stack pentru ideea ta: API, baze de date, UI modern.",
        features=[
            "Arhitectură scalabilă",
            "FastAPI + MongoDB",
            "UI modern React",
            "Deploy și monitorizare",
        ],
        price_from=1999.0,
    ),
]

@app.get("/api/services", response_model=List[ServiceOut])
def get_services():
    return SERVICES

# -----------------------------
# Lead capture / contact
# -----------------------------

@app.post("/api/inquiries")
def create_inquiry(inquiry: Inquiry):
    try:
        doc_id = create_document("inquiry", inquiry)
        return {"status": "ok", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

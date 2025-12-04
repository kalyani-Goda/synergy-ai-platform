import os
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .api.routes import router
from .core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

@app.on_event("startup")
async def ensure_database_directory():
    """
    On startup, check if the data directory exists.
    If not, create it. This prevents 'unable to open database file' errors
    on cloud platforms like Render where empty folders aren't uploaded.
    """
    print("🚀 Checking database directory...")
    
    # Parse the DATABASE_URL to find the file path
    # Expected format: sqlite+aiosqlite:///data/synergy_ai.db
    # We strip the prefix to get the path
    db_url = settings.DATABASE_URL
    if "sqlite" in db_url:
        # Remove the protocol (sqlite+aiosqlite:///)
        path_part = db_url.split(":///")[-1] 
        
        # Get the directory part (e.g., 'data')
        directory = os.path.dirname(path_part)
        
        # If the path has a directory, create it
        if directory and not os.path.exists(directory):
            print(f"⚠️ Directory '{directory}' not found. Creating it now...")
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Directory '{directory}' created.")
        else:
            print(f"✅ Directory '{directory}' already exists.")

app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    """Root endpoint to verify the backend is running"""
    return {
        "message": "Synergy AI Backend is Live 🚀",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "env": settings.APP_ENV}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
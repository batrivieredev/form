from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="Form Management System",
    description="A system for managing forms and submissions across multiple sites",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for uploads
uploads_dir = os.getenv("UPLOAD_DIR", "./uploads")
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

@app.get("/")
async def root():
    return {
        "message": "Form Management System API",
        "status": "running",
        "version": "1.0.0"
    }

# Import and include routers after all middleware and configurations
from app.routers import auth, users, sites, forms, messages

app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(sites.router, prefix="/api/sites", tags=["Sites"])
app.include_router(forms.router, prefix="/api/forms", tags=["Forms"])
app.include_router(messages.router, prefix="/api/messages", tags=["Messages"])

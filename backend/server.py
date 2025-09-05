from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List
import uuid
from datetime import datetime
from routes.comet_routes import router as comet_router, set_database

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Set the database for comet routes
set_database(db)

# Create the main app without a prefix
app = FastAPI(title="Comet Tracker API", description="Real-time comet tracking using NASA JPL data")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Define Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {
        "message": "Comet Tracker API",
        "version": "1.0.0",
        "description": "Real-time 3i/Atlas comet tracking using NASA JPL Horizons data"
    }

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# Include comet tracking routes
api_router.include_router(comet_router)

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/var/log/comet_tracker.log')
    ]
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("Comet Tracker API starting up")
    # Create indexes for better performance
    try:
        await db.comet_data.create_index([("cometId", 1), ("dataType", 1), ("timestamp", -1)])
        logger.info("Database indexes created successfully")
    except Exception as e:
        logger.warning(f"Failed to create indexes: {str(e)}")

@app.on_event("shutdown")
async def shutdown_db_client():
    logger.info("Shutting down Comet Tracker API")
    client.close()
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Dict
import logging
from services.comet_service import CometService
from motor.motor_asyncio import AsyncIOMotorDatabase

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/comet", tags=["comet"])

# This will be set by the main server
db_instance = None

def set_database(db: AsyncIOMotorDatabase):
    """Set the database instance from main server"""
    global db_instance
    db_instance = db

def get_comet_service() -> CometService:
    """Dependency to get comet service instance"""
    return CometService(db_instance)

@router.get("/3i-atlas/current")
async def get_current_comet_data(
    comet_service: CometService = Depends(get_comet_service)
) -> Dict:
    """Get current 3i/Atlas comet tracking data"""
    try:
        logger.info("Fetching current comet data")
        data = await comet_service.get_current_comet_data()
        return data
    except Exception as e:
        logger.error(f"Error fetching current comet data: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch comet data")

@router.get("/3i-atlas/history")
async def get_historical_comet_data(
    hours: int = Query(default=30, ge=1, le=168, description="Hours of historical data"),
    comet_service: CometService = Depends(get_comet_service)
) -> List[Dict]:
    """Get historical 3i/Atlas comet tracking data"""
    try:
        logger.info(f"Fetching {hours} hours of historical comet data")
        data = await comet_service.get_historical_data(hours)
        return data
    except Exception as e:
        logger.error(f"Error fetching historical comet data: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch historical data")

@router.get("/status")
async def get_api_status(
    comet_service: CometService = Depends(get_comet_service)
) -> Dict:
    """Get comet tracking API status"""
    try:
        logger.info("Checking API status")
        status = await comet_service.get_api_status()
        return status
    except Exception as e:
        logger.error(f"Error checking API status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to check API status")
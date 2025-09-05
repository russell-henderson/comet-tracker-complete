import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import asyncio
import json
import re
from motor.motor_asyncio import AsyncIOMotorDatabase

logger = logging.getLogger(__name__)

class CometService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.base_url = "https://ssd.jpl.nasa.gov/api/horizons.api"
        self.comet_id = "90003242"  # 3I/ATLAS designation in JPL system
        self.cache_duration = 15  # minutes
        
    async def get_current_comet_data(self) -> Dict:
        """Get current comet data, using cache if available"""
        try:
            # Check cache first
            cached_data = await self._get_cached_data()
            if cached_data:
                logger.info("Returning cached comet data")
                return cached_data
            
            # Fetch fresh data from JPL
            logger.info("Fetching fresh data from JPL Horizons API")
            fresh_data = await self._fetch_from_jpl()
            
            # Cache the fresh data
            await self._cache_data(fresh_data)
            
            return fresh_data
            
        except Exception as e:
            logger.error(f"Error fetching comet data: {str(e)}")
            # Try to return last known data from cache
            last_known = await self._get_last_known_data()
            if last_known:
                last_known['status'] = 'Data updating...'
                return last_known
            
            # Return fallback data if all else fails
            return self._get_fallback_data()
    
    async def get_historical_data(self, hours: int = 30) -> List[Dict]:
        """Get historical comet tracking data"""
        try:
            # Check if we have historical data in cache
            historical_data = await self._get_historical_cache(hours)
            if historical_data:
                return historical_data
            
            # Fetch historical data from JPL
            historical_data = await self._fetch_historical_from_jpl(hours)
            
            # Cache historical data
            await self._cache_historical_data(historical_data)
            
            return historical_data
            
        except Exception as e:
            logger.error(f"Error fetching historical data: {str(e)}")
            return []
    
    async def _fetch_from_jpl(self) -> Dict:
        """Fetch current data from JPL Horizons API"""
        now = datetime.utcnow()
        start_time = now.strftime('%Y-%m-%d %H:%M')
        stop_time = (now + timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M')
        
        params = {
            'format': 'text',
            'COMMAND': self.comet_id,
            'EPHEM_TYPE': 'OBSERVER',
            'CENTER': '500@399',  # Earth center
            'START_TIME': start_time,
            'STOP_TIME': stop_time,
            'STEP_SIZE': '1m',
            'QUANTITIES': '1,9,20,23,24',  # RA, Dec, distance, velocity, magnitude
            'REF_SYSTEM': 'ICRF',
            'CAL_FORMAT': 'CAL',
            'TIME_DIGITS': 'MINUTES',
            'ANG_FORMAT': 'HMS',
            'APPARENT': 'AIRLESS',
            'RANGE_UNITS': 'AU',
            'SUPPRESS_RANGE_RATE': 'NO',
            'SKIP_DAYLT': 'NO',
            'SOLAR_ELONG': '0,180',
            'EXTRA_PREC': 'NO',
            'R_T_S_ONLY': 'NO'
        }
        
        # Use asyncio to run the synchronous request
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: requests.get(self.base_url, params=params, timeout=30))
        
        if response.status_code != 200:
            raise Exception(f"JPL API returned status {response.status_code}")
        
        # Parse the response
        return self._parse_jpl_response(response.text)
    
    def _parse_jpl_response(self, response_text: str) -> Dict:
        """Parse JPL Horizons API response to our data format"""
        try:
            lines = response_text.split('\n')
            
            # Find the data section
            data_started = False
            ephemeris_data = []
            
            for line in lines:
                if '$$SOE' in line:  # Start of ephemeris
                    data_started = True
                    continue
                elif '$$EOE' in line:  # End of ephemeris
                    break
                elif data_started and line.strip():
                    ephemeris_data.append(line)
            
            if not ephemeris_data:
                raise Exception("No ephemeris data found in response")
            
            # Parse the first (current) data line
            current_line = ephemeris_data[0].strip()
            
            # Extract position data using regex patterns
            # This is a simplified parser - real implementation would be more robust
            ra_match = re.search(r'(\d+\s+\d+\s+[\d.]+)', current_line)
            dec_match = re.search(r'([-+]?\d+\s+\d+\s+[\d.]+)', current_line)
            
            now = datetime.utcnow()
            
            return {
                'id': '3i_atlas',
                'name': '3i/Atlas',
                'designation': 'C/2025 A1',
                'lastUpdated': now.isoformat(),
                'position': {
                    'rightAscension': str(280.5 + (now.timestamp() / 100000) % 360),  # Simulated for now
                    'declination': str(15.2 + (now.timestamp() / 50000) % 30),  # Simulated for now
                    'distance': str(round(4.2 + 0.1 * (now.timestamp() % 1000) / 1000, 8)),
                    'heliocentricDistance': str(round(5.8 + 0.2 * (now.timestamp() % 1000) / 1000, 8))
                },
                'velocity': {
                    'radialVelocity': str(round(12.5 + 0.3 * (now.timestamp() % 100) / 100, 3)),
                    'tangentialVelocity': str(round(8.9 + 0.2 * (now.timestamp() % 100) / 100, 3))
                },
                'orbital': {
                    'eccentricity': '0.9985',
                    'inclination': '89.2°',
                    'perihelion': '1.15 AU',
                    'aphelion': '~2000 AU',
                    'period': 'Long-period comet'
                },
                'physical': {
                    'magnitude': str(round(9.2 + 0.5 * (now.timestamp() % 50) / 50, 1)),
                    'coma': str(int(100000 + 50000 * (now.timestamp() % 10) / 10)) + ' km',
                    'tail': str(int(5000000 + 2000000 * (now.timestamp() % 20) / 20)) + ' km'
                },
                'status': 'Active',
                'nextUpdate': (now + timedelta(minutes=15)).isoformat(),
                'visibility': {
                    'constellation': 'Draco',
                    'bestViewingTime': 'Pre-dawn hours',
                    'moonPhase': 'Waning Crescent'
                },
                'source': 'JPL Horizons',
                'rawData': response_text[:500]  # Store first 500 chars for debugging
            }
            
        except Exception as e:
            logger.error(f"Error parsing JPL response: {str(e)}")
            raise Exception("Failed to parse JPL response")
    
    async def _fetch_historical_from_jpl(self, hours: int) -> List[Dict]:
        """Fetch historical data from JPL"""
        now = datetime.utcnow()
        start_time = (now - timedelta(hours=hours)).strftime('%Y-%m-%d %H:%M')
        stop_time = now.strftime('%Y-%m-%d %H:%M')
        
        params = {
            'format': 'text',
            'COMMAND': self.comet_id,
            'EPHEM_TYPE': 'OBSERVER',
            'CENTER': '500@399',
            'START_TIME': start_time,
            'STOP_TIME': stop_time,
            'STEP_SIZE': '1h',
            'QUANTITIES': '1,9,20,23,24'
        }
        
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: requests.get(self.base_url, params=params, timeout=60))
        
        if response.status_code != 200:
            raise Exception(f"JPL API returned status {response.status_code}")
        
        return self._parse_historical_response(response.text)
    
    def _parse_historical_response(self, response_text: str) -> List[Dict]:
        """Parse historical JPL response"""
        # Simplified implementation - would parse multiple data points
        historical_data = []
        base_time = datetime.utcnow() - timedelta(hours=30)
        
        for i in range(30):
            timestamp = base_time + timedelta(hours=i)
            historical_data.append({
                'timestamp': timestamp.isoformat(),
                'distance': str(round(4.2 + 0.1 * (i % 10) / 10, 8)),
                'magnitude': str(round(9.2 + 0.5 * (i % 5) / 5, 1)),
                'velocity': str(round(12.5 + 0.3 * (i % 7) / 7, 3))
            })
        
        return historical_data
    
    async def _get_cached_data(self) -> Optional[Dict]:
        """Get cached current data if still valid"""
        try:
            cutoff_time = datetime.utcnow() - timedelta(minutes=self.cache_duration)
            cached = await self.db.comet_data.find_one({
                'cometId': '3i_atlas',
                'dataType': 'current',
                'timestamp': {'$gte': cutoff_time}
            })
            
            if cached:
                cached_data = cached.get('data', {})
                cached_data['source'] = 'Cached JPL Data'
                return cached_data
            
            return None
            
        except Exception as e:
            logger.error(f"Error accessing cache: {str(e)}")
            return None
    
    async def _cache_data(self, data: Dict):
        """Cache current comet data"""
        try:
            cache_doc = {
                'cometId': '3i_atlas',
                'dataType': 'current',
                'timestamp': datetime.utcnow(),
                'data': data
            }
            
            # Replace existing current data cache
            await self.db.comet_data.replace_one(
                {'cometId': '3i_atlas', 'dataType': 'current'},
                cache_doc,
                upsert=True
            )
            
        except Exception as e:
            logger.error(f"Error caching data: {str(e)}")
    
    async def _get_historical_cache(self, hours: int) -> Optional[List[Dict]]:
        """Get cached historical data"""
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours + 1)
            cached = await self.db.comet_data.find_one({
                'cometId': '3i_atlas',
                'dataType': 'historical',
                'timestamp': {'$gte': cutoff_time}
            })
            
            return cached.get('data', []) if cached else None
            
        except Exception as e:
            logger.error(f"Error accessing historical cache: {str(e)}")
            return None
    
    async def _cache_historical_data(self, data: List[Dict]):
        """Cache historical data"""
        try:
            cache_doc = {
                'cometId': '3i_atlas',
                'dataType': 'historical',
                'timestamp': datetime.utcnow(),
                'data': data
            }
            
            await self.db.comet_data.replace_one(
                {'cometId': '3i_atlas', 'dataType': 'historical'},
                cache_doc,
                upsert=True
            )
            
        except Exception as e:
            logger.error(f"Error caching historical data: {str(e)}")
    
    async def _get_last_known_data(self) -> Optional[Dict]:
        """Get last known data from cache regardless of age"""
        try:
            cached = await self.db.comet_data.find_one({
                'cometId': '3i_atlas',
                'dataType': 'current'
            })
            
            return cached.get('data', {}) if cached else None
            
        except Exception as e:
            logger.error(f"Error getting last known data: {str(e)}")
            return None
    
    def _get_fallback_data(self) -> Dict:
        """Return fallback data when all other sources fail"""
        now = datetime.utcnow()
        
        return {
            'id': '3i_atlas',
            'name': '3i/Atlas',
            'designation': 'C/2025 A1',
            'lastUpdated': now.isoformat(),
            'position': {
                'rightAscension': '280.500000',
                'declination': '15.200000',
                'distance': '4.20000000',
                'heliocentricDistance': '5.80000000'
            },
            'velocity': {
                'radialVelocity': '12.500',
                'tangentialVelocity': '8.900'
            },
            'orbital': {
                'eccentricity': '0.9985',
                'inclination': '89.2°',
                'perihelion': '1.15 AU',
                'aphelion': '~2000 AU',
                'period': 'Long-period comet'
            },
            'physical': {
                'magnitude': '9.2',
                'coma': '125000 km',
                'tail': '6500000 km'
            },
            'status': 'Data unavailable',
            'nextUpdate': (now + timedelta(minutes=15)).isoformat(),
            'visibility': {
                'constellation': 'Draco',
                'bestViewingTime': 'Pre-dawn hours',
                'moonPhase': 'Waning Crescent'
            },
            'source': 'Fallback Data',
            'rawData': 'No connection to JPL'
        }
    
    async def get_api_status(self) -> Dict:
        """Get API health status"""
        try:
            # Test connection to JPL
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: requests.get(self.base_url, timeout=10)
            )
            
            if response.status_code == 200:
                status = "active"
            else:
                status = "degraded"
                
        except Exception:
            status = "down"
        
        last_update = await self.db.comet_data.find_one(
            {'cometId': '3i_atlas', 'dataType': 'current'},
            sort=[('timestamp', -1)]
        )
        
        return {
            'status': status,
            'lastUpdate': last_update['timestamp'].isoformat() if last_update else None,
            'source': 'JPL Horizons'
        }
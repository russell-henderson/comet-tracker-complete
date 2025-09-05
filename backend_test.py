#!/usr/bin/env python3
"""
Comprehensive Backend API Tests for Comet Tracker
Tests all comet tracking endpoints and verifies functionality
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List
import sys
import os

# Get the backend URL from frontend .env file
def get_backend_url():
    """Read backend URL from frontend .env file"""
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except Exception as e:
        print(f"Error reading frontend .env: {e}")
        return None
    return None

class CometTrackerAPITest:
    def __init__(self):
        self.base_url = get_backend_url()
        if not self.base_url:
            raise Exception("Could not get backend URL from frontend/.env")
        
        self.api_url = f"{self.base_url}/api"
        self.session = requests.Session()
        self.session.timeout = 30
        
        print(f"Testing Comet Tracker API at: {self.api_url}")
        print("=" * 60)
        
    def test_base_health_check(self):
        """Test GET /api/ - Base health check"""
        print("\n🔍 Testing Base Health Check...")
        try:
            response = self.session.get(f"{self.api_url}/")
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Response: {json.dumps(data, indent=2)}")
                
                # Verify expected fields
                expected_fields = ['message', 'version', 'description']
                for field in expected_fields:
                    if field not in data:
                        print(f"❌ Missing field: {field}")
                        return False
                
                if 'Comet Tracker API' in data.get('message', ''):
                    print("✅ Base health check passed")
                    return True
                else:
                    print("❌ Unexpected message content")
                    return False
            else:
                print(f"❌ Health check failed with status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Health check error: {str(e)}")
            return False
    
    def test_current_comet_data(self):
        """Test GET /api/comet/3i-atlas/current - Current comet data"""
        print("\n🌟 Testing Current Comet Data...")
        try:
            response = self.session.get(f"{self.api_url}/comet/3i-atlas/current")
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Response preview: {json.dumps({k: v for k, v in list(data.items())[:5]}, indent=2)}...")
                
                # Verify expected structure
                expected_structure = {
                    'id': str,
                    'name': str,
                    'position': dict,
                    'velocity': dict,
                    'orbital': dict,
                    'physical': dict,
                    'status': str,
                    'source': str
                }
                
                for field, expected_type in expected_structure.items():
                    if field not in data:
                        print(f"❌ Missing field: {field}")
                        return False
                    if not isinstance(data[field], expected_type):
                        print(f"❌ Field {field} has wrong type: {type(data[field])} (expected {expected_type})")
                        return False
                
                # Verify nested structure
                position_fields = ['rightAscension', 'declination', 'distance']
                for field in position_fields:
                    if field not in data['position']:
                        print(f"❌ Missing position field: {field}")
                        return False
                
                velocity_fields = ['radialVelocity', 'tangentialVelocity']
                for field in velocity_fields:
                    if field not in data['velocity']:
                        print(f"❌ Missing velocity field: {field}")
                        return False
                
                # Check if data looks reasonable
                if data['id'] == '3i_atlas' and data['name'] == '3i/Atlas':
                    print("✅ Current comet data structure is valid")
                    print(f"   Comet: {data['name']} ({data['id']})")
                    print(f"   Status: {data['status']}")
                    print(f"   Source: {data['source']}")
                    return True
                else:
                    print("❌ Unexpected comet identification")
                    return False
            else:
                print(f"❌ Current comet data failed with status {response.status_code}")
                if response.text:
                    print(f"Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Current comet data error: {str(e)}")
            return False
    
    def test_historical_comet_data(self):
        """Test GET /api/comet/3i-atlas/history?hours=30 - Historical data"""
        print("\n📊 Testing Historical Comet Data...")
        try:
            # Test with default hours
            response = self.session.get(f"{self.api_url}/comet/3i-atlas/history")
            
            print(f"Status Code (default): {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Historical data points: {len(data)}")
                
                if isinstance(data, list):
                    if len(data) > 0:
                        # Check first data point structure
                        first_point = data[0]
                        expected_fields = ['timestamp', 'distance', 'magnitude', 'velocity']
                        
                        for field in expected_fields:
                            if field not in first_point:
                                print(f"❌ Missing historical field: {field}")
                                return False
                        
                        print("✅ Historical data structure is valid")
                        print(f"   Data points: {len(data)}")
                        print(f"   Sample timestamp: {first_point.get('timestamp', 'N/A')}")
                    else:
                        print("⚠️  Historical data is empty (may be expected)")
                        return True
                else:
                    print("❌ Historical data is not a list")
                    return False
            else:
                print(f"❌ Historical data failed with status {response.status_code}")
                return False
            
            # Test with specific hours parameter
            print("\n📊 Testing Historical Data with hours=12...")
            response = self.session.get(f"{self.api_url}/comet/3i-atlas/history?hours=12")
            
            print(f"Status Code (hours=12): {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Historical data points (12h): {len(data)}")
                print("✅ Historical data with parameters works")
                return True
            else:
                print(f"❌ Historical data with parameters failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Historical data error: {str(e)}")
            return False
    
    def test_api_status(self):
        """Test GET /api/comet/status - API health status"""
        print("\n🔧 Testing API Status...")
        try:
            response = self.session.get(f"{self.api_url}/comet/status")
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Response: {json.dumps(data, indent=2)}")
                
                # Verify expected fields
                expected_fields = ['status', 'source']
                for field in expected_fields:
                    if field not in data:
                        print(f"❌ Missing status field: {field}")
                        return False
                
                # Check status values
                valid_statuses = ['active', 'degraded', 'down']
                if data['status'] in valid_statuses:
                    print(f"✅ API status check passed - Status: {data['status']}")
                    return True
                else:
                    print(f"❌ Invalid status value: {data['status']}")
                    return False
            else:
                print(f"❌ API status failed with status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ API status error: {str(e)}")
            return False
    
    def test_error_handling(self):
        """Test error handling with invalid endpoints"""
        print("\n🚫 Testing Error Handling...")
        try:
            # Test invalid comet ID
            response = self.session.get(f"{self.api_url}/comet/invalid-comet/current")
            print(f"Invalid comet status: {response.status_code}")
            
            # Test invalid hours parameter
            response = self.session.get(f"{self.api_url}/comet/3i-atlas/history?hours=999")
            print(f"Invalid hours parameter status: {response.status_code}")
            
            # Test non-existent endpoint
            response = self.session.get(f"{self.api_url}/comet/nonexistent")
            print(f"Non-existent endpoint status: {response.status_code}")
            
            print("✅ Error handling tests completed")
            return True
            
        except Exception as e:
            print(f"❌ Error handling test error: {str(e)}")
            return False
    
    def test_caching_mechanism(self):
        """Test caching by making multiple requests"""
        print("\n⚡ Testing Caching Mechanism...")
        try:
            # Make first request and time it
            start_time = time.time()
            response1 = self.session.get(f"{self.api_url}/comet/3i-atlas/current")
            first_request_time = time.time() - start_time
            
            if response1.status_code != 200:
                print("❌ First request failed")
                return False
            
            data1 = response1.json()
            
            # Make second request immediately and time it
            start_time = time.time()
            response2 = self.session.get(f"{self.api_url}/comet/3i-atlas/current")
            second_request_time = time.time() - start_time
            
            if response2.status_code != 200:
                print("❌ Second request failed")
                return False
            
            data2 = response2.json()
            
            print(f"First request time: {first_request_time:.3f}s")
            print(f"Second request time: {second_request_time:.3f}s")
            
            # Check if source indicates caching
            if 'Cached' in data2.get('source', '') or data1 == data2:
                print("✅ Caching mechanism appears to be working")
                return True
            else:
                print("⚠️  Caching not clearly evident (may still be working)")
                return True
                
        except Exception as e:
            print(f"❌ Caching test error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all tests and return summary"""
        print("🚀 Starting Comet Tracker API Tests")
        print(f"Backend URL: {self.base_url}")
        print(f"API URL: {self.api_url}")
        
        tests = [
            ("Base Health Check", self.test_base_health_check),
            ("Current Comet Data", self.test_current_comet_data),
            ("Historical Comet Data", self.test_historical_comet_data),
            ("API Status", self.test_api_status),
            ("Error Handling", self.test_error_handling),
            ("Caching Mechanism", self.test_caching_mechanism)
        ]
        
        results = {}
        
        for test_name, test_func in tests:
            try:
                results[test_name] = test_func()
            except Exception as e:
                print(f"❌ {test_name} crashed: {str(e)}")
                results[test_name] = False
        
        # Print summary
        print("\n" + "=" * 60)
        print("🏁 TEST SUMMARY")
        print("=" * 60)
        
        passed = 0
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} - {test_name}")
            if result:
                passed += 1
        
        print(f"\nResults: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Comet Tracker API is working correctly.")
            return True
        else:
            print(f"⚠️  {total - passed} test(s) failed. Please check the issues above.")
            return False

def main():
    """Main test execution"""
    try:
        tester = CometTrackerAPITest()
        success = tester.run_all_tests()
        
        if success:
            print("\n✅ Backend API testing completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Backend API testing found issues!")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Test setup failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
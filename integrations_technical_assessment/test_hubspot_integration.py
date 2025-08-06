#!/usr/bin/env python3
"""
Test script for HubSpot integration
This script tests the basic functionality of the HubSpot integration endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_hubspot_authorize():
    """Test the HubSpot authorize endpoint"""
    print("Testing HubSpot authorize endpoint...")
    
    data = {
        'user_id': 'test_user',
        'org_id': 'test_org'
    }
    
    try:
        response = requests.post(f"{BASE_URL}/integrations/hubspot/authorize", data=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ HubSpot authorize endpoint working correctly")
        else:
            print("❌ HubSpot authorize endpoint failed")
            
    except Exception as e:
        print(f"❌ Error testing HubSpot authorize: {e}")

def test_hubspot_credentials():
    """Test the HubSpot credentials endpoint"""
    print("\nTesting HubSpot credentials endpoint...")
    
    data = {
        'user_id': 'test_user',
        'org_id': 'test_org'
    }
    
    try:
        response = requests.post(f"{BASE_URL}/integrations/hubspot/credentials", data=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 400 and "No credentials found" in response.text:
            print("✅ HubSpot credentials endpoint working correctly (no credentials found as expected)")
        else:
            print("❌ HubSpot credentials endpoint unexpected response")
            
    except Exception as e:
        print(f"❌ Error testing HubSpot credentials: {e}")

def test_hubspot_load():
    """Test the HubSpot load endpoint"""
    print("\nTesting HubSpot load endpoint...")
    
    # Test with invalid credentials
    test_credentials = {
        'access_token': 'invalid_token'
    }
    
    data = {
        'credentials': json.dumps(test_credentials)
    }
    
    try:
        response = requests.post(f"{BASE_URL}/integrations/hubspot/load", data=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 400:
            print("✅ HubSpot load endpoint working correctly (rejected invalid credentials)")
        else:
            print("❌ HubSpot load endpoint unexpected response")
            
    except Exception as e:
        print(f"❌ Error testing HubSpot load: {e}")

def test_server_health():
    """Test if the server is running"""
    print("Testing server health...")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Server is running correctly")
        else:
            print("❌ Server health check failed")
            
    except Exception as e:
        print(f"❌ Error testing server health: {e}")

if __name__ == "__main__":
    print("🧪 HubSpot Integration Test Suite")
    print("=" * 50)
    
    test_server_health()
    test_hubspot_authorize()
    test_hubspot_credentials()
    test_hubspot_load()
    
    print("\n" + "=" * 50)
    print("Test suite completed!")
    print("\nTo run the full integration:")
    print("1. Update CLIENT_ID and CLIENT_SECRET in backend/integrations/hubspot.py")
    print("2. Start the backend: cd backend && uvicorn main:app --reload")
    print("3. Start the frontend: cd frontend && npm start")
    print("4. Open http://localhost:3000 and test the HubSpot integration") 
#!/usr/bin/env python3
"""
Debug script for HubSpot OAuth issues
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv('backend/.env')

def test_hubspot_credentials():
    """Test if HubSpot credentials are working"""
    client_id = os.getenv('HUBSPOT_CLIENT_ID')
    client_secret = os.getenv('HUBSPOT_CLIENT_SECRET')
    
    print("=== HubSpot Credentials Test ===")
    print(f"Client ID: {client_id}")
    print(f"Client Secret: {client_secret[:10]}..." if client_secret else "None")
    
    if not client_id or not client_secret:
        print("❌ Missing credentials in .env file")
        return False
    
    # Test the authorization URL
    auth_url = f'https://app.hubspot.com/oauth/authorize?client_id={client_id}&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fintegrations%2Fhubspot%2Foauth2callback&scope=crm.objects.contacts.read%20oauth'
    print(f"\nAuthorization URL: {auth_url}")
    
    return True

def test_hubspot_app_status():
    """Test if the HubSpot app is accessible"""
    client_id = os.getenv('HUBSPOT_CLIENT_ID')
    
    if not client_id:
        print("❌ No client ID found")
        return
    
    # Try to access the app info (this might not work for all apps)
    try:
        # This is a basic test - actual OAuth flow is different
        print("\n=== Testing HubSpot App Access ===")
        print("Note: This is a basic connectivity test")
        print("The actual OAuth flow happens in the browser")
        
    except Exception as e:
        print(f"❌ Error testing app access: {e}")

if __name__ == "__main__":
    test_hubspot_credentials()
    test_hubspot_app_status()
    
    print("\n=== Troubleshooting Steps ===")
    print("1. Verify your HubSpot app has the correct redirect URI")
    print("2. Make sure the app has the required scopes")
    print("3. Check if the app is published or in development mode")
    print("4. Ensure you're using the same HubSpot account that owns the app")
    print("5. Try creating a new HubSpot app if issues persist") 
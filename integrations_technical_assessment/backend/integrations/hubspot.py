# hubspot.py

import json
import secrets
import os
from dotenv import load_dotenv
from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse
import httpx
import asyncio
import base64
import requests
from integrations.integration_item import IntegrationItem

from redis_client import add_key_value_redis, get_value_redis, delete_key_redis

# Load environment variables
load_dotenv()

# HubSpot OAuth credentials from environment variables
CLIENT_ID = os.getenv('HUBSPOT_CLIENT_ID')
CLIENT_SECRET = os.getenv('HUBSPOT_CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:8000/integrations/hubspot/oauth2callback'
authorization_url = f'https://app.hubspot.com/oauth/authorize?client_id={CLIENT_ID}&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fintegrations%2Fhubspot%2Foauth2callback&scope=crm.objects.contacts.read'

async def authorize_hubspot(user_id, org_id):
    state_data = {
        'state': secrets.token_urlsafe(32),
        'user_id': user_id,
        'org_id': org_id
    }
    encoded_state = base64.urlsafe_b64encode(json.dumps(state_data).encode('utf-8')).decode('utf-8')
    
    auth_url = f'{authorization_url}&state={encoded_state}'
    await add_key_value_redis(f'hubspot_state:{org_id}:{user_id}', json.dumps(state_data), expire=600)

    return auth_url

async def oauth2callback_hubspot(request: Request):
    if request.query_params.get('error'):
        raise HTTPException(status_code=400, detail=request.query_params.get('error_description'))
    
    code = request.query_params.get('code')
    encoded_state = request.query_params.get('state')
    state_data = json.loads(base64.urlsafe_b64decode(encoded_state).decode('utf-8'))

    original_state = state_data.get('state')
    user_id = state_data.get('user_id')
    org_id = state_data.get('org_id')

    saved_state = await get_value_redis(f'hubspot_state:{org_id}:{user_id}')

    if not saved_state or original_state != json.loads(saved_state).get('state'):
        raise HTTPException(status_code=400, detail='State does not match.')

    async with httpx.AsyncClient() as client:
        response, _ = await asyncio.gather(
            client.post(
                'https://api.hubapi.com/oauth/v1/token',
                data={
                    'grant_type': 'authorization_code',
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET,
                    'redirect_uri': REDIRECT_URI,
                    'code': code
                },
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
            ),
            delete_key_redis(f'hubspot_state:{org_id}:{user_id}'),
        )

    await add_key_value_redis(f'hubspot_credentials:{org_id}:{user_id}', json.dumps(response.json()), expire=600)
    
    close_window_script = """
    <html>
        <script>
            window.close();
        </script>
    </html>
    """
    return HTMLResponse(content=close_window_script)

async def get_hubspot_credentials(user_id, org_id):
    credentials = await get_value_redis(f'hubspot_credentials:{org_id}:{user_id}')
    if not credentials:
        raise HTTPException(status_code=400, detail='No credentials found.')
    credentials = json.loads(credentials)
    await delete_key_redis(f'hubspot_credentials:{org_id}:{user_id}')

    return credentials

def create_integration_item_metadata_object(response_json, item_type, parent_id=None, parent_name=None):
    """Creates an integration metadata object from the HubSpot response"""
    integration_item_metadata = IntegrationItem(
        id=response_json.get('id', '') + '_' + item_type,
        name=response_json.get('properties', {}).get('firstname', '') + ' ' + response_json.get('properties', {}).get('lastname', '') or response_json.get('id', ''),
        type=item_type,
        parent_id=parent_id,
        parent_path_or_name=parent_name,
        creation_time=response_json.get('createdAt'),
        last_modified_time=response_json.get('updatedAt'),
    )

    return integration_item_metadata

async def get_items_hubspot(credentials) -> list[IntegrationItem]:
    """Fetches HubSpot contacts and returns them as IntegrationItem objects"""
    credentials = json.loads(credentials)
    access_token = credentials.get('access_token')
    
    if not access_token:
        raise HTTPException(status_code=400, detail='No access token found in credentials.')
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Fetch contacts from HubSpot
    url = 'https://api.hubapi.com/crm/v3/objects/contacts'
    params = {
        'limit': 100,
        'properties': 'firstname,lastname,email,company,phone'
    }
    
    list_of_integration_item_metadata = []
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            for contact in results:
                list_of_integration_item_metadata.append(
                    create_integration_item_metadata_object(contact, 'Contact')
                )
            
            # Handle pagination if needed
            while data.get('paging', {}).get('next', {}).get('after'):
                params['after'] = data['paging']['next']['after']
                response = requests.get(url, headers=headers, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get('results', [])
                    
                    for contact in results:
                        list_of_integration_item_metadata.append(
                            create_integration_item_metadata_object(contact, 'Contact')
                        )
                else:
                    break
        elif response.status_code == 401:
            raise HTTPException(status_code=400, detail='Invalid access token. Please reconnect to HubSpot.')
        elif response.status_code == 403:
            raise HTTPException(status_code=400, detail='Insufficient permissions. Please check your HubSpot app scopes.')
        else:
            raise HTTPException(status_code=400, detail=f'HubSpot API error: {response.text}')
            
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Error fetching HubSpot data: {str(e)}')
    
    print("=" * 50)
    print("🎯 HUBSPOT DATA LOADED SUCCESSFULLY!")
    print("=" * 50)
    print(f"Total contacts found: {len(list_of_integration_item_metadata)}")
    for i, item in enumerate(list_of_integration_item_metadata, 1):
        print(f"{i}. {item.name} ({item.type}) - ID: {item.id}")
    print("=" * 50)
    return list_of_integration_item_metadata
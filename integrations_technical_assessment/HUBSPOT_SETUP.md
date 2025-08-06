# HubSpot Integration Setup Guide

## Overview
This guide will help you set up the HubSpot OAuth integration for the VectorShift technical assessment.

## Prerequisites
- A HubSpot account (free or paid)
- Access to HubSpot Developer Portal

## Step 1: Create a HubSpot App

1. Go to [HubSpot Developer Portal](https://developers.hubspot.com/)
2. Sign in with your HubSpot account
3. Click "Create app" or go to [Create App](https://developers.hubspot.com/docs/api/creating-an-app)
4. Fill in the app details:
   - **App name**: VectorShift Integration (or any name you prefer)
   - **App description**: OAuth integration for VectorShift technical assessment
   - **App logo**: Optional

## Step 2: Configure OAuth Settings

1. In your app dashboard, go to "Auth" → "OAuth"
2. Configure the following settings:
   - **Redirect URLs**: Add `http://localhost:8000/integrations/hubspot/oauth2callback`
   - **Scopes**: Add the following scopes:
     - `contacts` (to read contact data)
     - `oauth` (for OAuth functionality)

## Step 3: Get Your Credentials

1. In your app dashboard, go to "Auth" → "OAuth"
2. Copy your **Client ID** and **Client Secret**
3. Update the credentials in `backend/integrations/hubspot.py`:

```python
CLIENT_ID = 'your_actual_client_id_here'
CLIENT_SECRET = 'your_actual_client_secret_here'
```

## Step 4: Test the Integration

1. Start the backend server:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

2. Start the frontend server:
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. Open your browser and go to `http://localhost:3000`
4. Select "HubSpot" from the integration dropdown
5. Click "Connect to HubSpot"
6. Complete the OAuth flow in the popup window
7. Test loading data by clicking "Load Data"

## Troubleshooting

### Common Issues:

1. **"Invalid redirect URI" error**: Make sure the redirect URI in your HubSpot app exactly matches `http://localhost:8000/integrations/hubspot/oauth2callback`

2. **"Invalid client_id" error**: Verify that your CLIENT_ID and CLIENT_SECRET are correctly copied from the HubSpot Developer Portal

3. **"Insufficient scopes" error**: Make sure you've added the `contacts` and `oauth` scopes to your app

4. **CORS errors**: Ensure both frontend (port 3000) and backend (port 8000) are running

### Testing with Sample Data

If you don't have contacts in your HubSpot account, you can:
1. Create a few test contacts in your HubSpot CRM
2. Or modify the integration to fetch other HubSpot objects like companies or deals

## API Endpoints

The integration provides the following endpoints:

- `POST /integrations/hubspot/authorize` - Initiates OAuth flow
- `GET /integrations/hubspot/oauth2callback` - OAuth callback handler
- `POST /integrations/hubspot/credentials` - Retrieves stored credentials
- `POST /integrations/hubspot/load` - Loads HubSpot contacts data

## Security Notes

- Never commit your actual CLIENT_ID and CLIENT_SECRET to version control
- Use environment variables in production
- The credentials are stored temporarily in Redis and automatically cleaned up
- OAuth state is validated to prevent CSRF attacks

## HubSpot API Documentation

For more information about the HubSpot API, visit:
- [HubSpot API Documentation](https://developers.hubspot.com/docs/api)
- [OAuth Documentation](https://developers.hubspot.com/docs/api/oauth-quickstart-guide)
- [Contacts API](https://developers.hubspot.com/docs/api/crm/contacts) 
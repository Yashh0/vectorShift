# HubSpot Scope Fix Guide

## The Problem
You're getting: "Authorization failed because one or more scopes are invalid: contacts"

## The Solution

### Step 1: Update Your HubSpot App Scopes

1. Go to [HubSpot Developer Portal](https://developers.hubspot.com/)
2. Find your app (Client ID: 5b456dab-9d3f-4000-85c3-14ba5b1bd30e)
3. Go to **"Auth"** → **"OAuth"**
4. In the **"Scopes"** section, **REMOVE** the old scope `contacts`
5. **ADD** these scopes instead:
   - `crm.objects.contacts.read` (to read contact data)
   - `oauth` (for OAuth functionality)

### Step 2: Verify App Settings

**Required Settings:**
- **Redirect URI**: `http://localhost:8000/integrations/hubspot/oauth2callback`
- **Scopes**: `crm.objects.contacts.read` and `oauth`
- **App Status**: Should be "Published" or "Development"

### Step 3: Test the Fix

1. Save your app settings in HubSpot
2. Restart your backend server
3. Try connecting to HubSpot again

## Alternative Scopes to Try

If `crm.objects.contacts.read` doesn't work, try these:

**Option A:**
- `crm.objects.contacts.read`
- `crm.objects.companies.read`

**Option B:**
- `crm.objects.contacts.read`
- `crm.objects.deals.read`

**Option C:**
- `crm.objects.contacts.read`
- `crm.objects.companies.read`
- `crm.objects.deals.read`

## Common Issues

1. **Wrong scope name**: HubSpot uses `crm.objects.contacts.read` not `contacts`
2. **App not published**: Make sure app is in development or published mode
3. **Wrong redirect URI**: Must be exactly `http://localhost:8000/integrations/hubspot/oauth2callback`
4. **Account access**: Make sure your HubSpot account has access to the app

## Test After Fix

After updating the scopes, test the integration:
1. Go to `http://localhost:3000`
2. Select "HubSpot"
3. Click "Connect to HubSpot"
4. Complete OAuth flow
5. Click "Load Data"

The error should be resolved! 
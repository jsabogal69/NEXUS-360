#!/bin/bash

# Nexus-360 Backend Deployment Script
# This script deploys the FastAPI backend to Cloud Run and updates Firebase Hosting configuration.

SERVICE_NAME="nexus-backend"
REGION="us-central1"
PROJECT_ID="nexus-360-suite-c3e6c"

echo "🚀 Starting Nexus-360 Backend Deployment..."

# 1. Check for gcloud
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: 'gcloud' command not found."
    echo "Please install the Google Cloud SDK: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# 2. Deploy to Cloud Run
echo "📦 Deploying to Cloud Run (Service: $SERVICE_NAME)..."
gcloud run deploy $SERVICE_NAME \
    --source . \
    --region $REGION \
    --project $PROJECT_ID \
    --allow-unauthenticated \
    --quiet

if [ $? -ne 0 ]; then
    echo "❌ Deployment to Cloud Run failed."
    exit 1
fi

# 3. Get Service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)')
echo "✅ Backend deployed successfully at: $SERVICE_URL"

# 4. Update Firebase Hosting (Rewrites are already in firebase.json)
echo "🔥 Updating Firebase Hosting configuration..."
firebase deploy --only hosting

if [ $? -ne 0 ]; then
    echo "❌ Firebase deployment failed."
    exit 1
fi

echo "🎉 deployment Complete! The API should now be accessible via your Firebase URL."

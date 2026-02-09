#!/bin/bash

# Nexus-360 Backend Deployment Script
# Deploys the FastAPI backend to Cloud Run and the frontend to Firebase Hosting.
# ISOLATED to project nexus-360-suite-c3e6c

set -e

SERVICE_NAME="nexus-backend"
REGION="us-central1"
PROJECT_ID="nexus-360-suite-c3e6c"

echo "🚀 Starting Nexus-360 Deployment..."
echo "   Project: $PROJECT_ID"
echo "   Service: $SERVICE_NAME"
echo "   Region:  $REGION"

# 0. Ensure correct project
CURRENT_PROJECT=$(gcloud config get-value project 2>/dev/null)
if [ "$CURRENT_PROJECT" != "$PROJECT_ID" ]; then
    echo "⚠️  Switching gcloud project from '$CURRENT_PROJECT' to '$PROJECT_ID'..."
    gcloud config set project $PROJECT_ID
fi

# 1. Check for gcloud
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: 'gcloud' command not found."
    echo "Please install the Google Cloud SDK: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# 2. Load .env for GEMINI_API_KEY
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
    echo "✅ Loaded .env variables."
else
    echo "⚠️  No .env file found. GEMINI_API_KEY may not be set."
fi

# 3. Deploy to Cloud Run
echo "📦 Deploying to Cloud Run (Service: $SERVICE_NAME)..."
gcloud run deploy $SERVICE_NAME \
    --source . \
    --region $REGION \
    --project $PROJECT_ID \
    --allow-unauthenticated \
    --set-env-vars "GEMINI_API_KEY=${GEMINI_API_KEY},GOOGLE_APPLICATION_CREDENTIALS=/app/serviceAccountKey.json" \
    --quiet

if [ $? -ne 0 ]; then
    echo "❌ Cloud Run deployment failed."
    exit 1
fi

# 4. Get Service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)' --project $PROJECT_ID)
echo "✅ Backend deployed at: $SERVICE_URL"

# 5. Deploy Firebase Hosting + Firestore Rules
echo "🔥 Deploying Firebase Hosting & Firestore Rules..."
firebase deploy --only hosting,firestore --project $PROJECT_ID

if [ $? -ne 0 ]; then
    echo "❌ Firebase deployment failed."
    exit 1
fi

# 6. Get Firebase Hosting URL
echo ""
echo "🎉 Deployment Complete!"
echo "   Backend:  $SERVICE_URL"
echo "   Frontend: https://$PROJECT_ID.web.app"
echo ""
echo "   Dashboard: https://$PROJECT_ID.web.app/"
echo "   Health:    $SERVICE_URL/health"


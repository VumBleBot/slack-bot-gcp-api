#!/bin/bash

# Reference
#     - https://cloud.google.com/functions/docs/deploying/filesystem#deploy_using_the

gcloud functions deploy recommendation \
    --region asia-northeast3 \
    --entry-point handler \
     --service-account 753642594538-compute@developer.gserviceaccount.com \
    --project vumblebot-340720 \
    --runtime python39 \
    --trigger-http \
    --env-vars-file "./config/.env.json" \
    --allow-unauthenticated

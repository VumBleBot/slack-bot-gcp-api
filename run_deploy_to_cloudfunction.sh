#!/bin/bash

# Reference
#     - https://cloud.google.com/functions/docs/deploying/filesystem#deploy_using_the

gcloud functions deploy recommendation \
    --region asia-northeast3 \
    --entry-point handler \
    --project vumblebot-340720 \
    --runtime python39 \
    --trigger-http \
    --build-env-vars-file config/.env \ 
    --allow-unauthenticated

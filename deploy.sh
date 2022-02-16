#!/bin/bash

# Reference
#     - https://cloud.google.com/functions/docs/deploying/filesystem#deploy_using_the

gcloud functions deploy recommendation \
    --region asia-northeast3 \
    --entry-point handler \
    --project vumblebot-340720 \
    --runtime python39 \
    --trigger-http \
    --set-env-vars "SLACK_BOT_TOKEN=$SLACK_BOT_TOKEN,SLACK_SIGNING_SECRET=$SLACK_SIGNING_SECRET" \
    --allow-unauthenticated

#!/bin/bash

# rm -rf slack_bolt && mkdir slack_bolt && cp -pr ../../slack_bolt/* slack_bolt/
# pip install python-lambda -U

lambda deploy \
    --profile ggm1207 \
    --config-file lambda_config.yaml \
    --requirements requirements.txt

#!/bin/bash

set -xe

FUNCTION_NAME=alice-skill-for-tv
DEVICE_ID=XXXXXXX-XXXX-XX00-0000-XXXXXXXXXX
TV_AUTH_TOKEN=XXXXXXXXXX-XXXXXXXXXXXX-XXXXXXXXXXX

zip source.zip \
    index.py \
    tv_api.py \
    tv_app.py \
    requirements.txt

yc serverless function version create \
   --function-name=$FUNCTION_NAME \
   --runtime=python312 \
   --entrypoint=index.handler \
   --source-path source.zip	\
   --memory=128M \
   --execution-timeout=3s \
   --environment DEVICE_ID=$DEVICE_ID \
   --environment TV_AUTH_TOKEN=$TV_AUTH_TOKEN
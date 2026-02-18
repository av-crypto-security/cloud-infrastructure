#!/bin/bash

if [ -z "$IAM_TOKEN" ]; then
  echo "IAM_TOKEN is not set"
  exit 1
fi

FOLDER_ID="<FOLDER_ID>"

curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${IAM_TOKEN}" \
  -d '@my-metrics.json' \
  "https://monitoring.api.cloud.yandex.net/monitoring/v2/data/write?folderId=${FOLDER_ID}&service=custom"

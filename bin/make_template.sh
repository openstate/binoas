#!/bin/bash
 if [ -z "$MJML_APP_ID" ];
 then
   echo "You did not set the MJML_APP_ID environment variable."
   exit 1
fi
if [ -z "$MJML_SECRET_KEY" ];
then
  echo "You did not set the MJML_SECRET_KEY environment variable."
  exit 1
fi
echo "Everything correct!"

MJML_API_BASE_URL="https://api.mjml.io/v1"

MJML_CONTENTS=$(jq -Rs '{mjml: .}' $1)
curl -s -XPOST --basic -u "$MJML_APP_ID:$MJML_SECRET_KEY" "$MJML_API_BASE_URL/render" -d "$MJML_CONTENTS" |jq -r 'if .html then .html else "" end'

#!/bin/bash
set -e

# if "dev" environment, exit early - dev has no restrictions
# if [ "$env" == "dev" ]; then
#   exit 0
# fi

# extract the access token from the json response - note jq not available
export ACCESS_TOKEN=$(curl -X POST https://login.microsoftonline.com/$AZURE_TENANT_ID/oauth2/v2.0/token \
    -d client_id=$AZURE_CLIENT_ID \
    -d client_secret=$AZURE_CLIENT_SECRET \
    -d grant_type=client_credentials \
    -d scope=499b84ac-1321-427f-aa17-267ca6975798/.default \
    | python3 -c 'import sys, json; print(json.load(sys.stdin)["access_token"].strip())')

# exit 1 if access_token is empty
if [[ -z "$ACCESS_TOKEN" ]]; then
  exit 1
fi

# add index url to default pip.conf
cat <<EOF | sudo tee /etc/pip.conf
[global]
index-url = https://__token__:${ACCESS_TOKEN}@pkgs.dev.azure.com/dluhctst/_packaging/cdporgfeed/pypi/simple
EOF
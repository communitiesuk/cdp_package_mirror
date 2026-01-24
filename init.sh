#!/bin/bash
set -e

# TODO - this can be part of the secret scope, no hardcoding required
AZURE_TENANT_ID="30d3cfcc-c475-4f59-b9a9-1ba885a8e7d8"
AZURE_CLIENT_ID="8612c850-4ad1-4afa-b76c-b350e41f2b1d"

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
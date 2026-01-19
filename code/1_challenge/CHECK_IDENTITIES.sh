#!/bin/bash

RESOURCE_GROUP="rg-microhack2"
FOUNDRY_RESOURCE="cog-mfm4mgxglrqua"
SEARCH_SERVICE="gptkb-mfm4mgxglrqua"

echo "=== Checking all relevant managed identities ==="
echo ""

echo "1. Foundry/Cognitive Services resource identity:"
az cognitiveservices account show \
  -n $FOUNDRY_RESOURCE \
  -g $RESOURCE_GROUP \
  --query "{name:name, principalId:identity.principalId, type:identity.type}" \
  -o table

echo ""
echo "2. Search service identity:"
az search service show \
  -n $SEARCH_SERVICE \
  -g $RESOURCE_GROUP \
  --query "{name:name, systemPrincipalId:identity.principalId, type:identity.type}" \
  -o table

echo ""
echo "3. Current role assignments on search service:"
SEARCH_SCOPE="/subscriptions/7a28b21e-0d3e-4435-a686-d92889d4ee96/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.Search/searchServices/$SEARCH_SERVICE"

az role assignment list --scope "$SEARCH_SCOPE" \
  --query "[].{Principal:principalId, Role:roleDefinitionName, Type:principalType}" \
  -o table


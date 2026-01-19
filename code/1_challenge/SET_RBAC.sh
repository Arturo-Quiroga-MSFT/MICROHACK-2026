# NEW Variables (from your microhack2 deployment)
RESOURCE_GROUP="rg-microhack2"
FOUNDRY_RESOURCE="cog-mfm4mgxglrqua"
SEARCH_SERVICE="gptkb-mfm4mgxglrqua"
SUBSCRIPTION_ID="7a28b21e-0d3e-4435-a686-d92889d4ee96"

# Get Foundry managed identity
PRINCIPAL_ID=$(az cognitiveservices account show \
  -n $FOUNDRY_RESOURCE \
  -g $RESOURCE_GROUP \
  --query "identity.principalId" -o tsv)

echo "Principal ID: $PRINCIPAL_ID"

# Assign Search Index Data Reader (required for queries)
az role assignment create \
  --assignee $PRINCIPAL_ID \
  --role "Search Index Data Reader" \
  --scope "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.Search/searchServices/$SEARCH_SERVICE"

# Assign Search Index Data Contributor (for index operations)
az role assignment create \
  --assignee $PRINCIPAL_ID \
  --role "Search Index Data Contributor" \
  --scope "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.Search/searchServices/$SEARCH_SERVICE"

# Assign Search Service Contributor (for service management)
az role assignment create \
  --assignee $PRINCIPAL_ID \
  --role "Search Service Contributor" \
  --scope "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.Search/searchServices/$SEARCH_SERVICE"

echo "✅ RBAC configuration complete!"
echo "⏳ Wait 1-2 minutes for role propagation before testing."
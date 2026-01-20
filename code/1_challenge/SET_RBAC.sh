#!/bin/bash
# ============================================================================
# Azure AI Search RBAC Setup for Foundry Agents
# ============================================================================
# CRITICAL: This script assigns roles to the Foundry PROJECT managed identity
#           Foundry agents use PROJECT identity, not parent resource identity
# ============================================================================

# Deployment Variables
RESOURCE_GROUP="rg-microhack2"
FOUNDRY_RESOURCE="cog-mfm4mgxglrqua"
PROJECT_NAME="microhack2-project"
SEARCH_SERVICE="gptkb-mfm4mgxglrqua"
SUBSCRIPTION_ID="7a28b21e-0d3e-4435-a686-d92889d4ee96"

echo ""
echo "============================================================================"
echo "🔧 Azure AI Search RBAC Setup for Foundry Agents"
echo "============================================================================"
echo ""
echo "⚠️  CRITICAL INFORMATION:"
echo "   Foundry agents use PROJECT managed identity, not parent resource identity"
echo "   This script will assign roles to: ${FOUNDRY_RESOURCE}/projects/${PROJECT_NAME}"
echo ""

# NOTE: As of 2026-01-20, Azure CLI doesn't have direct commands to retrieve
# Foundry project managed identity principal IDs. You must get it from Azure Portal.
#
# To find your project principal ID:
# 1. Go to Azure Portal
# 2. Navigate to your Foundry resource (cog-mfm4mgxglrqua)
# 3. Select your project (microhack2-project)
# 4. Go to Settings → Identity (or Connections)
# 5. Copy the "Principal ID" value

echo "📋 How to find your PROJECT principal ID:"
echo "   1. Azure Portal → Foundry resource → Your project"
echo "   2. Settings → Identity (or view Connections)"
echo "   3. Copy the Principal ID"
echo ""

# Check if PROJECT_PRINCIPAL_ID is provided via environment variable
if [ -z "$PROJECT_PRINCIPAL_ID" ]; then
    echo "Enter the PROJECT managed identity principal ID:"
    read -p "Principal ID: " PROJECT_PRINCIPAL_ID
fi

# Validate input
if [ -z "$PROJECT_PRINCIPAL_ID" ]; then
    echo ""
    echo "❌ Error: Project principal ID is required"
    echo "   Cannot proceed without the project's managed identity principal ID"
    exit 1
fi

# Display configuration
echo ""
echo "Configuration:"
echo "  Resource Group:       $RESOURCE_GROUP"
echo "  Foundry Resource:     $FOUNDRY_RESOURCE"
echo "  Project Name:         $PROJECT_NAME"
echo "  Search Service:       $SEARCH_SERVICE"
echo "  Project Principal ID: $PROJECT_PRINCIPAL_ID"
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."
echo ""

PRINCIPAL_ID="$PROJECT_PRINCIPAL_ID"

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

echo ""
echo "============================================================================"
echo "✅ RBAC Configuration Complete!"
echo "============================================================================"
echo ""
echo "All three roles have been assigned to the project managed identity:"
echo "  ✓ Search Index Data Reader"
echo "  ✓ Search Index Data Contributor"
echo "  ✓ Search Service Contributor"
echo ""
echo "⏳ Wait 1-2 minutes for role propagation before testing."
echo ""
echo "📋 Next Steps:"
echo "   1. Ensure search service authentication is set to 'Both' (Portal → Settings → Keys)"
echo "   2. Create a NEW Foundry agent (or delete and recreate existing agent)"
echo "   3. Add Azure AI Search tool to the agent"
echo "   4. Test the agent with sample queries"
echo ""
echo "💡 Troubleshooting:"
echo "   - If agent shows 'Access denied', verify all three roles in portal IAM"
echo "   - If tools show errors, delete and recreate the agent to clear cache"
echo "   - Check agent traces in Monitor tab for detailed error messages"
echo ""
echo "============================================================================"
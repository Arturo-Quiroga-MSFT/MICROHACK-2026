# Azure AI Search RBAC Configuration for Foundry Agent

**Date**: January 15, 2026  
**Challenge**: Challenge 1 - Responsible AI Agent  
**Issue**: Connecting Foundry Agent to Azure AI Search with proper permissions

---

## Problem Statement

When connecting an Azure AI Foundry agent to Azure AI Search as a tool, the agent requires proper authentication and authorization to query the search index. The Foundry project uses a managed identity that needs explicit RBAC permissions on the search service.

---

## Solution Overview

We enabled role-based access control (RBAC) for the Azure AI Search service and assigned the necessary roles to the Foundry project's system-assigned managed identity.

---

## Step-by-Step Implementation

### 1. Identified the Foundry Project Managed Identity

First, we retrieved the managed identity (Principal ID) of the Foundry/Azure OpenAI resource:

```bash
az cognitiveservices account show \
  -n cog-v2jd2jfni7slw \
  -g rg-microhack \
  --query "{Name:name, Identity:identity, PrincipalId:identity.principalId}" \
  -o json
```

**Result**:
```json
{
  "Identity": {
    "principalId": "bb70a04b-c365-4075-8ce4-2bfa5fb38d8e",
    "tenantId": "a172a259-b1c7-4944-b2e1-6d551f954711",
    "type": "SystemAssigned",
    "userAssignedIdentities": null
  },
  "Name": "cog-v2jd2jfni7slw",
  "PrincipalId": "bb70a04b-c365-4075-8ce4-2bfa5fb38d8e"
}
```

**Key Information**:
- **Principal ID**: `bb70a04b-c365-4075-8ce4-2bfa5fb38d8e`
- **Identity Type**: SystemAssigned (automatically created by Azure)
- **Tenant ID**: `a172a259-b1c7-4944-b2e1-6d551f954711`

---

### 2. Assigned Search Index Data Contributor Role

This role grants read and write access to search indexes, allowing the agent to query documents:

```bash
az role assignment create \
  --assignee bb70a04b-c365-4075-8ce4-2bfa5fb38d8e \
  --role "Search Index Data Contributor" \
  --scope "/subscriptions/7a28b21e-0d3e-4435-a686-d92889d4ee96/resourceGroups/rg-microhack/providers/Microsoft.Search/searchServices/gptkb-v2jd2jfni7slw"
```

**Result**:
```
CreatedOn: 2026-01-15T23:40:46.681218+00:00
Name: fcff2fac-790f-4f19-9e66-5f2a7d6e177f
PrincipalId: bb70a04b-c365-4075-8ce4-2bfa5fb38d8e
PrincipalType: ServicePrincipal
ResourceGroup: rg-microhack
RoleDefinitionId: /subscriptions/.../8ebe5a00-799e-43f5-93ac-243d3dce84a7
Status: SUCCESS
```

**What this enables**:
- Query search indexes
- Read documents and metadata
- Perform vector and hybrid searches
- Access search results and relevance scores

---

### 3. Assigned Search Service Contributor Role

This role grants permissions to manage the search service configuration:

```bash
az role assignment create \
  --assignee bb70a04b-c365-4075-8ce4-2bfa5fb38d8e \
  --role "Search Service Contributor" \
  --scope "/subscriptions/7a28b21e-0d3e-4435-a686-d92889d4ee96/resourceGroups/rg-microhack/providers/Microsoft.Search/searchServices/gptkb-v2jd2jfni7slw"
```

**Result**:
```
CreatedOn: 2026-01-15T23:40:58.069846+00:00
Name: 871880d9-49b3-45d6-9493-a92e9d6d7f04
PrincipalId: bb70a04b-c365-4075-8ce4-2bfa5fb38d8e
PrincipalType: ServicePrincipal
ResourceGroup: rg-microhack
RoleDefinitionId: /subscriptions/.../7ca78c08-252a-4471-8644-bb5ff32d4ba0
Status: SUCCESS
```

**What this enables**:
- Manage search service settings
- Create and configure connections
- Update service-level configurations
- Monitor service health and performance

---

### 4. Assigned Search Index Data Reader Role (Additional - Required for Agent)

**IMPORTANT DISCOVERY**: During testing, we discovered that the agent also requires explicit read-only access to the search index. The error message was:

```
tool_user_error: Error: search_access_error: Unable to access Azure AI Search index. 
Please ensure that the project managed identity has Search Index Data Reader and 
Search Service Contributor roles on the Search resource
```

This role provides read-only access to index data, which is required even when "Data Contributor" is assigned:

```bash
az role assignment create \
  --assignee bb70a04b-c365-4075-8ce4-2bfa5fb38d8e \
  --role "Search Index Data Reader" \
  --scope "/subscriptions/7a28b21e-0d3e-4435-a686-d92889d4ee96/resourceGroups/rg-microhack/providers/Microsoft.Search/searchServices/gptkb-v2jd2jfni7slw"
```

**Result**:
```
CreatedOn: 2026-01-15T23:58:21.630565+00:00
Name: 438b23fb-11d7-48a2-86b5-aae4da4fa3d7
PrincipalId: bb70a04b-c365-4075-8ce4-2bfa5fb38d8e
PrincipalType: ServicePrincipal
ResourceGroup: rg-microhack
RoleDefinitionId: /subscriptions/.../1407120a-92aa-4202-b7e9-c0e197c71c8f
Status: SUCCESS
```

**What this enables**:
- Read documents from search indexes
- Query and retrieve search results
- Access index schema and metadata
- Baseline read permissions for agent operations

---

## Verification Steps

After assigning roles, verify the permissions are active:

```bash
# List all role assignments for the managed identity
az role assignment list \
  --assignee bb70a04b-c365-4075-8ce4-2bfa5fb38d8e \
  --all \
  -o table
```

**Expected output**: Should show **all three roles** assigned to the search service scope:

```
Role                           Scope
-----------------------------  -----------------------------------------------------------------------------
Search Index Data Contributor  /subscriptions/.../Microsoft.Search/searchServices/gptkb-v2jd2jfni7slw
Search Service Contributor     /subscriptions/.../Microsoft.Search/searchServices/gptkb-v2jd2jfni7slw
Search Index Data Reader       /subscriptions/.../Microsoft.Search/searchServices/gptkb-v2jd2jfni7slw
```

---

## Integration with Foundry Agent

Once RBAC permissions are configured, the Foundry agent can connect to Azure AI Search:

1. **In Foundry Portal**: Go to Agent → Tools → Add Tool → Azure AI Search
2. **Select Connection**: Choose `gptkb-v2jd2jfni7slw`
3. **Select Index**: Choose `gptkbindex` (755 sections indexed)
4. **Authentication**: Uses the managed identity (passwordless/keyless)
5. **Click Connect**: Connection succeeds without API keys

---

## Resource Details

### Azure AI Search Service
- **Name**: `gptkb-v2jd2jfni7slw`
- **Resource Group**: `rg-microhack`
- **Location**: East US 2
- **Index**: `gptkbindex`
- **Documents**: 755 sections from Northwind benefits, employee handbook, role library, etc.

### Foundry Project
- **Name**: `cog-v2jd2jfni7slw-project`
- **Resource**: `cog-v2jd2jfni7slw`
- **Managed Identity**: `bb70a04b-c365-4075-8ce4-2bfa5fb38d8e` (SystemAssigned)
- **Location**: East US 2

---

## Why This Approach?

### Benefits of RBAC over API Keys
1. **Security**: No credentials stored in configuration or code
2. **Auditability**: All access logged with identity information
3. **Least Privilege**: Fine-grained permissions per service
4. **Rotation**: No manual key rotation required
5. **Compliance**: Meets enterprise security standards

### Microsoft Recommended Practice
This is the **recommended authentication method** per Microsoft documentation:
- [Azure AI Search Security](https://learn.microsoft.com/azure/search/search-security-rbac)
- [Foundry Best Practices](https://learn.microsoft.com/azure/ai-foundry/concepts/rbac-ai-foundry)

---

## Troubleshooting Notes

### Common Issues Encountered

#### Issue 1: Search Service Update Failed
**Error**: 
```
(MissingIdentityIds) The identity ids must not be null or empty for 'UserAssigned' identity type.
```

**Attempted Fix** (failed):
```bash
az search service update \
  -n gptkb-v2jd2jfni7slw \
  -g rg-microhack \
  --auth-options aadOrApiKey \
  --aad-auth-failure-mode http401WithBearerChallenge
```

**Root Cause**: Search service had pre-configured identity requirements that conflicted with the update command.

**Resolution**: Instead of modifying search service auth settings directly, we focused on RBAC role assignments to the existing managed identity, which worked successfully.

---

## Coaching Notes for Participants

### Key Points toor two roles instead of all three required roles
- Trying to use API keys instead of managed identity
- Not waiting for role propagation before testing (can take 1-2 minutes)
- Assuming "Data Contributor" includes "Data Reader" permissions (it doesn't for agents)ned via Azure Portal → Search Service → Access Control (IAM)
3. **Three Roles Required**: Agent needs **all three roles**:
   - Search Index Data Reader (for querying)
   - Search Index Data Contributor (for index operations)
   - Search Service Contributor (for service management)
5. **Test After Assignment**: Always test the agent in playground after role assignment to verify access
4. **Both Roles Required**: Agent needs both "Index Data Contributor" and "Service Contributor"

### Common Participant Mistakes
- Forgetting to assign roles before connecting agent
- Using only one role instead of both
- Trying to use API keys instead of managed identity
- Not waiting for role propagation before testing

### Verification Steps for Participants
1. Check managed identity exists: `az cognitiveservices account show`
2. Verify role assignments: `az role assignment list --assignee <principal-id>`
3. Test connection in Foundry portal
4. Query agent should retrieve documents with citations

---

## Command Reference

### Quick Setup Commands (All-in-One)

```bash
# Variables
RESOURCE_GROUP="rg-microhack"
FOUNDRY_RESOURCE="cog-v2jd2jfni7slw"
SEARCH_SERVICE="gptkb-v2jd2jfni7slw"
SUBSCRIPTION_ID="7a28b21e-0d3e-4435-a686-d92889d4ee96"

# Get Foundry managed identity
PRINCIPAL_ID=$(az cognitiveservices account show \
  -n $FOUNDRY_RESOURCE \
  -g $RESOURCE_GROUP \Reader (required for agent queries)
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

echo "✅ RBAC configuration complete! All three roles assigned."
echo "⏳ Wait 1-2 minutes for role propagation before testing agent.
  --assignee $PRINCIPAL_ID \
  --role "Search Service Contributor" \
  --scope "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.Search/searchServices/$SEARCH_SERVICE"

echo "✅ RBAC configuration complete!"
```

---

## Related Documentation

- **Azure AI Search RBReader" role assigned successfully
3. "Search Index Data Contributor" role assigned successfully
4. "Search Service Contributor" role assigned successfully
5. All three roles verified in role assignment list
6. Agent can connect to Azure AI Search without errors
7. Agent can query search index and retrieve documents
8. Citations appear in agent responses with document references
9. No "search_access_error" or "Forbidden" errors in playground
---

## Success Criteria

✅ **RBAC Configuration Complete** when:
1. Foundry managed identity Principal ID identified
2. "Search Index Data Contributor" role assigned successfully
3. "Search Service Contributor" role assigned successfully
4. Agent can connect to Azure AI Search without errors
5. Agent can query search index and retrieve documents
6. Citations appear in agent responses with document references

---

**Status**: ✅ **RBAC CONFIGURATION COMPLETE**

**Time to Complete**: ~5 minutes  
**Commands Executed**: 3 (identity lookup + 2 role assignments)  
**Next Step**: Configure agent instructions and test queries

# Azure AI Search RBAC Setup for Foundry Agents

**Date**: January 16, 2026  
**Purpose**: Complete guide to configure Azure AI Search permissions for Foundry agents using managed identity authentication

---

## Overview

Foundry agents require **three RBAC roles** on Azure AI Search to query knowledge bases. These permissions must be assigned to the **Foundry PROJECT managed identity**, not the parent Cognitive Services resource.

### Critical Distinction

❌ **WRONG**: Assigning roles to `cog-mfm4mgxglrqua` (parent resource)  
✅ **CORRECT**: Assigning roles to `cog-mfm4mgxglrqua/projects/microhack2-project` (project identity)

**Why?** Agents operate within a Foundry project context and use the project's managed identity, not the parent resource's identity.

---

## Prerequisites

Before starting:
- ✅ Foundry project deployed (e.g., `microhack2-project`)
- ✅ Azure AI Search service deployed (e.g., `gptkb-mfm4mgxglrqua`)
- ✅ Search index created and populated with documents
- ✅ Appropriate Azure RBAC permissions to assign roles (Owner or User Access Administrator)

---

## Required Roles

All **three** roles are required for full agent functionality:

| Role | Purpose | Required For |
|------|---------|--------------|
| **Search Index Data Reader** | Query and read search index | Agent to retrieve documents ✅ |
| **Search Index Data Contributor** | Read/write index data | Index operations (optional for read-only agents) |
| **Search Service Contributor** | Service-level management | Service configuration and connection validation |

⚠️ **Common Error**: Many guides only mention 2 roles, missing "Search Index Data Reader" which is critical for querying!

---

## Step 1: Enable "Both" Authentication on Search Service

The search service must accept both API keys and RBAC authentication.

### Option A: Azure Portal (Recommended)

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your resource group (e.g., `rg-microhack2`)
3. Open your Azure AI Search service (e.g., `gptkb-mfm4mgxglrqua`)
4. Left menu → **Settings** → **Keys**
5. Under **API access control**, select **"Both"**
6. Click **Save**

### Option B: Azure CLI

```bash
# Note: This may fail if search service has complex identity configuration
# Use portal method if you encounter identity-related errors

az search service update \
  --name gptkb-mfm4mgxglrqua \
  --resource-group rg-microhack2 \
  --auth-options aadOrApiKey \
  --aad-auth-failure-mode http401WithBearerChallenge
```

---

## Step 2: Identify the Project Managed Identity

### Get Project Principal ID (CLI)

```bash
# Set variables
RESOURCE_GROUP="rg-microhack2"
FOUNDRY_RESOURCE="cog-mfm4mgxglrqua"
PROJECT_NAME="microhack2-project"

# Get project resource ID
PROJECT_ID=$(az cognitiveservices account show \
  -n $FOUNDRY_RESOURCE \
  -g $RESOURCE_GROUP \
  --query "properties.projects[?name=='$PROJECT_NAME'].id | [0]" \
  -o tsv)

# Get project identity (if available via CLI)
# Note: As of 2026-01-16, project identity may need to be retrieved via portal
echo "Project resource path: ${FOUNDRY_RESOURCE}/projects/${PROJECT_NAME}"
```

### Get Project Principal ID (Portal)

1. Go to Azure Portal
2. Navigate to your Foundry resource (e.g., `cog-mfm4mgxglrqua`)
3. Left menu → **Operate** → **Manage** → **Resources**
4. Find your project → click **Connections**
5. Look for the project's managed identity principal ID in the connection details

**Example Principal ID**: `305fc35b-1af5-4dcf-afad-677d508273fb`

---

## Step 3: Assign RBAC Roles

### Option A: Azure Portal (Recommended)

**For each of the three roles, repeat these steps:**

1. Go to your Azure AI Search service in Azure Portal
2. Left menu → **Access control (IAM)**
3. Click **Add** → **Add role assignment**
4. **Role tab**: Select the role:
   - First: **Search Index Data Reader**
   - Second: **Search Index Data Contributor**
   - Third: **Search Service Contributor**
5. Click **Next**
6. **Members tab**: 
   - Select **Managed identity**
   - Click **+ Select members**
   - **Managed identity dropdown**: Select **"Foundry project"** (or filter for your project)
   - Find and select: `cog-mfm4mgxglrqua/projects/microhack2-project`
   - Click **Select**
7. **Review + assign tab**: Click **Review + assign**

Repeat for all three roles.

### Option B: Azure CLI (Advanced)

⚠️ **Challenge**: As of 2026-01-16, the Azure CLI doesn't have direct commands to retrieve Foundry project managed identity principal IDs. You'll need to get the principal ID from the portal first.

```bash
# Variables
RESOURCE_GROUP="rg-microhack2"
SEARCH_SERVICE="gptkb-mfm4mgxglrqua"
SUBSCRIPTION_ID="7a28b21e-0d3e-4435-a686-d92889d4ee96"

# PROJECT Principal ID (get from portal or Azure Resource Graph)
PROJECT_PRINCIPAL_ID="305fc35b-1af5-4dcf-afad-677d508273fb"  # Replace with your project's principal ID

# Build search service scope
SEARCH_SCOPE="/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RESOURCE_GROUP}/providers/Microsoft.Search/searchServices/${SEARCH_SERVICE}"

# Assign Search Index Data Reader
az role assignment create \
  --assignee $PROJECT_PRINCIPAL_ID \
  --role "Search Index Data Reader" \
  --scope "$SEARCH_SCOPE"

# Assign Search Index Data Contributor
az role assignment create \
  --assignee $PROJECT_PRINCIPAL_ID \
  --role "Search Index Data Contributor" \
  --scope "$SEARCH_SCOPE"

# Assign Search Service Contributor
az role assignment create \
  --assignee $PROJECT_PRINCIPAL_ID \
  --role "Search Service Contributor" \
  --scope "$SEARCH_SCOPE"

echo "✅ All three roles assigned to project identity"
echo "⏳ Wait 1-2 minutes for role propagation"
```

---

## Step 4: Verify Role Assignments

### Verify via Portal

1. Go to Azure AI Search service → **Access control (IAM)**
2. Click **Role assignments** tab
3. Search for your project name (e.g., "microhack2-project")
4. Confirm all three roles are listed:
   - ✅ Search Index Data Reader
   - ✅ Search Index Data Contributor
   - ✅ Search Service Contributor

### Verify via CLI

```bash
RESOURCE_GROUP="rg-microhack2"
SEARCH_SERVICE="gptkb-mfm4mgxglrqua"
SUBSCRIPTION_ID="7a28b21e-0d3e-4435-a686-d92889d4ee96"

SEARCH_SCOPE="/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RESOURCE_GROUP}/providers/Microsoft.Search/searchServices/${SEARCH_SERVICE}"

az role assignment list \
  --scope "$SEARCH_SCOPE" \
  --query "[?contains(principalName, 'project')].{Principal:principalName, Role:roleDefinitionName, Type:principalType}" \
  -o table
```

Expected output:
```
Principal                                          Role                           Type
-------------------------------------------------  -----------------------------  ----------------
cog-.../projects/microhack2-project               Search Index Data Reader       ServicePrincipal
cog-.../projects/microhack2-project               Search Index Data Contributor  ServicePrincipal
cog-.../projects/microhack2-project               Search Service Contributor     ServicePrincipal
```

---

## Step 5: Create Foundry Agent with Search Tool

**IMPORTANT**: Only create the agent AFTER completing Steps 1-4 and waiting 1-2 minutes for role propagation.

1. Go to Microsoft Foundry portal
2. Navigate to your project → **Build** → **Agents**
3. Click **+ Create new agent**
4. Configure agent:
   - **Name**: e.g., "HR-Benefits-Assistant"
   - **Instructions**: Use clear instructions like:
     ```
     You are an HR Benefits Assistant for Contoso Electronics. Your role is to 
     help employees understand their benefits, policies, and answer HR-related questions.

     INSTRUCTIONS:
     - Always search the knowledge base using Azure AI Search before answering questions
     - Provide accurate information based on the retrieved documents
     - Include citations with document names and page numbers when available
     - If you cannot find relevant information in the knowledge base, say "I don't have 
       that information in my knowledge base. Please contact HR directly."
     - Be professional, helpful, and empathetic
     - Do not make up information or provide answers without supporting documentation
     ```
5. **Tools section**:
   - Click **+ Add tool**
   - Select **Azure AI Search**
   - Configure connection:
     - **Search Service**: Select `gptkb-mfm4mgxglrqua`
     - **Index**: Select `gptkbindex`
     - **Authentication**: AAD / Managed Identity (auto-detected)
   - Connection should show **green checkmark** ✅
6. Click **Save**
7. Test the agent in the playground with a sample query

---

## Troubleshooting

### Error: "Access denied. Check your permissions or managed identity access to the search service."

**Causes**:
1. ❌ Roles assigned to parent resource instead of project
2. ❌ Missing "Search Index Data Reader" role
3. ❌ Search service authentication not set to "Both"
4. ❌ Role propagation delay (need to wait 1-2 minutes)

**Solutions**:
1. Verify roles are assigned to **project identity**, not parent
2. Confirm all **three roles** are assigned
3. Set search authentication to **"Both"** in portal
4. Wait 1-2 minutes after role assignment
5. **Delete and recreate** the agent to clear connection cache

### Error: "No tool output found for remote function call"

**Causes**:
1. ❌ Azure AI Search tool not added to agent
2. ❌ Tool connection not properly configured
3. ❌ Index name incorrect

**Solutions**:
1. Add Azure AI Search tool in agent Tools section
2. Verify connection shows green checkmark
3. Confirm index name matches (e.g., `gptkbindex`)

### Roles Were Assigned But Agent Still Fails

**Solution**: Delete and recreate the agent. Foundry agents cache connection information, and changes to RBAC may not be reflected in existing agents.

---

## Success Criteria

✅ **Setup is complete when**:
1. Search service authentication set to "Both"
2. All three RBAC roles assigned to project managed identity
3. Role assignments visible in IAM → Role assignments
4. Agent created with Azure AI Search tool connected
5. Agent successfully answers questions with document citations
6. No "Access denied" errors in agent traces

---

## Example Test Queries

After setup, test your agent with these queries:

- "What protection does Contoso offer against balance billing?"
- "What are my dental benefits under my plan?"
- "What hearing aids benefits do I have under my plan?"
- "What is the deductible for Northwind Health Plus?"

**Expected Response**:
- Agent retrieves relevant documents from search index
- Provides accurate answer based on documents
- Includes citations like `[Northwind_Standard_Benefits_Details.pdf#page=7]`

---

## Key Learnings

### ✅ What Worked
- Assigning roles to **PROJECT managed identity** (not parent resource)
- Using **Azure Portal** for role assignment (more reliable than CLI for projects)
- Setting search authentication to **"Both"**
- Assigning all **three roles** (including often-forgotten Search Index Data Reader)
- Creating **fresh agent** after RBAC changes

### ❌ Common Mistakes
- Assigning roles to parent Cognitive Services resource instead of project
- Missing "Search Index Data Reader" role (not mentioned in some documentation)
- Using only two roles (as some READMEs suggest)
- Not waiting for role propagation
- Trying to fix existing agent instead of creating new one

---

## Related Documentation

- [Azure AI Search RBAC Overview](https://learn.microsoft.com/azure/search/search-security-rbac)
- [Microsoft Foundry Agents](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/agents)
- [Challenge 1 README](../code/1_challenge/README.md) (⚠️ Note: missing third role as of 2026-01-16)

---

## Automation Script

Complete setup script for reference:

```bash
#!/bin/bash
# Complete RBAC setup for Foundry agent + Azure AI Search

# ============================================================================
# VARIABLES - UPDATE THESE FOR YOUR ENVIRONMENT
# ============================================================================
RESOURCE_GROUP="rg-microhack2"
FOUNDRY_RESOURCE="cog-mfm4mgxglrqua"
SEARCH_SERVICE="gptkb-mfm4mgxglrqua"
SUBSCRIPTION_ID="7a28b21e-0d3e-4435-a686-d92889d4ee96"

# Get PROJECT principal ID from portal and update here
PROJECT_PRINCIPAL_ID="305fc35b-1af5-4dcf-afad-677d508273fb"  # REPLACE WITH YOUR PROJECT'S PRINCIPAL ID

# ============================================================================
# STEP 1: Enable Both authentication on search service (optional - use portal)
# ============================================================================
echo "Step 1: Configuring search service authentication..."
echo "⚠️  Recommend doing this via Azure Portal: Settings → Keys → Select 'Both'"
echo "    (CLI command may fail with identity errors)"

# ============================================================================
# STEP 2: Assign RBAC roles to PROJECT identity
# ============================================================================
echo ""
echo "Step 2: Assigning RBAC roles to project identity..."

SEARCH_SCOPE="/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RESOURCE_GROUP}/providers/Microsoft.Search/searchServices/${SEARCH_SERVICE}"

echo "  Assigning Search Index Data Reader..."
az role assignment create \
  --assignee $PROJECT_PRINCIPAL_ID \
  --role "Search Index Data Reader" \
  --scope "$SEARCH_SCOPE" \
  --output none

echo "  Assigning Search Index Data Contributor..."
az role assignment create \
  --assignee $PROJECT_PRINCIPAL_ID \
  --role "Search Index Data Contributor" \
  --scope "$SEARCH_SCOPE" \
  --output none

echo "  Assigning Search Service Contributor..."
az role assignment create \
  --assignee $PROJECT_PRINCIPAL_ID \
  --role "Search Service Contributor" \
  --scope "$SEARCH_SCOPE" \
  --output none

# ============================================================================
# STEP 3: Verify assignments
# ============================================================================
echo ""
echo "Step 3: Verifying role assignments..."
az role assignment list \
  --scope "$SEARCH_SCOPE" \
  --assignee "$PROJECT_PRINCIPAL_ID" \
  --query "[].{Role:roleDefinitionName, Scope:scope}" \
  -o table

echo ""
echo "✅ RBAC setup complete!"
echo ""
echo "NEXT STEPS:"
echo "1. Wait 1-2 minutes for role propagation"
echo "2. Create new Foundry agent with Azure AI Search tool"
echo "3. Test agent with sample queries"
echo ""
echo "If agent shows 'Access denied':"
echo "  - Verify search service authentication is set to 'Both' (in portal)"
echo "  - Delete and recreate the agent to clear connection cache"
```

---

**Status**: ✅ Validated setup (January 16, 2026)  
**Environment**: microhack2 deployment  
**Agent**: "TWO" - working successfully with all three roles

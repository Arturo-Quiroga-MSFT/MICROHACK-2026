# Challenge 0: Environment Setup - COMPLETED ✅

**Date Completed**: January 15, 2026  
**Coach**: Arturo Quiroga  
**Time to Complete**: ~20 minutes (14m23s deployment + upgrade)

---

## Overview

Successfully set up the complete Azure environment for the Trustworthy AI Microhack, including:
- Base RAG chat application deployment
- Azure infrastructure provisioning
- Azure OpenAI to Foundry migration

---

## Steps Completed

### 1. Repository Setup

**Created GitHub Repository**:
- Repository: `Arturo-Quiroga-MSFT/MICROHACK-2026`
- URL: https://github.com/Arturo-Quiroga-MSFT/MICROHACK-2026
- Visibility: Public
- Purpose: Coach preparation materials and evaluation scripts

**Local Workspace**:
- Location: `/Users/arturoquiroga/MICROHACK-2026`
- Initialized git repository
- Pushed all microhack materials to GitHub

### 2. RAG Application Deployment

**Cloned Base Application**:
```bash
cd /Users/arturoquiroga
git clone https://github.com/Azure-Samples/azure-search-openai-demo.git azure-ragchat-demo
```

**Deployed with Azure Developer CLI**:
```bash
cd azure-ragchat-demo
azd up
```

**Deployment Configuration**:
- Environment Name: `microhack`
- Subscription: `ARTURO-MngEnvMCAP094150` (7a28b21e-0d3e-4435-a686-d92889d4ee96)
- Primary Region: East US 2
- Document Intelligence Region: West US 2
- Deployment Time: 14 minutes 23 seconds

---

## Resources Provisioned

### Resource Group
- **Name**: `rg-microhack`
- **Location**: East US 2
- **Status**: Succeeded

### Azure OpenAI (Upgraded to Foundry)
- **Original Name**: `cog-v2jd2jfni7slw`
- **Kind**: OpenAI → **Microsoft Foundry** (after upgrade)
- **Location**: eastus2
- **Foundry Project**: `cog-v2jd2jfni7slw-project`

**Model Deployments**:
- `gpt-4.1-mini` - Chat completion model
- `text-embedding-3-large` - Embedding model for vector search

### Azure AI Search
- **Name**: `gptkb-v2jd2jfni7slw`
- **Index Name**: `gptkbindex`
- **Total Sections Indexed**: 755 sections

**Indexed Documents**:
- Northwind_Standard_Benefits_Details.pdf (305 sections)
- Northwind_Health_Plus_Benefits_Details.pdf (314 sections)
- role_library.pdf (76 sections)
- employee_handbook.pdf (22 sections)
- Financial Market Analysis Report 2023.pdf (11 sections)
- Benefit_Options.pdf (7 sections)
- PerksPlus.pdf (6 sections)
- Zava_Company_Overview.md (3 sections)
- Various JSON files (11 sections)

### Document Intelligence
- **Name**: `cog-di-v2jd2jfni7slw`
- **Kind**: FormRecognizer
- **Location**: westus2

### Monitoring & Observability
- **Application Insights**: `appi-v2jd2jfni7slw`
- **Log Analytics Workspace**: `log-v2jd2jfni7slw`
- **Portal Dashboard**: `dash-v2jd2jfni7slw`

### Container Infrastructure
- **Container Registry**: `microhackacrv2jd2jfni7slw`
- **Container Apps Environment**: `microhack-aca-env`
- **Backend Container App**: `capps-backend-v2jd2jfni7slw`

### Storage
- **Storage Account**: `stv2jd2jfni7slw`

---

## Application Deployment

### Live Application
- **URL**: https://capps-backend-v2jd2jfni7slw.blackriver-d1eaacf5.eastus2.azurecontainerapps.io/
- **Status**: ✅ Running and responding
- **Verification**: curl returned valid HTML response

### Application Features
- Enterprise Q&A chat interface
- RAG pattern implementation
- Azure OpenAI GPT-4.1-mini backend
- Azure AI Search for document retrieval
- Document Intelligence for PDF processing

---

## Azure OpenAI → Foundry Upgrade

### Migration Process
1. Navigated to Azure OpenAI resource in portal
2. Clicked "Upgrade to Foundry" banner
3. Accepted default project name: `cog-v2jd2jfni7slw-project`
4. Upgrade completed in ~2 minutes

### New Foundry Project Details
- **Project Name**: `cog-v2jd2jfni7slw-project`
- **Endpoint**: https://cog-v2jd2jfni7slw.services.ai.azure.com/api/projects/
- **Location**: eastus2
- **Resource Group**: rg-microhack
- **Subscription**: ARTURO-MngEnvMCAP094150

### Foundry Capabilities Enabled
- ✅ **Agents** - Build and manage AI agents
- ✅ **Model Catalog** - Access to OpenAI, Microsoft Research, and OSS models
- ✅ **Playgrounds** - Chat, Assistants, Video, Audio, Images
- ✅ **Templates** - Pre-built agent templates
- ✅ **Fine-tuning** - Model customization
- ✅ **Evaluation** (PREVIEW) - Automated testing
- ✅ **Guardrails + Controls** - Content safety and policy enforcement
- ✅ **Tracing** (PREVIEW) - Observability for agent workflows
- ✅ **Monitoring** - Performance and usage tracking
- ✅ **Governance** (PREVIEW) - Compliance and risk management

### Authentication Note
- API key authentication is disabled (using Azure credential/passwordless)
- This is the recommended secure approach

---

## Success Criteria Validation

✅ **Environment Provisioned**
- All Azure resources created successfully
- Resource group: rg-microhack deployed in East US 2

✅ **Application Deployed**
- RAG chat application accessible at public endpoint
- Successfully returns HTML and serves frontend

✅ **Documents Indexed**
- 755 document sections indexed in Azure AI Search
- All sample documents (Northwind benefits, employee handbook, etc.) processed

✅ **Models Deployed**
- GPT-4.1-mini deployment active
- text-embedding-3-large deployment active

✅ **Foundry Migration Complete**
- Azure OpenAI resource upgraded to Microsoft Foundry
- Foundry project created with all capabilities enabled
- Existing deployments preserved

✅ **Monitoring Configured**
- Application Insights connected
- Log Analytics workspace operational

---

## Key URLs & Resources

### Azure Portal Links
- **Resource Group**: https://portal.azure.com/#resource/subscriptions/7a28b21e-0d3e-4435-a686-d92889d4ee96/resourceGroups/rg-microhack/overview
- **Foundry Project**: https://ai.azure.com/foundryProject/overview?wsid=/subscriptions/7a28b21e-0d3e-4435-a686-d92889d4ee96/resourceGroups/rg-microhack/providers/Microsoft.CognitiveServices/accounts/cog-v2jd2jfni7slw-project
- **Application**: https://capps-backend-v2jd2jfni7slw.blackriver-d1eaacf5.eastus2.azurecontainerapps.io/

### GitHub Repository
- **Microhack Materials**: https://github.com/Arturo-Quiroga-MSFT/MICROHACK-2026

### Local Directories
- **Microhack Workspace**: `/Users/arturoquiroga/MICROHACK-2026`
- **RAG Application**: `/Users/arturoquiroga/azure-ragchat-demo`

---

## Command Reference

### Azure CLI Commands Used
```bash
# Verify Azure login
az account show --query "{Subscription:name, TenantId:tenantId, User:user.name}" -o table

# List cognitive services accounts
az cognitiveservices account list -g rg-microhack --query "[].{Name:name, Kind:kind, Location:location}" -o table

# Check resource group status
az group show -n rg-microhack --query "{Name:name, Location:location, State:properties.provisioningState}" -o table
```

### Azure Developer CLI Commands
```bash
# Deploy complete infrastructure and application
azd up

# Configuration during deployment
# - Environment: microhack
# - Subscription: ARTURO-MngEnvMCAP094150
# - Document Intelligence Location: West US 2
# - Primary Location: East US 2
# - OpenAI Location: East US 2
```

### GitHub CLI Commands
```bash
# Create and push repository
git init
gh repo create MICROHACK-2026 --public --source=. --remote=origin --description="Trustworthy AI Microhack - Coach Preparation"
git add -A
git commit -m "Initial commit: Trustworthy AI Microhack materials"
git branch -M main
git push -u origin main
```

---

## Environment Variables (from azd)

Location: `/Users/arturoquiroga/azure-ragchat-demo/.azure/microhack/.env`

Key variables set by azd deployment:
- `AZURE_SUBSCRIPTION_ID`
- `AZURE_RESOURCE_GROUP`
- `AZURE_OPENAI_SERVICE`
- `AZURE_SEARCH_SERVICE`
- `AZURE_STORAGE_ACCOUNT`
- `AZURE_FORMRECOGNIZER_SERVICE`
- `AZURE_APP_INSIGHTS`

---

## Coaching Notes

### Potential Participant Issues
1. **Region Selection**: Ensure participants choose supported regions (East US 2, West US, Sweden Central recommended)
2. **Quota Limits**: Some subscriptions may hit OpenAI quota limits - check beforehand
3. **Authentication**: Participants need proper RBAC permissions (Contributor or Owner on subscription)
4. **azd Version**: Ensure azd CLI is up to date (v1.23.0+)
5. **Deployment Time**: Set expectations - full deployment takes 12-15 minutes
6. **Foundry Upgrade**: Some may need manual upgrade via portal (as we did)

### Success Indicators for Participants
- Application endpoint returns valid HTTP 200 response
- Can access Foundry portal and see project
- Azure AI Search index contains documents (check in portal)
- Models are deployed and show "Succeeded" status

### Common Troubleshooting
- **Deployment fails**: Check subscription quota for OpenAI models
- **Documents not indexed**: Check Document Intelligence service provisioned successfully
- **Can't access Foundry**: Verify user has appropriate RBAC roles
- **App not loading**: Check Container App logs in portal

---

## Next Steps - Challenge 1

With Challenge 0 complete, ready to proceed to Challenge 1:

**Challenge 1 - Responsible AI Application Design**:
1. Create an Agent in Foundry portal
2. Connect Azure AI Search index (gptkb-v2jd2jfni7slw)
3. Configure content safety guardrails
4. Perform Responsible AI Impact Assessment
5. Run manual evaluations in Foundry
6. Execute automated evaluations using Azure AI Evaluation SDK

**Prerequisites Now Met**:
- ✅ Foundry project with agent capabilities
- ✅ Azure AI Search index with data
- ✅ Model deployments (GPT-4.1-mini, embeddings)
- ✅ Application Insights for tracing
- ✅ Document corpus indexed

---

## Time Investment Summary

| Activity | Time |
|----------|------|
| GitHub repo setup | 2 minutes |
| Clone base application | 1 minute |
| azd deployment | 14m 23s |
| Foundry upgrade | 2 minutes |
| Verification & testing | 2 minutes |
| **Total** | **~22 minutes** |

---

## Resources for Reference

- **RAG Chat App GitHub**: https://github.com/Azure-Samples/azure-search-openai-demo
- **Azure AI Foundry Docs**: https://learn.microsoft.com/azure/ai-foundry/
- **Upgrade Guide**: https://learn.microsoft.com/azure/ai-foundry/how-to/upgrade-azure-openai
- **Challenge Materials**: `/Users/arturoquiroga/MICROHACK-2026/code/0_challenge/README.md`

---

**Status**: ✅ **CHALLENGE 0 COMPLETE - READY FOR CHALLENGE 1**

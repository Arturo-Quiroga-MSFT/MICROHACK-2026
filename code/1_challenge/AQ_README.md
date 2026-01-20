# Challenge 1: Responsible AI - Designing a Reliable & Ethical Approach

## Overview

Contoso Electronics is piloting an internal HR Q&A application where employees can ask about benefits and policies. The bot retrieves answers from policy documents with citations. 

Before full deployment, the team must ensure the AI behaves responsibly. In this challenge, participants act as AI developers conducting an AI Impact Assessment and initial testing using:
- **Azure AI Foundry IQ** (agent creation + evaluation)
- **Control Plane** (deployment governance and monitoring)
- **Azure AI Search** (indexed data)
- **Azure OpenAI** (model deployment)

---

## Tools & Configuration Needed

- Azure AI Foundry IQ (agent creation + evaluation)
- Control Plane (deployment governance and monitoring)
- Azure AI Search (indexed data)
- Azure OpenAI model deployment
- Ground truth Q&A list (for evaluation)

---

## Part 1: Migrate Azure OpenAI to Microsoft Foundry

### Step 1.1: Open Azure OpenAI in Foundry

1. From **Azure Portal**, go to the resource group created in Challenge 0
2. Find and open your **Azure OpenAI** service

![Resources](/media/CH1_Resources.png)

3. Click **"Open in Foundry"**

![Open Foundry](/media/CH1_Foundry.png)

### Step 1.2: Start the Migration Wizard

1. Go to **Home**
2. Click **"Get Started"** to access the migration wizard

![Azure OpenAI Home](/media/CH1_AzureOpenAI.png)

### Step 1.3: Complete the Migration

1. Click **"Next"** to proceed

![Migration Wizard](/media/CH1_Migration.png)

2. Click **"Confirm"** to create your Foundry project

![Create Project](/media/CH1_CreateProject.png)

**Reference**: [How to upgrade Azure OpenAI to Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/upgrade-azure-openai?view=foundry-classic&tabs=portal#how-to-upgrade)

### What You Get with Foundry

With the 2026 Foundry project rollout, you get far more than just models:
- ✅ Agentic workflows
- ✅ Broader model catalog
- ✅ Foundry SDK
- ✅ Enhanced monitoring and observability
- ✅ Evaluation capabilities
- ✅ Support for multi-agent architectures at scale

![Foundry Upgrade](/media/CH1_Upgrade.png)

### Step 1.4: Access Your Foundry Project

1. View your **Foundry endpoint**
2. Click **"Start building"**

![Foundry Home](/media/CH1_FoundryHome.png)

---

## Part 2: Create Your First Agent

### Step 2.1: Create a New Agent

1. Expand the **"Start building"** dropdown
2. Click **"Create Agent"**

![Create Agent](/media/CH1_CreateAgent.png)

3. Enter a **name** for your agent (e.g., "HR-Benefits-Assistant")
4. Click **"Create"**

![Agent Name](/media/CH1_Agentname.png)

### Step 2.2: Verify Model Deployments

1. Go to the **Models** tab
2. View all deployed models under the **"Deployed"** tab

![Models Tab](/media/CH1_Models.png)

**Optional**: Deploy additional models
- Click **"Deploy base model"**
- Explore the model catalog
- Deploy any model of your choice

![Model Catalog](/media/CH1_ModelCatalog.png)

![Model Details](/media/CH1_ModelDetails.png)

---

## Part 3: Connect Agent to Azure AI Search

### Step 3.1: Add Azure AI Search Tool

1. In the **Agent playground**, go to **Tools**
2. Click **"Add tool"**
3. Select **"Azure AI Search"**

![Add Tool](/media/CH1_AddTool.png)

### Step 3.2: Create Search Connection

1. On the **"Create a new connection"** page:
   - Select your Azure AI Search resource from the dropdown
   - Click **"Connect"**

![Create Connection](/media/CH1_CreateConnection.png)

2. **Add search index**

![Add Index](/media/CH1_AddIndex.png)

**Optional**: Create a new index
- Select the **Storage account** created in Challenge 0
- Select the **'content'** container
- Click **"Create index"**

### Step 3.3: Enable RBAC for Azure AI Search

⚠️ **IMPORTANT**: Before testing the agent, configure RBAC permissions

#### Enable "Both" Authentication Mode

1. Go to your **Azure AI Search** resource in the portal
2. Navigate to **Settings → Keys**
3. Select **"Both"** to enable both key-based and keyless authentication
4. Click **"Save"**

![Keys Configuration](/media/CH1_keys.png)

#### Assign Required Roles

You need to assign **THREE roles** to your Foundry project's managed identity:

1. Go to **Access control (IAM)** in your Azure AI Search resource
2. Click **"Add" → "Add role assignment"**
3. Assign these roles to your **project's managed identity**:
   - ✅ **Search Index Data Reader** (required for queries)
   - ✅ **Search Index Data Contributor** (required for index operations)
   - ✅ **Search Service Contributor** (required for service management)

**How to find your project's managed identity**:
- In IAM role assignment, select **"Managed identity"**
- Choose **"Foundry project"** from the dropdown
- Select your project (e.g., `cog-xxxxx/projects/your-project-name`)

![Role Assignment](/media/CH1_RoleAssignment.png)

💡 **Note**: Wait 1-2 minutes after role assignment for permissions to propagate

---

## Part 4: Configure Agent Instructions and Monitoring

### Step 4.1: Add Agent Instructions

Add clear instructions to help your agent use the tools effectively:

**Example instructions**:
```
You are an HR Benefits Assistant for Contoso Electronics.

INSTRUCTIONS:
- Always search the knowledge base using Azure AI Search before answering
- Provide accurate information based on retrieved documents
- Include citations with document names and page numbers
- If information isn't in the knowledge base, say "I don't have that information"
- Be professional, helpful, and empathetic
- Do not make up information
```

**Save** your agent configuration

### Step 4.2: Connect Monitoring

1. Go to the **Monitor** tab
2. Click **"Connect to Application Insights"**
3. Select the **App Insights resource** created in Challenge 0
4. Confirm the connection

![Monitor Configuration](/media/CH1_Monitor.png)

---

## Part 5: Connect Knowledge Base (Foundry IQ)

### Step 5.1: Enable Foundry IQ

1. In your agent, go to the **Knowledge** tab
2. Click **"Connect to Foundry IQ"**

![Foundry IQ](/media/CH1_FoundryIQ.png)

### Step 5.2: Create Knowledge Base

1. Create a new knowledge base using your Azure AI Search index
2. **Save** your agent

![Knowledge Base](/media/CH1_knowledgebase.png)

---

## Part 6: Test Your Agent

### Step 6.1: Run Test Queries

Test your agent with sample questions from the ground truth dataset:

**Sample questions**: [ground_truth.jsonl](https://github.com/Azure-Samples/azure-search-openai-demo/blob/main/evals/ground_truth.jsonl)

Example queries:
- "What protection does Contoso offer against balance billing?"
- "What are my dental benefits under my plan?"
- "What hearing aids benefits do I have?"
- "What is the deductible for Northwind Health Plus?"

![Test Agent](/media/CH1_testAgent.png)

### Step 6.2: Verify Monitoring Data

1. Go to the **Monitor** tab
2. Confirm that telemetry is being captured
3. Review traces and metrics

![Monitor Agent](/media/CH1_MonitorAgent.png)

---

## Part 7: Create Guardrail Policy

### Overview

Guardrail policies ensure your AI models operate safely and responsibly by enforcing minimum safety controls.

**Reference**: [Create Guardrail Policy](https://learn.microsoft.com/en-us/azure/ai-foundry/control-plane/quickstart-create-guardrail-policy?view=foundry)

### Step 7.1: Navigate to Compliance

1. Click **"Operate"** in the upper-right navigation
2. Select **"Compliance"** in the left pane
3. Click **"Create policy"**

![Operate Tab](/media/CH1_Operate.png)

### Step 7.2: Add Guardrail Controls

Select the controls to add to your policy. As you configure each control, click **"Add control"**.

**Available controls**:
- 🛡️ **Content safety filters** - Block harmful content
- 🛡️ **Prompt shields** - Protect against prompt injection attacks
- 🛡️ **Groundedness checks** - Ensure responses are based on source data

These controls represent the **minimum settings** required for compliance.

### Step 7.3: Define Policy Scope

1. Click **"Next"** to move to scope selection
2. Choose your scope:
   - **Subscription** - Apply policy across entire subscription
   - **Resource Group** - Apply policy to specific resource group
3. Select your desired subscription or resource group
4. Click **"Select"**

💡 **Tip**: For this challenge, scope to your resource group

### Step 7.4: Add Exceptions (Optional)

1. Click **"Next"** to add exceptions

**Exception options**:
- If scoped to **subscription**: Exclude entire resource groups or individual deployments
- If scoped to **resource group**: Exclude individual model deployments only

2. Add any needed exceptions
3. Click **"Next"** when done

### Step 7.5: Review and Submit

1. **Name your policy** (e.g., "Contoso-HR-Bot-Policy")
2. Review:
   - Scope
   - Controls
   - Exceptions
3. Click **"Submit"** to create the policy

![Compliance Dashboard](/media/CH1_Compliance.png)

---

## Part 8: Run Evaluations

### Step 8.1: Upload Ground Truth Dataset

1. Go to your agent's **Evaluations** tab
2. Click **"Upload dataset"**
3. Upload the **ground_truth.jsonl** file

![Upload Ground Truth](/media/CH1_truth.png)

### Step 8.2: Configure and Run Evaluation

1. Review the evaluation configuration
2. Select evaluation metrics:
   - **Relevance** - Are responses relevant to the question?
   - **Groundedness** - Are responses grounded in source documents?
   - **Citation quality** - Are citations accurate?
   - **Safety** - Are responses safe and appropriate?
3. Click **"Run evaluation"**
4. Wait for completion (typically 5-10 minutes)

![Run Evaluation](/media/CH1_Evaluation.png)

### Step 8.3: Review Results

1. View all metrics in the **Evaluations** tab
2. Review individual question/answer pairs
3. Identify areas for improvement

![Evaluation Metrics](/media/CH1_EvaluationMetrics.png)

---

## Success Criteria

To successfully complete this challenge, you must:

### ✅ 1. Successfully Migrate Azure OpenAI to Microsoft Foundry
- Open the Challenge 0 Azure OpenAI resource in Microsoft Foundry
- Complete the Azure OpenAI → Foundry migration
- Confirm Foundry project creation

### ✅ 2. Create a New Agent in Foundry
- Create an agent in the Foundry project
- Verify agent workspace is active

### ✅ 3. Verify & Deploy Models
- Navigate to the Models tab
- Verify deployed Azure OpenAI models appear under "Deployed"
- (Optional) Deploy an additional model from the Model Catalog

### ✅ 4. Connect Agent to Azure AI Search
- Add Azure AI Search from Tools
- Create or select a search index
- Enable "Both" authentication mode on search service
- Assign all **three required roles** to project managed identity:
  - Search Index Data Reader
  - Search Index Data Contributor
  - Search Service Contributor
- Verify tool appears with no configuration errors

### ✅ 5. Add Instructions to the Agent
- Write clear system instructions
- Define when to use Azure AI Search
- Save configuration with no validation errors

### ✅ 6. Configure Monitoring
- Connect agent to Application Insights from Challenge 0
- Confirm telemetry is active

### ✅ 7. Connect Knowledge via Foundry IQ
- Connect to Foundry IQ
- Create Knowledge Base using Azure AI Search index
- Save agent successfully

### ✅ 8. Test the Agent
- Test with sample questions from ground_truth.jsonl
- Verify correct search retrieval
- Confirm grounded responses with no hallucinations
- Observe monitoring/traces in Monitor tab

### ✅ 9. Create a Guardrail Policy
- Navigate to Operate → Compliance
- Create policy with safety filters, prompt shields, and groundedness controls
- Assign policy scope to subscription/resource group
- Submit successfully

### ✅ 10. Run Evaluations
- Upload ground_truth.jsonl under Evaluations
- Run evaluation job
- Review metrics: accuracy, groundedness, citations, safety

---

## Learning Resources

### Microsoft Foundry
- [What is Azure AI Foundry?](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry?view=foundry-classic)
- [Control Plane Overview](https://learn.microsoft.com/en-us/azure/ai-foundry/control-plane/overview?view=foundry)

### Azure AI Search
- [What is Azure AI Search?](https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search?tabs=indexing%2Cquickstarts)

### Responsible AI
- [Responsible AI Concepts](https://learn.microsoft.com/en-us/azure/machine-learning/concept-responsible-ai?view=azureml-api-2)

---

## Troubleshooting

### Agent shows "Access denied" error

**Cause**: Missing RBAC permissions or roles not propagated

**Solution**:
1. Verify all **three roles** are assigned in Azure AI Search IAM
2. Confirm roles are assigned to **project managed identity** (not parent resource)
3. Wait 1-2 minutes for role propagation
4. Delete and recreate the agent to clear connection cache

### Tool shows configuration errors

**Cause**: Search service authentication not set to "Both"

**Solution**:
1. Go to Azure AI Search → Settings → Keys
2. Select "Both" for authentication
3. Save and wait 1-2 minutes

### Agent doesn't return documents

**Cause**: Missing "Search Index Data Reader" role

**Solution**:
1. Go to Azure AI Search → Access Control (IAM)
2. Add role assignment: "Search Index Data Reader"
3. Assign to project managed identity
4. Recreate agent

---

# 🎉 CHALLENGE 1 COMPLETE!

Congratulations! You've successfully:
- ✅ Migrated Azure OpenAI to Microsoft Foundry
- ✅ Created and configured a Foundry agent
- ✅ Implemented RBAC security
- ✅ Connected knowledge sources
- ✅ Created guardrail policies
- ✅ Ran comprehensive evaluations

**Next**: Continue to [Challenge 2 - Well-Architected & Trustworthy Foundation](/code/2_challenge/README.md)

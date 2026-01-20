# Comparison: Your Documentation vs. Updated Challenge READMEs

**Date**: January 20, 2026  
**Purpose**: Compare your working RBAC setup documentation with the updated Challenge 1 README and identify script update needs

---

## 1. Challenge 1 RBAC Instructions - Gap Analysis

### Your Documentation (FOUNDRY-AGENT-SEARCH-RBAC-SETUP.md)

✅ **Comprehensive and Accurate** - Documents the complete working solution:

| Topic | Your Docs | Challenge 1 README | Status |
|-------|-----------|-------------------|---------|
| **Number of Roles** | ✅ THREE roles | ❌ TWO roles | **README GAP** |
| **Parent vs Project Identity** | ✅ Explicitly documented | ❌ Not mentioned | **README GAP** |
| **Search Index Data Reader** | ✅ Included | ❌ Missing | **CRITICAL GAP** |
| **Search Index Data Contributor** | ✅ Included | ✅ Included | ✅ Match |
| **Search Service Contributor** | ✅ Included | ✅ Included | ✅ Match |
| **"Both" Authentication** | ✅ Step-by-step portal + CLI | ✅ Portal steps | ✅ Match |
| **Troubleshooting** | ✅ Comprehensive section | ❌ Not included | Your docs better |
| **CLI Commands** | ✅ With project principal ID | ❌ Not provided | Your docs better |
| **Agent Recreation Note** | ✅ Documented | ❌ Not mentioned | Your docs better |

### Critical README Gap

**Challenge 1 README Line 171-183** states:
```markdown
To enable RBAC:
From the left pane, select Settings > Keys. 
Select Both to enable both key-based and keyless authentication...

2. To assign the necessary roles: 
From the left pane, select Access control (IAM). 
Select Add > Add role assignment. 
Assign the Search Index Data Contributor role to the managed identity of your project. 
Repeat the role assignment for Search Service Contributor.
```

❌ **Missing**: Search Index Data Reader (required for queries!)

---

## 2. Your SET_RBAC.sh Script Analysis

### Current Script Status

✅ **Functionally Correct** but targets parent resource by default

**Location**: `/Users/arturoquiroga/MICROHACK-2026/code/1_challenge/SET_RBAC.sh`

**Current Behavior**:
- Uses `az cognitiveservices account show` to get principal ID
- This retrieves the **parent resource identity** (`dfd02657-...`)
- Assigns all three roles correctly
- **Problem**: Agents use PROJECT identity, not parent identity

### Required Updates

**Option 1: Update Script to Get Project Identity** (Recommended for full automation)

```bash
#!/bin/bash
# UPDATED: Now targets Foundry PROJECT managed identity

RESOURCE_GROUP="rg-microhack2"
FOUNDRY_RESOURCE="cog-mfm4mgxglrqua"
PROJECT_NAME="microhack2-project"
SEARCH_SERVICE="gptkb-mfm4mgxglrqua"
SUBSCRIPTION_ID="7a28b21e-0d3e-4435-a686-d92889d4ee96"

echo "⚠️  CRITICAL: This script assigns roles to the Foundry PROJECT identity"
echo "   Foundry agents use PROJECT managed identity, not parent resource identity"
echo ""

# NOTE: As of 2026-01-20, Azure CLI doesn't have direct command to get project principal ID
# You must retrieve it manually from the Azure Portal:
# 1. Go to Foundry resource → Project → Connections
# 2. Copy the project's managed identity principal ID

echo "Please provide the PROJECT managed identity principal ID:"
read -p "Project Principal ID: " PROJECT_PRINCIPAL_ID

if [ -z "$PROJECT_PRINCIPAL_ID" ]; then
    echo "❌ Error: Project principal ID is required"
    exit 1
fi

echo ""
echo "Configuration:"
echo "  Resource Group: $RESOURCE_GROUP"
echo "  Search Service: $SEARCH_SERVICE"
echo "  Project Principal ID: $PROJECT_PRINCIPAL_ID"
echo ""

SEARCH_SCOPE="/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RESOURCE_GROUP}/providers/Microsoft.Search/searchServices/${SEARCH_SERVICE}"

# Assign all three roles
echo "Assigning Search Index Data Reader..."
az role assignment create \
  --assignee $PROJECT_PRINCIPAL_ID \
  --role "Search Index Data Reader" \
  --scope "$SEARCH_SCOPE"

echo "Assigning Search Index Data Contributor..."
az role assignment create \
  --assignee $PROJECT_PRINCIPAL_ID \
  --role "Search Index Data Contributor" \
  --scope "$SEARCH_SCOPE"

echo "Assigning Search Service Contributor..."
az role assignment create \
  --assignee $PROJECT_PRINCIPAL_ID \
  --role "Search Service Contributor" \
  --scope "$SEARCH_SCOPE"

echo ""
echo "✅ All three roles assigned to project identity"
echo "⏳ Wait 1-2 minutes for role propagation"
echo ""
echo "Next steps:"
echo "1. Enable 'Both' authentication on search service (if not done)"
echo "2. Create NEW Foundry agent with Azure AI Search tool"
echo "3. Test agent with sample queries"
```

**Option 2: Add Environment Variable** (Quick fix)

```bash
# At the top of existing script, add:
PROJECT_PRINCIPAL_ID="${PROJECT_PRINCIPAL_ID:-dfd02657-ed0d-493a-8ddc-188342ade4ba}"

# Usage:
# PROJECT_PRINCIPAL_ID="305fc35b-1af5-4dcf-afad-677d508273fb" ./SET_RBAC.sh
```

---

## 3. Challenge 0 & Challenge 2 Script Comparison

### Challenge 0: evaluatemh.py

**Your Script** (`code/0_challenge/evaluatemh.py`):
- ✅ Targets `/chat` endpoint
- ✅ Uses `BACKEND_URI` from environment
- ✅ Includes multiprocessing workaround
- ✅ Uploads to Foundry via `AZURE_AI_PROJECT_ENDPOINT`
- ✅ Ground truth file: `ground_truth_test.jsonl`

**Challenge 2** (`code/2_challenge/evaluate.py`):
- ✅ Same structure
- ✅ Targets `/ask` endpoint (different)
- ⚠️ Uses `BACKEND_URL` variable (minor naming difference)

**Status**: ✅ Your Challenge 0 script is correct and updated

---

### Challenge 0: safety_evaluationmh.py

**Your Script** (`code/0_challenge/safety_evaluationmh.py`):
- ✅ Uses `AdversarialSimulator` + `ContentSafetyEvaluator`
- ✅ Targets `/chat` endpoint
- ✅ Uses `AzureDeveloperCliCredential`
- ✅ Saves to `redteam_results/simulation_data.jsonl`
- ✅ Uploads results to Foundry portal
- ✅ Validates simulation outputs before evaluation

**Challenge 2** (`code/2_challenge/safety_evaluation.py`):
- ✅ Identical structure and approach
- ✅ Same credential handling
- ⚠️ Endpoint consistency (`/chat` with auto-appending)

**Status**: ✅ Your Challenge 0 script is correct and matches updated Challenge 2 pattern

---

### Challenge 0: redteammh.py

**Your Script** (`code/0_challenge/redteammh.py`):
- ✅ Uses `RedTeam` class from `azure.ai.evaluation.red_team`
- ✅ Targets `/chat` endpoint
- ✅ Four risk categories: Violence, HateUnfairness, Sexual, SelfHarm
- ✅ Async execution with `asyncio.run()`
- ✅ Saves to `evals/redteam_results/basic_scan_results.json`
- ✅ Advanced scan commented out (time/cost optimization)
- ✅ Uses `BACKEND_URI` from environment
- ❌ **Missing**: Import statements in `if __name__ == "__main__"` block

**Challenge 2** (`code/2_challenge/redteam.py`):
- ✅ Same structure
- ✅ Same risk categories
- ✅ Uses `/ask` endpoint (different)
- ✅ Imports in proper location

**Issue Found**: Your `redteammh.py` has imports inside `if __name__` block, which is correct for multiprocessing, but different from Challenge 2 reference.

**Status**: ⚠️ Minor structural difference, functionally equivalent

---

## 4. Script Update Recommendations

### 🔧 Required Updates

#### 1. SET_RBAC.sh - Add Project Identity Support

**Priority**: HIGH  
**Impact**: Critical for agent RBAC setup

```bash
# Update script to prompt for project principal ID
# Add warning about parent vs project identity
# See Option 1 in Section 2 above
```

---

### 📋 Optional Improvements

#### 2. Alignment of evaluate.py Scripts (Challenge 0 vs Challenge 2)

**Priority**: LOW  
**Reason**: Your scripts work correctly, just minor naming differences

**Changes**:
- Standardize on `/chat` endpoint (your version is correct)
- Keep `BACKEND_URI` environment variable name

#### 3. redteammh.py Import Organization

**Priority**: VERY LOW  
**Reason**: Current structure works, just different style

Your approach (imports in `__main__`):
```python
if __name__ == "__main__":
    from azure.identity import DefaultAzureCredential
    from azure.ai.evaluation.red_team import RedTeam, RiskCategory
    # ...
```

Challenge 2 approach (imports at top):
```python
from azure.identity import DefaultAzureCredential
from azure.ai.evaluation.red_team import RedTeam, RiskCategory
# ...
```

**Recommendation**: Keep your current structure - it's safer for multiprocessing scenarios

---

## 5. Documentation Completeness Comparison

| Feature | Your RBAC Docs | Challenge 1 README |
|---------|---------------|-------------------|
| Step-by-step portal instructions | ✅ Detailed | ✅ Basic |
| CLI commands with parameters | ✅ Complete | ❌ Missing |
| Troubleshooting section | ✅ Comprehensive | ❌ None |
| Error messages documented | ✅ All errors | ❌ None |
| Parent vs project identity | ✅ Explicitly called out | ❌ Not mentioned |
| Third role documented | ✅ Search Index Data Reader | ❌ Missing |
| Agent recreation guidance | ✅ Included | ❌ Missing |
| Success criteria | ✅ Detailed | ✅ Listed |
| Example test queries | ✅ Provided | ✅ Provided |
| Automation script | ✅ Complete script | ❌ None |

**Overall**: Your documentation is significantly more comprehensive than the Challenge 1 README.

---

## 6. Summary of Findings

### ✅ What's Working (No Changes Needed)

1. **evaluatemh.py** - Correct, uses `/chat` endpoint and `BACKEND_URI`
2. **safety_evaluationmh.py** - Correct, matches Challenge 2 pattern
3. **redteammh.py** - Functionally correct, minor style difference
4. **FOUNDRY-AGENT-SEARCH-RBAC-SETUP.md** - Comprehensive, accurate, better than README

### ⚠️ What Needs Updating

1. **SET_RBAC.sh** - Must target PROJECT identity, not parent resource
   - **Action**: Update script to prompt for project principal ID
   - **Impact**: High - critical for agent functionality

2. **Challenge 1 README** - Missing critical information
   - **Not your responsibility** but worth noting:
     - Missing "Search Index Data Reader" role
     - Missing parent vs project identity distinction
     - Missing CLI automation examples

### 🎯 Recommended Actions

**Priority 1**: Update SET_RBAC.sh
- Add project principal ID input prompt
- Add warning about parent vs project identity
- Keep all three roles

**Priority 2**: Consider creating a PR to Challenge 1 README
- Add missing "Search Index Data Reader" role
- Add note about parent vs project identity
- Reference your comprehensive documentation

**Priority 3**: Document script differences
- Note that your scripts use `/chat` vs Challenge 2's `/ask`
- Both are valid endpoints for testing

---

## 7. Script Comparison Matrix

| Script | Challenge 0 (Yours) | Challenge 2 (Reference) | Endpoint | Status |
|--------|-------------------|----------------------|----------|---------|
| evaluate | evaluatemh.py | evaluate.py | /chat vs /ask | ✅ Both work |
| safety | safety_evaluationmh.py | safety_evaluation.py | /chat | ✅ Match |
| redteam | redteammh.py | redteam.py | /chat vs /ask | ✅ Both work |
| RBAC | SET_RBAC.sh | (none) | N/A | ⚠️ Needs update |

---

## 8. Key Learnings for Future Reference

### What You Discovered That's Not in README

1. **Foundry agents use PROJECT managed identity**, not parent resource identity
2. **Three roles required**, not two (README missing Search Index Data Reader)
3. **Agent recreation required** after RBAC changes (connections are cached)
4. **Azure CLI limitations** - can't directly query Foundry project principal IDs
5. **Portal method more reliable** than CLI for project identity assignments

### Best Practices You Established

1. Always assign roles to PROJECT identity via portal first
2. Enable "Both" authentication mode on search service
3. Wait 1-2 minutes for role propagation
4. Delete and recreate agent after RBAC changes
5. Use portal IAM view to verify all three roles

---

**Status**: ✅ Analysis complete  
**Next Step**: Update SET_RBAC.sh script to prompt for project principal ID  
**Documentation**: Your RBAC guide is production-ready and more comprehensive than official README

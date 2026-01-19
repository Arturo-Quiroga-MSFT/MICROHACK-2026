# Evaluations references (Foundry + SDKs)

Saved: 2026-01-16

## Links
- Azure SDK for Python – `azure-ai-evaluation` source: https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/evaluation/azure-ai-evaluation
- Foundry Classic – Evaluate SDK how-to: https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/evaluate-sdk?view=foundry-classic
- Python API overview – Azure AI Evaluation: https://learn.microsoft.com/en-us/python/api/overview/azure/ai-evaluation-readme?view=azure-python&viewFallbackFrom=foundry

## Notes (to be filled)
- Goal: Understand which evaluation APIs populate Foundry UI and how programmatic runs map to portal objects.
- Hypothesis: Foundry UI “Evaluations” are created via `azure.ai.evaluation.evaluate(..., azure_ai_project=...)` (or related project-aware APIs), while OpenAI `client.evals.*` runs are a different backend and may not surface in Foundry UI.

## Findings
- The Foundry portal “Evaluations” UI is populated by runs created via the Azure AI Evaluation SDK, e.g. `azure.ai.evaluation.evaluate(..., azure_ai_project=...)`.
- These SDK runs return a `studio_url` (direct deep link) and can be authenticated without API keys by passing a `TokenCredential` (e.g. `DefaultAzureCredential`) into evaluator constructors.
- OpenAI `client.evals.*` evaluations/runs created via the project OpenAI client may succeed and produce results, but they do not appear in Foundry “Evaluations” (likely a different backend/registry).

### Legacy vs New Foundry portal visibility (2026-01-16)
- Evaluations created via `azure.ai.evaluation.evaluate(..., azure_ai_project=...)` appear in the **Foundry Classic / legacy** Evaluation experience.
- The same evaluation does **not** currently appear in the **New Foundry (preview)** Evaluations list.
- Working assumption: the New Foundry (preview) “Evaluations” page is not yet fully wired up to all evaluation run backends that feed the legacy experience, or it is scoped to a different evaluation object type.
- Practical impact: use `studio_url` (or the legacy Evaluation page) as the source of truth for these runs until the preview UI converges.

### Cloud evaluation (AI Foundry Evaluations REST API) experiment (2026-01-16)
- Created an evaluation run via the AI Foundry Evaluations REST API (`POST {projectEndpoint}/evaluations/runs:run?api-version=2025-05-15-preview`) using Entra ID (`https://ai.azure.com/.default`).
- Result: this cloud evaluation run shows up in the **Foundry Classic / legacy** Evaluation experience.
- Result: it still does **not** show up in the **New Foundry (preview)** Evaluations list (as of 2026-01-16).
- Script: `AQ-CONTENT/sdk-test/test_foundry_cloud_evaluation_rest.py`

### New Foundry (preview) portal visibility mystery - SOLVED! 🎯 (2026-01-16)

**Discovery**: The New Foundry (preview) Evaluations UI filters OpenAI evals objects by `properties.evals_run_type == "azure_ai"`

#### Investigation Process

1. **Observed**: Portal-created eval `eval-1r8lmh2d` appears in New Foundry (preview), but our programmatically-created evals don't
2. **Examined**: Retrieved full JSON of `eval-1r8lmh2d` and compared with our programmatic evals
3. **Key Difference Found**:
   - `eval-1r8lmh2d` (UI-created, **visible in New Foundry preview**):
     ```json
     {
       "id": "eval_eaddad056c564d4a8bb016c7d2eed424",
       "object": "eval",
       "properties": {
         "evals_run_type": "azure_ai"  ← This is the filter!
       },
       "testing_criteria": [
         {
           "type": "azure_ai_evaluator",
           "evaluator_name": "builtin.coherence"
         }
       ]
     }
     ```
   - Our programmatic evals via `test_eval.py` (**NOT visible in New Foundry preview**):
     ```json
     {
       "id": "eval_696a7513761c819192ab3d48b63f3ea5",
       "object": "eval",
       "properties": {},  ← No evals_run_type property
       "testing_criteria": [
         {
           "type": "label_model"
         }
       ]
     }
     ```

4. **Testing**: Attempted to create eval with `properties.evals_run_type="azure_ai"` via:
   - OpenAI evals REST API: ❌ Returns `400 Bad Request: Unknown parameter: 'properties'`
   - The `properties` field appears to be set by the Foundry UI backend, not accessible via public APIs

#### Two Types of Evaluations

| Type | Creation Method | OpenAI evals API | Properties | New Foundry Preview | Legacy Portal |
|------|----------------|------------------|------------|---------------------|---------------|
| **label_model evals** | `client.evals.create()` with label_model | ✅ Accessible | Empty `{}` | ❌ Not visible | ❌ Not visible |
| **azure_ai evals** | Foundry Portal UI (or internal API) | ✅ Accessible (read) | `{"evals_run_type": "azure_ai"}` | ✅ Visible | ✅ Visible (via runs) |

#### Current Understanding

1. **New Foundry (preview) Evaluations page**:
   - Lists **OpenAI eval objects** (not Foundry Evaluations REST API runs)
   - Filters for `properties.evals_run_type == "azure_ai"`
   - This property can only be set by the portal UI during creation (no known programmatic method)

2. **Foundry Evaluations REST API** (`/evaluations/runs:run`):
   - Creates different object type (evaluation runs, not eval definitions)
   - Runs appear in **Legacy portal only**
   - Not related to the New Foundry preview UI at all (different backend)

3. **OpenAI evals API** (`client.evals.create()`):
   - Can create eval definitions programmatically
   - But cannot set the `properties.evals_run_type` field via API
   - Without that property, evals don't appear in New Foundry preview

#### Implications for Programmatic Monitoring

**To achieve New Foundry (preview) visibility programmatically**, we would need:
- Either an undocumented/internal API endpoint that accepts `properties` parameter
- Or a way to create evals through a Foundry SDK that sets this property
- Or accept that New Foundry preview visibility currently requires UI-based creation

**Current programmatic options**:
- ✅ **Legacy portal visibility**: Use Foundry Evaluations REST API or Azure AI Evaluation SDK
- ❌ **New Foundry preview visibility**: No known programmatic method as of 2026-01-16

**Files created during investigation**:
- `AQ-CONTENT/sdk-test/test_openai_eval_azure_ai_type.py`: Attempted azure_ai eval via REST (failed)
- Listed 10 existing OpenAI evals created by `test_eval.py` (all without azure_ai property, all invisible in New Foundry preview)

### Workspace proof
- Script: `AQ-CONTENT/sdk-test/test_foundry_evaluate_sdk.py`
- Output: `AQ-CONTENT/sdk-test/out/sdk-test-evaluate-sdk-*.results.jsonl`
- Example `studio_url` returned:
	- https://ai.azure.com/resource/build/evaluation/3a6bb856-793d-451f-8865-5f9969f6f6ff

## Next experiments
- Run an eval via `azure.ai.evaluation.evaluate()` with `azure_ai_project` and confirm it shows in Foundry UI.
- Compare IDs/URLs returned (e.g., `studio_url`) with Foundry navigation.

### Try a "cloud evaluation" via the Foundry SDK (potentially New Foundry-compatible)
- Run an evaluation using `azure.ai.projects.AIProjectClient` + `azure.ai.projects.models.Evaluation` / `EvaluatorConfiguration` (the "run evaluations in the cloud" flow).
- Check whether that evaluation shows up in the New Foundry (preview) Evaluations list.
- If it does, prefer this path for programmatic monitoring (polling run status) and New Foundry UI visibility.

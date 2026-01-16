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

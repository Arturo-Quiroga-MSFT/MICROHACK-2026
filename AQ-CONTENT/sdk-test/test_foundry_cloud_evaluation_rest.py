"""Submit a *cloud* Evaluation run to Foundry via the Evaluations REST API.

Why this exists:
- The local Azure AI Evaluation SDK (`azure.ai.evaluation.evaluate`) uploads results that appear in the
  legacy/Foundry Classic Evaluation UI, but may not show in the New Foundry (preview) Evaluations list.
- The AI Foundry Evaluations REST API (2025-05-15-preview) creates evaluation runs directly under the
  project and is a good candidate for New Foundry visibility.

Auth:
- Uses Microsoft Entra ID via DefaultAzureCredential (no Azure OpenAI API keys).

Docs:
- https://learn.microsoft.com/en-us/rest/api/aifoundry/aiprojects/evaluations/create
- https://learn.microsoft.com/en-us/rest/api/aifoundry/aiprojects/evaluations/list

Required env vars (matches sdk-test/.env):
- AZURE_AI_PROJECT_ENDPOINT
- AZURE_OPENAI_DEPLOYMENT (or AZURE_AI_MODEL_DEPLOYMENT_NAME)

Optional env vars:
- AZURE_AI_CONNECTION_NAME  (if your deployment is accessed via a connection)
- DATASET_NAME
- DATASET_VERSION
"""

from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import EvaluatorIds


API_VERSION = "2025-05-15-preview"
TOKEN_SCOPE = "https://ai.azure.com/.default"


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required env var: {name}")
    return value


def _compact(obj: Any) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True)


def _build_bearer_token(credential: DefaultAzureCredential) -> str:
    token = credential.get_token(TOKEN_SCOPE)
    return token.token


def _project_url(path_suffix: str) -> str:
    endpoint = _require_env("AZURE_AI_PROJECT_ENDPOINT").rstrip("/")
    return f"{endpoint}{path_suffix}"


def main() -> None:
    load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

    project_endpoint = _require_env("AZURE_AI_PROJECT_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT") or _require_env("AZURE_AI_MODEL_DEPLOYMENT_NAME")
    connection_name = os.getenv("AZURE_AI_CONNECTION_NAME")

    # The evaluation dataset should include at least a `query` field (and optionally `response`, `context`, etc.)
    data_path = Path(__file__).resolve().parent / "data" / "evaluate_test_data.jsonl"
    if not data_path.exists():
        raise FileNotFoundError(f"Missing JSONL data file: {data_path}")

    out_dir = Path(__file__).resolve().parent / "out"
    out_dir.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_UTC")
    evaluation_display_name = f"sdk-test-cloud-evaluation-{stamp}"

    dataset_name = os.getenv("DATASET_NAME") or f"sdk-test-cloud-eval-data-{stamp}"
    dataset_version = os.getenv("DATASET_VERSION") or "1"

    # Optional: If your model deployment is accessed via a connection, the API accepts:
    #   "{connectionName}/{modelDeploymentName}"
    model_deployment_ref = f"{connection_name}/{deployment_name}" if connection_name else deployment_name

    with DefaultAzureCredential(exclude_interactive_browser_credential=False) as credential:
        print(f"Project endpoint: {project_endpoint}")
        print(f"Model deployment ref: {model_deployment_ref}")
        print(f"Data: {data_path}")

        # 1) Upload dataset so the evaluation run can reference it
        with AIProjectClient(endpoint=project_endpoint, credential=credential) as project_client:
            dataset = project_client.datasets.upload_file(
                name=dataset_name,
                version=dataset_version,
                file_path=str(data_path),
            )

        if not getattr(dataset, "id", None):
            raise RuntimeError("Dataset upload returned no id.")

        print(f"Uploaded dataset id: {dataset.id}")

        # 2) Create evaluation run via REST API
        # Endpoint: POST {project_endpoint}/evaluations/runs:run?api-version=2025-05-15-preview
        create_url = _project_url(f"/evaluations/runs:run?api-version={API_VERSION}")
        token = _build_bearer_token(credential)

        # NOTE: `target` is optional. Here we evaluate existing columns from the dataset.
        # The AI-assisted evaluators still need a judge deployment specified in initParams.
        request_body: dict[str, Any] = {
            "displayName": evaluation_display_name,
            "description": "Created via Evaluations REST API (cloud evaluation run).",
            "data": {"type": "dataset", "id": dataset.id},
            "tags": {
                "source": "sdk-test",
                "api": "aiprojects/evaluations.create",
                "ui_goal": "new-foundry-visibility",
            },
            "evaluators": {
                "coherence": {
                    "id": EvaluatorIds.COHERENCE.value,
                    "initParams": {"deployment_name": deployment_name},
                    "dataMapping": {
                        "query": "${data.query}",
                        "response": "${data.response}",
                    },
                },
                "relevance": {
                    "id": EvaluatorIds.RELEVANCE.value,
                    "initParams": {"deployment_name": deployment_name},
                    "dataMapping": {
                        "query": "${data.query}",
                        "response": "${data.response}",
                        "context": "${data.context}",
                    },
                },
                "intent_resolution": {
                    "id": EvaluatorIds.INTENT_RESOLUTION.value,
                    "initParams": {"deployment_name": deployment_name},
                    "dataMapping": {
                        "query": "${data.query}",
                        "response": "${data.response}",
                    },
                },
            },
        }

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        print("\nSubmitting cloud evaluation run...")
        resp = requests.post(create_url, headers=headers, json=request_body, timeout=120)
        if resp.status_code not in (200, 201):
            raise RuntimeError(
                "Cloud evaluation create failed. "
                f"HTTP {resp.status_code}: {resp.text[:4000]}"
            )

        created = resp.json()
        out_path = out_dir / f"{evaluation_display_name}.create_response.json"
        out_path.write_text(_compact(created), encoding="utf-8")

        print("\nCreate response (saved):")
        print(f"- {out_path}")
        print("\nCreate response (id/status):")
        print(f"- id: {created.get('id')}")
        print(f"- status: {created.get('status')}")

        # 3) List runs (helps confirm server-side registration quickly)
        list_url = _project_url(f"/evaluations/runs?api-version={API_VERSION}")
        list_resp = requests.get(list_url, headers=headers, timeout=60)
        if list_resp.status_code == 200:
            listing = list_resp.json()
            value = listing.get("value") or []
            print(f"\nList runs returned {len(value)} items (showing up to 5):")
            for item in value[:5]:
                print(f"- {item.get('displayName')} | {item.get('status')} | {item.get('id')}")
        else:
            print(f"\nList runs failed HTTP {list_resp.status_code}: {list_resp.text[:500]}")

        print("\nNext: check New Foundry (preview) -> Evaluations list for:")
        print(f"  {evaluation_display_name}")

        # tiny sleep to flush prints in some terminals
        time.sleep(0.1)


if __name__ == "__main__":
    main()

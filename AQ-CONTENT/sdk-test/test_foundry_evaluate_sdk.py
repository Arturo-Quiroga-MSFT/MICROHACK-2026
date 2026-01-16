"""Run Azure AI Evaluation SDK and upload results to Foundry.

This uses azure.ai.evaluation.evaluate(..., azure_ai_project=...) which is the API surface
that publishes evaluations into the Foundry portal UI, and supports Entra ID auth by
passing a TokenCredential (no API key).
"""

from __future__ import annotations

import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from azure.identity import DefaultAzureCredential


def _require_env(name: str) -> str:
	value = os.getenv(name)
	if not value:
		raise ValueError(f"Missing required env var: {name}")
	return value


def _print_compact(obj: Any) -> None:
	print(json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True))


def main() -> None:
	load_dotenv()

	project_endpoint = _require_env("AZURE_AI_PROJECT_ENDPOINT")
	aoai_endpoint = _require_env("AZURE_OPENAI_ENDPOINT")
	aoai_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT") or _require_env("AZURE_AI_MODEL_DEPLOYMENT_NAME")

	data_path = Path(__file__).resolve().parent / "data" / "evaluate_test_data.jsonl"
	if not data_path.exists():
		raise FileNotFoundError(f"Missing JSONL data file: {data_path}")

	out_dir = Path(__file__).resolve().parent / "out"
	out_dir.mkdir(parents=True, exist_ok=True)

	stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
	evaluation_name = f"sdk-test-evaluate-sdk-{stamp}"
	output_path = out_dir / f"{evaluation_name}.results.jsonl"

	credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)

	try:
		from azure.ai.evaluation import CoherenceEvaluator, IntentResolutionEvaluator, RelevanceEvaluator, evaluate
		from azure.ai.evaluation import AzureOpenAIModelConfiguration
	except ModuleNotFoundError as ex:
		raise ModuleNotFoundError(
			"azure-ai-evaluation is not installed in the active environment. "
			"Install it (e.g., `pip install azure-ai-evaluation`) and retry."
		) from ex

	model_config = AzureOpenAIModelConfiguration(
		azure_endpoint=aoai_endpoint,
		azure_deployment=aoai_deployment,
	)

	evaluators = {
		"coherence": CoherenceEvaluator(model_config=model_config, credential=credential),
		"relevance": RelevanceEvaluator(model_config=model_config, credential=credential),
		"intent_resolution": IntentResolutionEvaluator(model_config=model_config, credential=credential),
	}

	evaluator_config = {
		"coherence": {
			"column_mapping": {
				"query": "${data.query}",
				"response": "${data.response}",
			}
		},
		"relevance": {
			"column_mapping": {
				"query": "${data.query}",
				"response": "${data.response}",
				"context": "${data.context}",
			}
		},
		"intent_resolution": {
			"column_mapping": {
				"query": "${data.query}",
				"response": "${data.response}",
			}
		},
	}

	print(f"Project endpoint: {project_endpoint}")
	print(f"Azure OpenAI endpoint: {aoai_endpoint}")
	print(f"Azure OpenAI deployment: {aoai_deployment}")
	print(f"Data: {data_path}")
	print(f"Output: {output_path}\n")

	result = evaluate(
		data=str(data_path),
		evaluators=evaluators,
		evaluator_config=evaluator_config,
		evaluation_name=evaluation_name,
		azure_ai_project=project_endpoint,
		output_path=str(output_path),
		tags={"source": "sdk-test", "api": "azure.ai.evaluation.evaluate"},
	)

	print("\nMetrics:")
	_print_compact(result.get("metrics", {}))

	rows = result.get("rows") or []
	if rows:
		print("\nFirst row:")
		_print_compact(rows[0])

	studio_url = result.get("studio_url")
	if studio_url:
		print("\nFoundry studio_url:")
		print(studio_url)

	print("\nDone.")
	print(f"Saved local results to: {output_path}")

	time.sleep(0.1)


if __name__ == "__main__":
	main()

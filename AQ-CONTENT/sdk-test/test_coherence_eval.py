"""
Test script to create evaluations programmatically with Coherence, Relevance, 
and Intent Resolution evaluators (matching the original sample).
"""
import os
import time
import json
from pprint import pprint
from dotenv import load_dotenv

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from openai.types.evals.create_eval_jsonl_run_data_source_param import (
    CreateEvalJSONLRunDataSourceParam,
    SourceFileContent,
    SourceFileContentContent,
)
from openai.types.eval_create_params import DataSourceConfigCustom

# Load environment variables
load_dotenv()

def main():
    endpoint = os.environ.get("AZURE_AI_PROJECT_ENDPOINT")
    model_deployment_name = os.environ.get("AZURE_AI_MODEL_DEPLOYMENT_NAME")

    if not endpoint or not model_deployment_name:
        raise ValueError("Missing required env vars: AZURE_AI_PROJECT_ENDPOINT, AZURE_AI_MODEL_DEPLOYMENT_NAME")
    
    print(f"Connecting to: {endpoint}")
    print(f"Using model: {model_deployment_name}\n")
    
    with (
        DefaultAzureCredential() as credential,
        AIProjectClient(endpoint=endpoint, credential=credential) as project_client,
        project_client.get_openai_client(api_version="2025-04-01-preview") as client,
    ):
        # Define the data schema
        data_source_config = DataSourceConfigCustom(
            {
                "type": "custom",
                "item_schema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "response": {"type": "string"},
                        "context": {"type": "string"},
                    },
                    "required": ["query", "response"],
                },
                "include_sample_schema": False,
            }
        )

        # Upload the test data file (use timestamp to avoid conflicts)
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        data_file_path = "./data/evaluate_test_data.jsonl"
        if not os.path.exists(data_file_path):
            raise FileNotFoundError(f"Data file not found: {data_file_path}")
        print(f"Uploading dataset from {data_file_path}...")
        dataset = project_client.datasets.upload_file(
            file_path=data_file_path,
            name=f"sdk_test_coherence_data_{timestamp}",
            version="1"
        )
        print(f"✓ Dataset uploaded (id: {dataset.id})\n")

        # Read JSONL content for eval run (avoids file_id errors)
        file_content_items: list[SourceFileContentContent] = []
        with open(data_file_path, "r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                item = json.loads(line)
                file_content_items.append(SourceFileContentContent(item=item))
        
        # Define evaluators to use - three evaluators like the original sample
        testing_criteria = [
            {
                "type": "label_model",
                "name": "coherence",
                "model": model_deployment_name,
                "input": [
                    {"content": "{{item.query}}", "role": "user"},
                    {"content": "{{item.response}}", "role": "assistant"}
                ],
                "labels": ["1", "2", "3", "4", "5"],
                "passing_labels": ["5", "4", "3"]
            },
            {
                "type": "label_model",
                "name": "relevance",
                "model": model_deployment_name,
                "input": [
                    {"content": "{{item.query}}", "role": "user"},
                    {"content": "{{item.response}}", "role": "assistant"},
                    {"content": "{{item.context}}", "role": "system"}
                ],
                "labels": ["1", "2", "3", "4", "5"],
                "passing_labels": ["5", "4", "3"]
            },
            {
                "type": "label_model",
                "name": "intent_resolution",
                "model": model_deployment_name,
                "input": [
                    {"content": "{{item.query}}", "role": "user"},
                    {"content": "{{item.response}}", "role": "assistant"}
                ],
                "labels": ["1", "2", "3", "4", "5"],
                "passing_labels": ["5", "4", "3"]
            }
        ]

        print("Creating Evaluation with 3 evaluators (Coherence, Relevance, Intent Resolution)...")
        eval_object = client.evals.create(
            name="SDK Test - Multi-Evaluator (Coherence, Relevance, Intent)",
            data_source_config=data_source_config,
            testing_criteria=testing_criteria,  # type: ignore
        )
        print(f"✓ Evaluation created (id: {eval_object.id}, name: {eval_object.name})\n")

        print("Creating Eval Run with uploaded dataset...")
        eval_run_object = None
        for attempt in range(1, 4):
            try:
                eval_run_object = client.evals.runs.create(
                    eval_id=eval_object.id,
                    name="sdk_test_run",
                    metadata={"test": "sdk_creation", "created_by": "evaluation_checker"},
                    data_source=CreateEvalJSONLRunDataSourceParam(
                        type="jsonl",
                        source=SourceFileContent(content=file_content_items, type="file_content"),
                    ),
                )
                break
            except Exception as ex:
                if attempt == 3:
                    raise
                print(f"Run creation failed (attempt {attempt}/3). Retrying in 5s...\n{ex}")
                time.sleep(5)
        if eval_run_object is None:
            raise RuntimeError("Failed to create eval run after retries.")
        print(f"✓ Eval Run created (id: {eval_run_object.id})\n")

        print(f"{'='*80}")
        print(f"Evaluation Details:")
        print(f"{'='*80}")
        print(f"Eval ID: {eval_object.id}")
        print(f"Run ID: {eval_run_object.id}")
        print(f"Status: {eval_run_object.status}")
        print(f"\nPortal URL (approximate):")
        print(f"https://ai.azure.com/resource/build/evaluation/{eval_object.id}")
        print(f"{'='*80}\n")

        # Monitor the run
        print("Monitoring evaluation run...")
        iteration = 0
        while True:
            iteration += 1
            run = client.evals.runs.retrieve(run_id=eval_run_object.id, eval_id=eval_object.id)
            print(f"Check #{iteration}: Status = {run.status}")
            
            if run.status in ("completed", "failed", "canceled"):
                print(f"\n✓ Evaluation {run.status}!")
                
                if hasattr(run, 'result_counts'):
                    print(f"Result counts: {run.result_counts}")
                
                if hasattr(run, 'report_url'):
                    print(f"Report URL: {run.report_url}")
                
                # Get results if completed or failed
                if run.status in ("completed", "failed"):
                    print("\nFetching results...")
                    output_items = list(client.evals.runs.output_items.list(run_id=run.id, eval_id=eval_object.id))
                    print(f"Total output items: {len(output_items)}")
                    if output_items:
                        print("\nFirst result sample:")
                        pprint(output_items[0])
                
                break
                
            time.sleep(5)

        print(f"\n{'='*80}")
        print("Test Complete!")
        print(f"{'='*80}")
        print("\nNext steps:")
        print("1. Check the Foundry portal to see this evaluation")
        print("2. Compare the eval_id with your portal evaluation")
        print("3. Try listing evaluations to see if portal ones appear")

if __name__ == "__main__":
    main()

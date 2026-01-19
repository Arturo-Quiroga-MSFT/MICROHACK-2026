#!/usr/bin/env python3
"""
Create an OpenAI eval object with properties.evals_run_type="azure_ai"
to make it visible in the New Foundry (preview) portal.

This mimics the structure of eval-1r8lmh2d which IS visible in the new portal.
Uses direct REST API since Python client doesn't support properties parameter.
"""
from dotenv import load_dotenv
load_dotenv()

import os
import json
import requests
from datetime import datetime, timezone
from azure.identity import DefaultAzureCredential

# Load config
endpoint = os.environ['AZURE_AI_PROJECT_ENDPOINT']
deployment = os.environ['AZURE_OPENAI_DEPLOYMENT']
aoai_endpoint = os.environ['AZURE_OPENAI_ENDPOINT']

print(f'Project endpoint: {endpoint}')
print(f'AOAI endpoint: {aoai_endpoint}')
print(f'Model deployment: {deployment}')
print()

# Get bearer token
credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
token = credential.get_token('https://cognitiveservices.azure.com/.default')

# Create eval with azure_ai properties
timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
eval_name = f"sdk-test-new-foundry-visible-{timestamp}"

print(f'Creating eval via REST: {eval_name}')

# Create eval matching the structure of eval-1r8lmh2d
payload = {
    "name": eval_name,
    "properties": {
        "evals_run_type": "azure_ai"  # This is the key property!
    },
    "data_source_config": {
        "type": "custom",
        "include_sample_schema": True,
        "schema": {
            "item": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "truth": {"type": "string"}
                },
                "required": []
            },
            "sample": {
                "type": "object",
                "properties": {
                    "output_text": {"type": "string"}
                }
            }
        }
    },
    "testing_criteria": [
        {
            "type": "azure_ai_evaluator",
            "name": "Coherence",
            "evaluator_name": "builtin.coherence",
            "evaluator_version": "",
            "initialization_parameters": {
                "deployment_name": deployment,
                "threshold": 3
            },
            "data_mapping": {
                "query": "{{item.question}}",
                "response": "{{sample.output_text}}",
                "context": "{{item.truth}}",
                "ground_truth": "{{item.truth}}"
            }
        },
        {
            "type": "azure_ai_evaluator",
            "name": "Relevance",
            "evaluator_name": "builtin.relevance",
            "evaluator_version": "",
            "initialization_parameters": {
                "deployment_name": deployment,
                "threshold": 3
            },
            "data_mapping": {
                "query": "{{item.question}}",
                "response": "{{sample.output_text}}",
                "context": "{{item.truth}}",
                "ground_truth": "{{item.truth}}"
            }
        },
        {
            "type": "azure_ai_evaluator",
            "name": "IntentResolution",
            "evaluator_name": "builtin.intent_resolution",
            "evaluator_version": "",
            "initialization_parameters": {
                "deployment_name": deployment,
                "threshold": 3
            },
            "data_mapping": {
                "query": "{{item.question}}",
                "response": "{{sample.output_text}}",
                "context": "{{item.truth}}",
                "ground_truth": "{{item.truth}}"
            }
        }
    ]
}

# POST to OpenAI evals API
url = f'{aoai_endpoint}/openai/evals?api-version=2025-04-01-preview'
headers = {
    'Authorization': f'Bearer {token.token}',
    'Content-Type': 'application/json'
}

print(f'POST {url}')
response = requests.post(url, headers=headers, json=payload)

if response.status_code != 200:
    print(f'ERROR: {response.status_code}')
    print(f'Response: {response.text}')
    
response.raise_for_status()

eval_obj = response.json()

print(f'✓ Created eval:')
print(f'  ID: {eval_obj["id"]}')
print(f'  Name: {eval_obj["name"]}')
if 'properties' in eval_obj:
    print(f'  Properties: {eval_obj["properties"]}')
print()

# Save full response
os.makedirs('out', exist_ok=True)
output_path = f'out/{eval_name}.eval_create_response.json'

with open(output_path, 'w') as f:
    json.dump(eval_obj, f, indent=2)
print(f'✓ Saved full eval object to: {output_path}')
print()

print('=' * 80)
print('NEXT STEP:')
print(f'1. Check if this eval appears in New Foundry (preview) portal')
print(f'2. The eval ID is: {eval_obj["id"]}')
print(f'3. This eval has properties.evals_run_type="azure_ai" which should make it visible')
print('=' * 80)

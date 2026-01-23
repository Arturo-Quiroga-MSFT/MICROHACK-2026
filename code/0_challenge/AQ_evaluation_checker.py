import os
import time
import sys
from azure.identity import AzureDeveloperCliCredential
from azure.ai.projects import AIProjectClient
from datetime import datetime

# ============================================================================
# CONFIGURATION - Update these values for YOUR evaluation
# ============================================================================

# Get your project endpoint from Azure Portal → Foundry → Project → Overview
# Format: https://<resource-name>.services.ai.azure.com/api/projects/<project-name>

# Option 1: microhack2 project (default)
# endpoint = "https://cog-mfm4mgxglrqua.services.ai.azure.com/api/projects/microhack2-project"

# Option 2: r2d2-foundry-001 / Main-Project (HEALTHCARE-ASSISTANT eval)
endpoint = "https://r2d2-foundry-001.services.ai.azure.com/api/projects/Main-Project"

# Optional: override from environment
endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT", endpoint)

# Get eval_id and run_id from the evaluation JSON or Foundry portal
# From the JSON: look for "eval_id" and "id" (which is the run_id)
eval_id = os.getenv("EVAL_ID", "eval_4d1e03bf58e3469e8455d4ac85a61faf")
run_id = os.getenv("EVAL_RUN_ID", "evalrun_97c5ba0843ee4951959fb295d701c2fe")

tenant_id = os.getenv("AZURE_TENANT_ID", "a172a259-b1c7-4944-b2e1-6d551f954711")
if tenant_id:
    credential = AzureDeveloperCliCredential(tenant_id=tenant_id, process_timeout=60)
else:
    credential = AzureDeveloperCliCredential(process_timeout=60)

# ============================================================================

print("="*80)
print(f"Monitoring Evaluation Run")
print("="*80)
print(f"Endpoint: {endpoint}")
print(f"Eval ID:  {eval_id}")
print(f"Run ID:   {run_id}")
print(f"Started:  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)
print()

# Validate configuration
if not eval_id or not run_id:
    print("❌ Error: Both eval_id and run_id must be set in the script")
    print("   Update the values at the top of the script")
    sys.exit(1)

try:
    project_client = AIProjectClient(endpoint=endpoint, credential=credential)
except Exception as e:
    print(f"❌ Error connecting to project: {e}")
    print("   Check that your endpoint URL is correct")
    sys.exit(1)

with project_client:
    # Get the OpenAI client
    client = project_client.get_openai_client(api_version="2025-04-01-preview")
    
    # Get initial run details
    print("Fetching run details...")
    try:
        run = client.evals.runs.retrieve(run_id=run_id, eval_id=eval_id)
        print(f"Agent: {run.name}")
        print(f"Initial status: {run.status}")
        
        if hasattr(run, 'data_source') and hasattr(run.data_source, 'target'):
            target = run.data_source.target
            if hasattr(target, 'name') and hasattr(target, 'version'):
                print(f"Target: {target.name} (version {target.version})")
        
        print()
    except Exception as e:
        print("❌ Error: Could not find evaluation")
        print(f"   {e}")
        print()
        print("🔍 Attempting to find the eval_id by run_id...")
        try:
            evals = client.evals.list(limit=25)
            found_eval_id = None
            if evals.data:
                for e in evals.data:
                    try:
                        runs = client.evals.runs.list(eval_id=e.id, order="desc", limit=5)
                        for r in runs.data:
                            if r.id == run_id:
                                found_eval_id = e.id
                                break
                        if found_eval_id:
                            break
                    except Exception:
                        continue
            
            if found_eval_id:
                print(f"✅ Found matching eval_id: {found_eval_id}")
                eval_id = found_eval_id
                run = client.evals.runs.retrieve(run_id=run_id, eval_id=eval_id)
                print(f"Agent: {run.name}")
                print(f"Initial status: {run.status}")
                print()
            else:
                print("   No matching eval_id found for this run_id.")
                print("   Recent eval IDs:")
                for e in evals.data:
                    print(f"   - {e.id}")
                print()
                print("💡 Troubleshooting:")
                print("   1. Confirm eval_id/run_id pair from the same project")
                print("   2. Verify endpoint matches where the evaluation was created")
                print("   3. Ensure you have permissions to view this evaluation")
                sys.exit(1)
        except Exception as list_error:
            print(f"   Could not list evaluations: {list_error}")
            print()
            print("🔧 Quick fix options:")
            print("   - Ensure you are logged into the correct tenant (azd/az login)")
            print("   - Try setting AZURE_AI_PROJECT_ENDPOINT, EVAL_ID, EVAL_RUN_ID env vars")
            sys.exit(1)
    
    # Poll until complete
    iteration = 0
    last_counts = {"total": 0, "passed": 0, "failed": 0, "errored": 0}
    
    while True:
        iteration += 1
        
        try:
            run = client.evals.runs.retrieve(run_id=run_id, eval_id=eval_id)
            timestamp = datetime.now().strftime('%H:%M:%S')
            
            # Display status with progress
            status_line = f"[{timestamp}] Check #{iteration}: Status = {run.status}"
            
            if hasattr(run, 'result_counts') and run.result_counts:
                counts = run.result_counts
                if counts.get('total', 0) > last_counts['total']:
                    # Progress detected - show detailed counts
                    total = counts.get('total', 0)
                    passed = counts.get('passed', 0)
                    failed = counts.get('failed', 0)
                    errored = counts.get('errored', 0)
                    
                    status_line += f" | Progress: {total} total"
                    if passed > 0:
                        status_line += f", {passed} ✓"
                    if failed > 0:
                        status_line += f", {failed} ✗"
                    if errored > 0:
                        status_line += f", {errored} ⚠️"
                    
                    last_counts = counts.copy()
            
            print(status_line)
            
            if run.status in ("completed", "failed", "canceled"):
                print()
                print("="*80)
                print(f"Evaluation {run.status.upper()}!")
                print("="*80)
                
                if hasattr(run, 'result_counts') and run.result_counts:
                    counts = run.result_counts
                    print(f"\nResults:")
                    print(f"  Total:   {counts.get('total', 0)}")
                    print(f"  Passed:  {counts.get('passed', 0)} ✓")
                    print(f"  Failed:  {counts.get('failed', 0)} ✗")
                    print(f"  Errored: {counts.get('errored', 0)} ⚠️")
                
                if hasattr(run, 'report_url') and run.report_url:
                    print(f"\n📊 Report URL:")
                    print(f"   {run.report_url}")
                
                # Get output items if completed
                if run.status == "completed":
                    print(f"\n📥 Fetching output items...")
                    try:
                        output_items = list(client.evals.runs.output_items.list(run_id=run.id, eval_id=eval_id))
                        print(f"   Total output items: {len(output_items)}")
                    except Exception as e:
                        print(f"   Could not fetch output items: {e}")
                
                print("="*80)
                break
                
            time.sleep(10)  # Check every 10 seconds
            
        except Exception as e:
            print(f"\n❌ Error checking evaluation: {e}")
            break

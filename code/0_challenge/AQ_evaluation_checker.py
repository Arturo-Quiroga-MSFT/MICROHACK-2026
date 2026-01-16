import time
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from datetime import datetime

# Setup
endpoint = "https://cog-v2jd2jfni7slw.services.ai.azure.com/api/projects/cog-v2jd2jfni7slw-project"
credential = DefaultAzureCredential()
eval_id = "eval_eaddad056c564d4a8bb016c7d2eed424"

print(f"Monitoring evaluation: {eval_id}")
print(f"Started at: {datetime.now().strftime('%H:%M:%S')}\n")

with AIProjectClient(endpoint=endpoint, credential=credential) as project_client:
    # Get the OpenAI client
    client = project_client.get_openai_client(api_version="2025-04-01-preview")
    
    # List recent runs for this evaluation to find the run_id
    print("Looking for evaluation runs...")
    eval_run_list = client.evals.runs.list(eval_id=eval_id, order="desc", limit=5)
    
    if not eval_run_list.data:
        print("No evaluation runs found yet.")
        exit(1)
    
    # Get the most recent run
    latest_run = eval_run_list.data[0]
    run_id = latest_run.id
    print(f"Found run: {run_id}")
    print(f"Initial status: {latest_run.status}\n")
    
    # Poll until complete
    iteration = 0
    while True:
        iteration += 1
        
        try:
            run = client.evals.runs.retrieve(run_id=run_id, eval_id=eval_id)
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"[{timestamp}] Check #{iteration}: Status = {run.status}")
            
            if run.status in ("completed", "failed", "canceled"):
                print(f"\n{'='*80}")
                print(f"Evaluation {run.status}!")
                print(f"{'='*80}")
                print(f"Status: {run.status}")
                
                if hasattr(run, 'result_counts'):
                    print(f"Result counts: {run.result_counts}")
                
                if hasattr(run, 'report_url'):
                    print(f"Report URL: {run.report_url}")
                
                # Get output items if completed
                if run.status == "completed":
                    print("\nFetching output items...")
                    output_items = list(client.evals.runs.output_items.list(run_id=run.id, eval_id=eval_id))
                    print(f"Total output items: {len(output_items)}")
                
                break
                
            time.sleep(10)  # Check every 10 seconds
            
        except Exception as e:
            print(f"Error checking evaluation: {e}")
            break
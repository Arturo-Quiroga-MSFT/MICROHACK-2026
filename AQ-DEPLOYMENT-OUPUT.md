cd azure-search-openai-demo 
(.venv) (base) arturoquiroga@MacBookPro azure-search-openai-demo % 
(.venv) (base) arturoquiroga@MacBookPro azure-search-openai-demo % 
(.venv) (base) arturoquiroga@MacBookPro azure-search-openai-demo % 
(.venv) (base) arturoquiroga@MacBookPro azure-search-openai-demo % azd env new
? Enter a unique environment name: microhack2
New environment 'microhack2' was set as default
(.venv) (base) arturoquiroga@MacBookPro azure-search-openai-demo % 
(.venv) (base) arturoquiroga@MacBookPro azure-search-openai-demo % azd env set USE_EVAL true
(.venv) (base) arturoquiroga@MacBookPro azure-search-openai-demo % azd env set AZURE_OPENAI_EVAL_DEPLOYMENT_CAPACITY 200 
(.venv) (base) arturoquiroga@MacBookPro azure-search-openai-demo % azd up
? Select an Azure Subscription to use:  1. ARTURO-MngEnvMCAP094150 (7a28b21e-0d3e-4435-a686-d92889d4ee96)
? Enter a value for the 'documentIntelligenceResourceGroupLocation' infrastructure parameter:  3. (US) East US (eastus)
? Enter a value for the 'location' infrastructure parameter: 47. (US) East US 2 (eastus2)
? Enter a value for the 'openAiLocation' infrastructure parameter: 19. (US) East US 2 (eastus2)

Packaging services (azd package)

  (✓) Done: Packaging service backend
  - No artifacts were found

Checking if authentication should be setup...
AZURE_USE_AUTHENTICATION is not set, skipping authentication setup.

Provisioning Azure resources (azd provision)
Provisioning Azure resources can take some time.

Subscription: ARTURO-MngEnvMCAP094150 (7a28b21e-0d3e-4435-a686-d92889d4ee96)
Location: East US 2

  You can view detailed progress in the Azure Portal:
  https://portal.azure.com/#view/HubsExtension/DeploymentDetailsBlade/~/overview/id/%2Fsubscriptions%2F7a28b21e-0d3e-4435-a686-d92889d4ee96%2Fproviders%2FMicrosoft.Resources%2Fdeployments%2Fmicrohack2-1768590666

  (✓) Done: Resource group: rg-microhack2 (1.688s)
  (✓) Done: Log Analytics workspace: log-mfm4mgxglrqua (21.437s)
  (✓) Done: Storage account: stmfm4mgxglrqua (23.074s)
  (✓) Done: Azure OpenAI: cog-mfm4mgxglrqua (21.42s)
  (✓) Done: Azure AI Services Model Deployment: cog-mfm4mgxglrqua/text-embedding-3-large (1.75s)
  (✓) Done: Azure AI Services Model Deployment: cog-mfm4mgxglrqua/eval (2.547s)
  (✓) Done: Azure AI Services Model Deployment: cog-mfm4mgxglrqua/gpt-4.1-mini (875ms)
  (✓) Done: Application Insights: appi-mfm4mgxglrqua (3.715s)
  (✓) Done: Document Intelligence: cog-di-mfm4mgxglrqua (35.16s)
  (✓) Done: Portal dashboard: dash-mfm4mgxglrqua (498ms)
  (✓) Done: Container Registry: microhack2acrmfm4mgxglrqua (25.376s)
  (✓) Done: Container Apps Environment: microhack2-aca-env (1m57.862s)
  (✓) Done: Search service: gptkb-mfm4mgxglrqua (6m40.448s)
  (✓) Done: Container App: capps-backend-mfm4mgxglrqua (20.48s)
Creating Python virtual environment ".venv"...
Installing dependencies from "requirements.txt" into virtual environment (in quiet mode)...
Running "prepdocs.py"
[14:22:46] INFO     Loading azd env from /Users/arturoquiroga/MICROHACK-SAMPLE/azure-search-openai-demo/.azure/microhack2/.env, which may override existing         load_azd_env.py:28
                    environment variables                                                                                                                                             
           INFO     Connecting to Azure services using the azd credential for tenant a172a259-b1c7-4944-b2e1-6d551f954711                                              prepdocs.py:214
           INFO     Using local files: ./data/*                                                                                                                         prepdocs.py:75
           INFO     OPENAI_HOST is azure, setting up Azure OpenAI client                                                                                           servicesetup.py:105
           INFO     Using Azure credential (passwordless authentication) for Azure OpenAI client                                                                   servicesetup.py:114
[14:22:47] INFO     Checking whether search index gptkbindex exists...                                                                                             searchmanager.py:97
[14:22:49] INFO     Creating new search index gptkbindex                                                                                                          searchmanager.py:239
           INFO     Including embedding3 field for text vectors in new index                                                                                      searchmanager.py:297
[14:22:53] INFO     Uploading blob for document 'Zava_Company_Overview.md'                                                                                          blobmanager.py:431
           INFO     Ingesting 'Zava_Company_Overview.md'                                                                                                            filestrategy.py:36
           INFO     Splitting 'Zava_Company_Overview.md' into sections                                                                                             textprocessor.py:42
[14:22:56] INFO     Computed embeddings in batch. Batch size: 3, Token count: 518                                                                                    embeddings.py:120
           INFO     Uploading batch 1 with 3 sections to search index 'gptkbindex'                                                                                searchmanager.py:639
[14:22:57] INFO     Uploading blob for document 'Northwind_Standard_Benefits_Details.pdf'                                                                           blobmanager.py:431
[14:22:58] INFO     Ingesting 'Northwind_Standard_Benefits_Details.pdf'                                                                                             filestrategy.py:36
           INFO     Extracting text from './data/Northwind_Standard_Benefits_Details.pdf' using Azure Document Intelligence                                            pdfparser.py:66
[14:23:13] INFO     Splitting 'Northwind_Standard_Benefits_Details.pdf' into sections                                                                              textprocessor.py:42
[14:23:14] INFO     Computed embeddings in batch. Batch size: 16, Token count: 2497                                                                                  embeddings.py:120
           INFO     Computed embeddings in batch. Batch size: 16, Token count: 3118                                                                                  embeddings.py:120
[14:23:15] INFO     Computed embeddings in batch. Batch size: 16, Token count: 2781                                                                                  embeddings.py:120
           INFO     Computed embeddings in batch. Batch size: 16, Token count: 2553                                                                                  embeddings.py:120
           INFO     Computed embeddings in batch. Batch size: 16, Token count: 2768                                                                                  embeddings.py:120
           INFO     Computed embeddings in batch. Batch size: 16, Token count: 2893                                                                                  embeddings.py:120
[14:23:16] INFO     Computed embeddings in batch. Batch size: 16, Token count: 2595                                                                                  embeddings.py:120
           INFO     Computed embeddings in batch. Batch size: 16, Token count: 2701                                                                                  embeddings.py:120
           INFO     Computed embeddings in batch. Batch size: 16, Token count: 2699                                                                                  embeddings.py:120
[14:23:17] INFO     Computed embeddings in batch. Batch size: 16, Token count: 2917                                                                                  embeddings.py:120
           INFO     Computed embeddings in batch. Batch size: 16, Token count: 2673                                                                                  embeddings.py:120
           INFO     Computed embeddings in batch. Batch size: 16, Token count: 2737                                                                                  embeddings.py:120
           INFO     Computed embeddings in batch. Batch size: 16, Token count: 2707                                                                                  embeddings.py:120
[14:23:18] INFO     Computed embeddings in batch. Batch size: 16, Token count: 2791                                                                                  embeddings.py:120
           INFO     Computed embeddings in batch. Batch size: 16, Token count: 2788                                                                                  embeddings.py:120
           INFO     Computed embeddings in batch. Batch size: 16, Token count: 2735                                                                                  embeddings.py:120
[14:23:26] INFO     Computed embeddings in batch. Batch size: 16, Token count: 2515                                                                                  embeddings.py:120
[14:23:27] INFO     Computed embeddings in batch. Batch size: 16, Token count: 2677                                                                                  embeddings.py:120
           INFO     Computed embeddings in batch. Batch size: 16, Token count: 2568                                                                                  embeddings.py:120
           INFO     Computed embeddings in batch. Batch size: 1, Token count: 112                                                                                    embeddings.py:120
           INFO     Uploading batch 1 with 305 sections to search index 'gptkbindex'                                                                              searchmanager.py:639
[14:23:35] INFO     Uploading blob for document 'PerksPlus.pdf'                                                                                                     blobmanager.py:431
           INFO     Ingesting 'PerksPlus.pdf'                                                                                                                       filestrategy.py:36
           INFO     Extracting text from './data/PerksPlus.pdf' using Azure Document Intelligence                                                                      pdfparser.py:66
[14:23:41] INFO     Splitting 'PerksPlus.pdf' into sections                                                                                                        textprocessor.py:42
           INFO     Computed embeddings in batch. Batch size: 6, Token count: 592                                                                                    embeddings.py:120
           INFO     Uploading batch 1 with 6 sections to search index 'gptkbindex'                                                                                searchmanager.py:639
[14:23:42] INFO     Uploading blob for document 'Financial Market Analysis Report 2023.pdf'                                                                         blobmanager.py:431
           INFO     Ingesting 'Financial Market Analysis Report 2023.pdf'                                                                                           filestrategy.py:36
           INFO     Extracting text from './data/Multimodal_Examples/Financial Market Analysis Report 2023.pdf' using Azure Document Intelligence                      pdfparser.py:66
[14:23:49] INFO     Splitting 'Financial Market Analysis Report 2023.pdf' into sections                                                                            textprocessor.py:42
[14:23:50] INFO     Computed embeddings in batch. Batch size: 11, Token count: 1439                                                                                  embeddings.py:120
           INFO     Uploading batch 1 with 11 sections to search index 'gptkbindex'                                                                               searchmanager.py:639
[14:23:51] INFO     Uploading blob for document 'Northwind_Health_Plus_Benefits_Details.pdf'                                                                        blobmanager.py:431
           INFO     Ingesting 'Northwind_Health_Plus_Benefits_Details.pdf'                                                                                          filestrategy.py:36
           INFO     Extracting text from './data/Northwind_Health_Plus_Benefits_Details.pdf' using Azure Document Intelligence                                         pdfparser.py:66
[14:24:06] INFO     Splitting 'Northwind_Health_Plus_Benefits_Details.pdf' into sections                                                                           textprocessor.py:42
[14:24:07] INFO     Computed embeddings in batch. Batch size: 16, Token count: 2525                                                                                  embeddings.py:120
           INFO     Computed embeddings in batch. Batch size: 16, Token count: 2887                                                                       embeddings.py:120
           INFO     Computed embeddings in batch. Batch size: 16, Token count: 2948                                                                 embeddings.py:120
[14:24:08] INFO     Computed embeddings in batch. Batch size: 16, Token count: 2583                                                                 embeddings.py:120
           INFO     Computed embeddings in batch. Batch size: 16, Token count: 2648                                                                 embeddings.py:120
           INFO     Computed embeddings in batch. Batch size: 16, Token count: 2611                                                                   embeddings.py:120
[14:24:09] INFO     Computed embeddings in batch. Batch size: 16, Token count: 2600                                                                      embeddings.py:120
           INFO     Computed embeddings in batch. Batch size: 16, Token count: 2755                                                                      embeddings.py:120
[14:24:10] INFO     Computed embeddings in batch. Batch size: 16, Token count: 2547                                                                      embeddings.py:120
           INFO     Computed embeddings in batch. Batch size: 16, Token count: 2776                                                                      embeddings.py:120
           INFO     Computed embeddings in batch. Batch size: 16, Token count: 2741                                                                      embeddings.py:120
           INFO     Computed embeddings in batch. Batch size: 16, Token count: 2525                                                                      embeddings.py:120
[14:24:11] INFO     Computed embeddings in batch. Batch size: 16, Token count: 2802                                                                      embeddings.py:120
           INFO     Computed embeddings in batch. Batch size: 16, Token count: 2606                                                                      embeddings.py:120
[14:24:14] INFO     Computed embeddings in batch. Batch size: 16, Token count: 2857                                                                      embeddings.py:120
           INFO     Computed embeddings in batch. Batch size: 16, Token count: 2759                                                                      embeddings.py:120
           INFO     Computed embeddings in batch. Batch size: 16, Token count: 2714                                                                      embeddings.py:120
[14:24:15] INFO     Computed embeddings in batch. Batch size: 16, Token count: 2690                                                                      embeddings.py:120
           INFO     Computed embeddings in batch. Batch size: 16, Token count: 2563                                                                      embeddings.py:120
           INFO     Computed embeddings in batch. Batch size: 10, Token count: 1639                                                                      embeddings.py:120
           INFO     Uploading batch 1 with 314 sections to search index 'gptkbindex'                                                                  searchmanager.py:639
[14:24:22] INFO     Uploading blob for document 'role_library.pdf'                                                                                      blobmanager.py:431
[14:24:23] INFO     Ingesting 'role_library.pdf'                                                                                                        filestrategy.py:36
           INFO     Extracting text from './data/role_library.pdf' using Azure Document Intelligence                                                       pdfparser.py:66
[14:24:34] INFO     Splitting 'role_library.pdf' into sections                                                                                         textprocessor.py:42
           INFO     Computed embeddings in batch. Batch size: 16, Token count: 2166                                                                      embeddings.py:120
           INFO     Computed embeddings in batch. Batch size: 16, Token count: 2082                                                                      embeddings.py:120
[14:24:35] INFO     Computed embeddings in batch. Batch size: 16, Token count: 2085                                                                      embeddings.py:120
           INFO     Computed embeddings in batch. Batch size: 16, Token count: 2427                                                                      embeddings.py:120
           INFO     Computed embeddings in batch. Batch size: 12, Token count: 1706                                                                      embeddings.py:120
           INFO     Uploading batch 1 with 76 sections to search index 'gptkbindex'                                                                   searchmanager.py:639
[14:24:37] INFO     Uploading blob for document 'Benefit_Options.pdf'                                                                                   blobmanager.py:431
           INFO     Ingesting 'Benefit_Options.pdf'                                                                                                     filestrategy.py:36
           INFO     Extracting text from './data/Benefit_Options.pdf' using Azure Document Intelligence                                                    pdfparser.py:66
[14:24:43] INFO     Splitting 'Benefit_Options.pdf' into sections                                                                                      textprocessor.py:42
[14:24:44] INFO     Computed embeddings in batch. Batch size: 7, Token count: 963                                                                        embeddings.py:120
           INFO     Uploading batch 1 with 7 sections to search index 'gptkbindex'                                                                    searchmanager.py:639
[14:24:45] INFO     Uploading blob for document 'employee_handbook.pdf'                                                                                 blobmanager.py:431
           INFO     Ingesting 'employee_handbook.pdf'                                                                                                   filestrategy.py:36
           INFO     Extracting text from './data/employee_handbook.pdf' using Azure Document Intelligence                                                  pdfparser.py:66
[14:24:53] INFO     Splitting 'employee_handbook.pdf' into sections                                                                                    textprocessor.py:42
           INFO     Computed embeddings in batch. Batch size: 16, Token count: 2249                                                                      embeddings.py:120
[14:24:54] INFO     Computed embeddings in batch. Batch size: 6, Token count: 791                                                                        embeddings.py:120
           INFO     Uploading batch 1 with 22 sections to search index 'gptkbindex'                                                                   searchmanager.py:639
[14:24:55] INFO     Uploading blob for document '2192.json'                                                                                             blobmanager.py:431
           INFO     Ingesting '2192.json'                                                                                                               filestrategy.py:36
           INFO     Splitting '2192.json' into sections                                                                                                textprocessor.py:42
           INFO     Computed embeddings in batch. Batch size: 2, Token count: 375                                                                        embeddings.py:120
           INFO     Uploading batch 1 with 2 sections to search index 'gptkbindex'                                                                    searchmanager.py:639
[14:24:56] INFO     Uploading blob for document '2189.json'                                                                                             blobmanager.py:431
           INFO     Ingesting '2189.json'                                                                                                               filestrategy.py:36
           INFO     Splitting '2189.json' into sections                                                                                                textprocessor.py:42
           INFO     Computed embeddings in batch. Batch size: 1, Token count: 205                                                                        embeddings.py:120
           INFO     Uploading batch 1 with 1 sections to search index 'gptkbindex'                                                                    searchmanager.py:639
           INFO     Uploading blob for document 'query.json'                                                                                            blobmanager.py:431
[14:24:57] INFO     Ingesting 'query.json'                                                                                                              filestrategy.py:36
           INFO     Splitting 'query.json' into sections                                                                                               textprocessor.py:42
           INFO     Computed embeddings in batch. Batch size: 7, Token count: 2199                                                                       embeddings.py:120
           INFO     Uploading batch 1 with 7 sections to search index 'gptkbindex'                                                                    searchmanager.py:639
[14:24:58] INFO     Uploading blob for document '2190.json'                                                                                             blobmanager.py:431
           INFO     Ingesting '2190.json'                                                                                                               filestrategy.py:36
           INFO     Splitting '2190.json' into sections                                                                                                textprocessor.py:42
           INFO     Computed embeddings in batch. Batch size: 2, Token count: 303                                                                        embeddings.py:120
           INFO     Uploading batch 1 with 2 sections to search index 'gptkbindex'                                                                    searchmanager.py:639
[14:24:59] INFO     Uploading blob for document '2191.json'                                                                                             blobmanager.py:431
           INFO     Ingesting '2191.json'                                                                                                               filestrategy.py:36
           INFO     Splitting '2191.json' into sections                                                                                                textprocessor.py:42
           INFO     Computed embeddings in batch. Batch size: 2, Token count: 418                                                                        embeddings.py:120
           INFO     Uploading batch 1 with 2 sections to search index 'gptkbindex'                                                                    searchmanager.py:639

Deploying services (azd deploy)

  (✓) Done: Deploying service backend
  - Endpoint: https://capps-backend-mfm4mgxglrqua.politemeadow-4eda9249.eastus2.azurecontainerapps.io/ 


SUCCESS: Your up workflow to provision and deploy to Azure completed in 16 minutes 37 seconds.
(.venv) (base) arturoquiroga@MacBookPro azure-search-openai-demo % 







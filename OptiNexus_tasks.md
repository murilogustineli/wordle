# Project Proposal: Document Classification for Service Levels in Azure Blob Storage
## Introduction

The following tasks describe the process of automating the classification of SOW documents based on service levels (L2, L3, L4) using Generative AI. These documents are stored in three Azure blob storage containers (`sows-from-teams`, `sows-from-poerautomate-v2`, `pls-signed-sows`) and require categorization based on their content. The goal is to produce a comprehensive data frame showcasing the classification output for each document.

## Tasks Breakdown
1. **Connect to Azure Blob Storage**

_Objective:_ Establish a connection with Azure blob storage to facilitate the retrieval of documents.
_Tasks:_
* Utilize the Azure SDK for Python to authenticate and connect to the desired Azure Blob Storage account.
* Look into `dependency_injector` from `directory app.core.utils.dependency`
    * An example is in the file `__init__.py` under the directory `/python/optinexus_data_services/sowcompliance/tests/test_parser/__init__.py`

2. **Download Documents**

_Objective:_ Retrieve all SOW documents from the specified container.
_Tasks:_
* List all blobs (documents) in the specific container.
* Download each blob into a local/temporary storage for processing.
    * Look into the class `AzureBlobFileListRetriever` and its method `retrieve_file_names()`
    * An example is in the file `__init__.py` under the directory `/python/optinexus_data_services/sowcompliance/tests/test_parser/__init__.py`

3. **Document Parsing**

_Objective:_ Convert the downloaded documents into a readable format and chunk them for efficient processing.
_Tasks:_
* For each document:
    * Determine the document type (PDF, docx).
    * Load the document into a readable format (bytes)
        * `AzureBlobContainerConnector.load_file_as_bytes()`
    * Break the document into manageable chunks for classification.
        * Use the class `DocxParser` or `PdfParser` depending on the document format
        * Use the method `parse_doc()` that is common in each class to parse the documents into different “chunks”

4. **Document Classification**

_Objective:_ Classify each document chunk according to the predefined service levels (L2, L3, L4).
_Tasks:_
* Load the trained generative AI model for classification.
* For each document chunk:
    * Predict its class for L2, L3, and L4 using the model.
    * Aggregate the results for each document to decide the final classification.
    * TODO: [Function Name: classify_chunk, Class Name: DocumentClassifier]

5. **Output Generation**

_Objective:_ Store the classification results in a structured manner for analysis.
_Tasks:_
* Create a dataframe structure to hold: Document Name, L2 Class, L3 Class, L4 Class.
* For each document, populate the dataframe with its classifications.
* TODO: [Function Name: generate_output_df, Class Name: ClassificationOutputter]

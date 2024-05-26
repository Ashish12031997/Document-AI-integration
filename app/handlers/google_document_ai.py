import json
from typing import Optional, Sequence

from google.api_core.client_options import ClientOptions
from google.oauth2 import service_account
from google.cloud import documentai


class GoogleDocumentAI:
    """
    A class that represents the Google Document AI service.

    Args:
        project_id (str): The ID of the Google Cloud project.
        location (str): The location of the processor.
        processor_id (str): The ID of the processor.
        processor_version (str): The version of the processor.

    Attributes:
        project_id (str): The ID of the Google Cloud project.
        location (str): The location of the processor.
        processor_id (str): The ID of the processor.
        processor_version (str): The version of the processor.
    """

    def __init__(
        self, project_id: str, location: str, processor_id: str, processor_version: str
    ):
        self.project_id = project_id
        self.location = location
        self.processor_id = processor_id
        self.processor_version = processor_version
        print(f"Google Document AI initialized with project ID: {project_id}")
        with open("festive-flight-424517-p7-8ceb1d9e5f64.json", "r") as f:
            key_file_dict = json.load(f)
        self.credentials = service_account.Credentials.from_service_account_file(
            "festive-flight-424517-p7-8ceb1d9e5f64.json"
        )

    def process_document_splitter_sample(
        self,
        file_path: str,
        mime_type: str,
    ) -> None:
        """
        Processes a document using the Document AI splitter sample.

        Args:
            file_path (str): The path to the document file.
            mime_type (str): The MIME type of the document.

        Returns:
            None
        """
        # Online processing request to Document AI
        document = process_document(
            self.project_id,
            self.location,
            self.processor_id,
            self.processor_version,
            file_path,
            mime_type,
        )

        # Read the splitter output from a document splitter/classifier processor:
        # e.g. https://cloud.google.com/document-ai/docs/processors-list#processor_procurement-document-splitter
        # This processor only provides text for the document and information on how
        # to split the document on logical boundaries. To identify and extract text,
        # form elements, and entities please see other processors like the OCR, form,
        # and specialized processors.

        print(f"Found {len(document.entities)} subdocuments:")
        for entity in document.entities:
            conf_percent = f"{entity.confidence:.1%}"
            pages_range = page_refs_to_string(entity.page_anchor.page_refs)

            # Print subdocument type information, if available
            if entity.type_:
                print(
                    f"{conf_percent} confident that {pages_range} a '{entity.type_}' subdocument."
                )
            else:
                print(f"{conf_percent} confident that {pages_range} a subdocument.")

    def page_refs_to_string(
        self,
        page_refs: Sequence[documentai.Document.PageAnchor.PageRef],
    ) -> str:
        """
        Converts a page ref to a string describing the page or page range.

        Args:
            page_refs (Sequence[documentai.Document.PageAnchor.PageRef]): The page references.

        Returns:
            str: A string describing the page or page range.
        """
        pages = [str(int(page_ref.page) + 1) for page_ref in page_refs]
        if len(pages) == 1:
            return f"page {pages[0]} is"
        else:
            return f"pages {', '.join(pages)} are"

    async def process_document(
        self,
        file_path: str,
        mime_type: str,
        process_options: Optional[documentai.ProcessOptions] = None,
    ) -> documentai.Document:
        """
        Processes a document using the Document AI service.

        Args:
            file_path (str): The path to the document file.
            mime_type (str): The MIME type of the document.
            process_options (Optional[documentai.ProcessOptions]): The process options.

        Returns:
            documentai.Document: The processed document.
        """
        # api_endpoint = {"api_endpoint": f"{self.location}-documentai.googleapis.com"}
        api_endpoint = {
            "api_endpoint": "https://us-documentai.googleapis.com/v1/projects/758647369828/locations/us/processors/be296d9282ea572c:process"
        }
        print(f"API Endpoint: {api_endpoint}")
        # You must set the `api_endpoint` if you use a location other than "us".
        client = documentai.DocumentProcessorServiceClient(
            credentials=self.credentials, client_options=api_endpoint
        )

        # The full resource name of the processor version, e.g.:
        # `projects/{project_id}/locations/{location}/processors/{processor_id}/processorVersions/{processor_version_id}`
        # You must create a processor before running this sample.
        name = client.processor_path(self.project_id, self.location, self.processor_id)
        # Read the file into memory
        print("file0-------", file_path)
        with open(file_path, "rb") as image:
            image_content = image.read()

        # # Configure the process request
        print(f"Request: going to process {file_path}")
        request = documentai.ProcessRequest(
            name=name,
            raw_document=documentai.RawDocument(
                content=image_content, mime_type=mime_type
            ),
            # Only supported for Document OCR processor
            process_options=process_options,
        )
        # result = await client.process_document(request=request)

        # # For a full list of `Document` object attributes, reference this page:
        # # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
        return result.document

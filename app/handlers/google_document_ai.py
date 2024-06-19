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
        self.credentials = service_account.Credentials.from_service_account_file(
            "smart-files-424819-2f6ab750750c.json"
        )
        self.api_endpoint = {
            "api_endpoint": f"{self.location}-documentai.googleapis.com"
        }

    def page_refs_to_string(
        self,
        page_refs: Sequence[documentai.Document.PageAnchor.PageRef],
    ) -> str:
        pages = [str(int(page_ref.page) + 1) for page_ref in page_refs]
        if len(pages) == 1:
            return f"page {pages[0]} is"
        else:
            return f"pages {', '.join(pages)} are"

    def process_document(
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

        # You must set the `api_endpoint` if you use a location other than "us".
        client = documentai.DocumentProcessorServiceClient(
            credentials=self.credentials, client_options=self.api_endpoint
        )
        name = client.processor_path(self.project_id, self.location, self.processor_id)
        # Read the file into memory
        with open(file_path, "rb") as image:
            image_content = image.read()

        # # Configure the process request
        request = documentai.ProcessRequest(
            name=name,
            raw_document=documentai.RawDocument(
                content=image_content, mime_type=mime_type
            ),
            # Only supported for Document OCR processor
            process_options=process_options,
        )
        result = client.process_document(request=request)
        res_entities = []
        # print(result.document.text)
        for entity in result.document.entities:
            bounding_boxes = []
            conf_percent = f"{entity.confidence:.1%}"
            pages_range = self.page_refs_to_string(entity.page_anchor.page_refs)
            if entity.type_:
                print(
                    f"{conf_percent} confident that {pages_range} a '{entity.type_}' subdocument."
                )
            else:
                print(f"{conf_percent} confident that {pages_range} a subdocument.")
            if entity.page_anchor:
                for ref in entity.page_anchor.page_refs:
                    if ref.bounding_poly:
                        vertices = []
                        for vertex in ref.bounding_poly.normalized_vertices:
                            vertices.append({"x": vertex.x, "y": vertex.y})
                        bounding_boxes.append(vertices)
                    else:
                        print("No bounding poly detected")
                res_entities.append(
                    {
                        "type": entity.type_,
                        "mention_text": entity.mention_text,
                        "mention_id": entity.mention_id,
                        "confidence": entity.confidence,
                        "bounding_boxes": bounding_boxes,
                        # Add other fields as needed
                    }
                )
        return res_entities

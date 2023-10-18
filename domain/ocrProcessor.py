import os
from typing import Optional
from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import FailedPrecondition
from google.api_core.exceptions import NotFound
from google.cloud import documentai  # type: ignore
from ocrModel import project_id,location,processor_display_name,processor_type,processor_name,processor_id,file_path,mime_type
# PROCESSOR_GUIDE: https://cloud.google.com/document-ai/docs/create-processor#documentai_create_processor-python

# Processor types:
# INVOICE_PROCESSOR
# CUSTOM_EXTRACTION_PROCESSOR
# FORM_PARSER_PROCESSOR
# OCR_PROCESSOR
# FORM_W9_PROCESSOR
# CUSTOM_CLASSIFICATION_PROCESSOR
# UTILITY_PROCESSOR
# EXPENSE_PROCESSOR
# CUSTOM_SPLITTING_PROCESSOR
# US_DRIVER_LICENSE_PROCESSOR
# US_PASSPORT_PROCESSOR
# PURCHASE_ORDER_PROCESSOR
# ID_PROOFING_PROCESSOR
# SUMMARY_PROCESSOR


def fetch_processor_types_sample(project_id: str, location: str) -> None:
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the location
    # e.g.: projects/project_id/locations/location
    parent = client.common_location_path(project_id, location)

    # Fetch all processor types
    response = client.fetch_processor_types(parent=parent)

    print("Processor types:")
    # Print the available processor types
    for processor_type in response.processor_types:
        if processor_type.allow_creation:
            print(processor_type.type_)

def create_processor_sample(
    project_id, location, processor_display_name, processor_type
) -> None:
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the location
    # e.g.: projects/project_id/locations/location
    parent = client.common_location_path(project_id, location)

    # Create a processor
    processor = client.create_processor(
        parent=parent,
        processor=documentai.Processor(
            display_name=processor_display_name, type_=processor_type
        ),
    )

    # Print the processor information
    print(f"Processor Name: {processor.name}")
    print(f"Processor Display Name: {processor.display_name}")
    print(f"Processor Type: {processor.type_}")


def get_processor_sample(project_id: str, location: str, processor_id: str) -> None:
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor, e.g.:
    # projects/{project_id}/locations/{location}/processors/{processor_id}
    name = client.processor_path(project_id, location, processor_id)

    # Make GetProcessor request
    processor = client.get_processor(name=name)

    # Print the processor information
    print(f"Processor Name: {processor.name}")
    print(f"Processor Display Name: {processor.display_name}")
    print(f"Processor Type: {processor.type_}")


def enable_processor_sample(project_id: str, location: str, processor_id: str) -> None:
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the location
    # e.g.: projects/project_id/locations/location/processors/processor_id
    processor_name = client.processor_path(project_id, location, processor_id)
    request = documentai.EnableProcessorRequest(name=processor_name)

    # Make EnableProcessor request
    try:
        operation = client.enable_processor(request=request)

        # Print operation name
        print(operation.operation.name)
        # Wait for operation to complete
        operation.result()
    # Cannot enable a processor that is already enabled
    except FailedPrecondition as e:
        print(e.message)


def disable_processor_sample(project_id: str, location: str, processor_id: str) -> None:
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    processor_name = client.processor_path(project_id, location, processor_id)
    request = documentai.DisableProcessorRequest(name=processor_name)

    # Make DisableProcessor request
    try:
        operation = client.disable_processor(request=request)

        # Print operation name
        print(operation.operation.name)
        # Wait for operation to complete
        operation.result()
    # Cannot disable a processor that is already disabled
    except FailedPrecondition as e:
        print(e.message)


def delete_processor_sample(project_id: str, location: str, processor_id: str) -> None:
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    processor_name = client.processor_path(project_id, location, processor_id)

    # Delete a processor
    try:
        operation = client.delete_processor(name=processor_name)
        # Print operation details
        print(operation.operation.name)
        # Wait for operation to complete
        operation.result()
    except NotFound as e:
        print(e.message)


# commands:
# create_processor_sample(project_id, location, processor_display_name, processor_type)
# get_processor_sample(project_id, location, processor_id)
# enable_processor_sample(project_id, location, processor_id)
# disable_processor_sample(project_id, location, processor_id)
# delete_processor_sample(project_id, location, processor_id)


def process_document_sample(
    project_id: str,
    location: str,
    processor_id: str,
    file_path: str,
    mime_type: str,
    field_mask: Optional[str] = None,
    processor_version_id: Optional[str] = None,
) -> str:
    
    try:
        # create_processor_sample(project_id, location, processor_display_name, processor_type)
        # enable_processor_sample(project_id, location, processor_id)
        # You must set the `api_endpoint` if you use a location other than "us".
        opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

        client = documentai.DocumentProcessorServiceClient(client_options=opts)

        if processor_version_id:
            # The full resource name of the processor version, e.g.:
            # `projects/{project_id}/locations/{location}/processors/{processor_id}/processorVersions/{processor_version_id}`
            name = client.processor_version_path(
                project_id, location, processor_id, processor_version_id
            )
        else:
            # The full resource name of the processor, e.g.:
            # `projects/{project_id}/locations/{location}/processors/{processor_id}`
            name = client.processor_path(project_id, location, processor_id)

        # Read the file into memory
        with open(file_path, "rb") as image:
            image_content = image.read()

        # Load binary data
        raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)
        print("======1=======")

        # For more information: https://cloud.google.com/document-ai/docs/reference/rest/v1/ProcessOptions
        # Optional: Additional configurations for processing.
        # process_options = documentai.ProcessOptions(
        #     # Process only specific pages
        #     individual_page_selector=documentai.ProcessOptions.IndividualPageSelector(
        #         pages=[1]
        #     )
        # )

        # Configure the process request
        request = documentai.ProcessRequest(
            name=name,
            raw_document=raw_document,
            field_mask=field_mask,
            # process_options=process_options,
        )
        print("======2=======", request.name)
        result = client.process_document(request=request)
        print("======3=======")
        # For a full list of `Document` object attributes, reference this page:
        # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
        document = result.document
        print("======4=======")
        # Read the text recognition output from the processor
        print("The document contains the following text:")
        print(document.text)

        text_Summary = document.text.replace('\n', ' ') + '\n'

        # Create a directory to store the text file if it doesn't exist
        os.makedirs('detected_texts', exist_ok=True)
        print("============")
        # Save all the detected text to a single txt file
        file_path = os.path.join('detected_texts', 'all_detected_texts.txt')
        with open(file_path, 'w', encoding='utf-8') as file:
            # Join all the texts with a space separator and write to the file
            file.write(" ".join(text_Summary))

        return text_Summary

    except Exception as e:
        print(f"Error during document processing: {e}")
        raise e  # To ensure the error is propagated

    
import os
# TODO(developer): Uncomment these variables before running the sample.

project_id = 'spry-pipe-399707'
location = 'us' # Format is 'us' or 'eu'
processor_display_name = 'INSIGHT' # Must be unique per project, e.g.: 'My Processor'
processor_type = 'OCR_PROCESSOR' # Use fetch_processor_types to get available processor types
# The full resource name of the processor, e.g.:
# projects/{project_id}/locations/{location}/processors/{processor_id}
processor_name = 'projects/1037194573053/locations/us/processors/6bcc7d42fa3786'
processor_id = '6bcc7d42fa3786'
file_path = os.path.join('detected_texts', 'combined.pdf')
mime_type = "application/pdf" # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types
# field_mask = "text,entities,pages.pageNumber"  # Optional. The fields to return in the Document object.
# processor_version_id = "YOUR_PROCESSOR_VERSION_ID" # Optional. Processor version to use
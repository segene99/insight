from typing import List
import requests
from google.cloud import vision as gvision
from model import ImageURL

def pic_to_text(url: List[ImageURL]) -> str:
    """Detects text in an image from a URL

    Args:
    url: URL to the image file

    Returns:
    String of text detected in image
    """

    # Download the image from the URL
    response = requests.get(url)
    image_content = response.content

    # Instantiates a client
    client = gvision.ImageAnnotatorClient()

    # Create an Image object with the content
    image = gvision.Image(content=image_content)

    # For dense text, use document_text_detection
    response = client.document_text_detection(image=image) # pylint: disable=no-member
    text = response.full_text_annotation.text

    print(f"Detected text: {text}")
            
    return text
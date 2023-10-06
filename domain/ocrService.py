import os
import requests
from google.cloud import vision as gvision
from typing import List
from model import ImageList, ImageURL

def pic_to_text(image_list: ImageList) -> List[str]:
    """Detects text in images from URLs

    Args:
    image_list: List of URLs to the image files

    Returns:
    List of strings of text detected in images
    """
    
    # Instantiates a client
    client = gvision.ImageAnnotatorClient()
    texts = []

    # Create a directory to store the text files if it doesn't exist
    os.makedirs('detected_texts', exist_ok=True)

    for idx, image_url_obj in enumerate(image_list.imageUrls):
        # Extract the URL string
        url = image_url_obj.url
        
        # Download the image from the URL
        response = requests.get(url)
        image_content = response.content

        # Create an Image object with the content
        image = gvision.Image(content=image_content)

        # For dense text, use document_text_detection
        response = client.document_text_detection(image=image) # pylint: disable=no-member
        text = response.full_text_annotation.text

        # Save the detected text to a txt file
        file_path = os.path.join('detected_texts', f'detected_text_{idx}.txt')
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)

        texts.append(text)

    return texts



'''
from typing import List
import requests
from google.cloud import vision as gvision
from model import ImageList, ImageURL

def pic_to_text(image_list: ImageList) -> List[str]:
    """Detects text in images from URLs

    Args:
    image_list: List of URLs to the image files

    Returns:
    List of strings of text detected in images
    """
    
    # Instantiates a client
    client = gvision.ImageAnnotatorClient()
    texts = []

    for image_url_obj in image_list.imageUrls:
        # Extract the URL string
        url = image_url_obj.url
        
        # Download the image from the URL
        response = requests.get(url)
        image_content = response.content

        # Create an Image object with the content
        image = gvision.Image(content=image_content)

        # For dense text, use document_text_detection
        response = client.document_text_detection(image=image) # pylint: disable=no-member
        text = response.full_text_annotation.text

        # print(f"Detected text for {url}: {text}")
        texts.append(text)

    return texts
'''
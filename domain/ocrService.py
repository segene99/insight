import os
import requests
from google.cloud import vision as gvision
from typing import List
from crud import insert_ocr
from database import SessionLocal
from models import ImageList, ImageURL
from models import Question

def pic_to_text(image_list: ImageList) -> List[str]:

    # Instantiates a client
    client = gvision.ImageAnnotatorClient()
    texts = []    
    # Remove duplicate ImageURL objects based on their URL
    unique_image_urls = list({img.url: img for img in image_list.imageUrls}.values())
    # Filter out .gif URLs from the unique set
    filtered_image_urls = [image_url_obj for image_url_obj in unique_image_urls if not image_url_obj.url.endswith('.gif')]
    # Filter out .gif URLs from the unique set and change "jpg" to "jpeg"
    print("Number of filtered image URLs:", len(filtered_image_urls))
    texts.append(image_list.productTexts)
    for image_url_obj in filtered_image_urls:
        # Download the image from the URL
        # Extract the URL string
        url = image_url_obj.url

        # Modify the URL if it starts with "https://"
        if url.startswith("https://"):
            url = url.replace("https://", "http://")
            image_url_obj.url = url

        res = requests.get(url)
        image_content = res.content
        # Create an Image object with the content
        image = gvision.Image(content=image_content)
        # For dense text, use document_text_detection
        response = client.document_text_detection(image=image) # pylint: disable=no-member
        # print("========ocr response======",response)
        document = response.full_text_annotation
        detected_text = response.full_text_annotation.text 
        get_document_bounds(document,detected_text)
        #print("========detected_text======",detected_text)
        # Remove existing newline characters and add a newline at the end
        text = detected_text.replace('\n', ' ') + '\n'
        texts.append(text)
        
    #print(texts)
    #OCR data insertion into DB
    insert_ocr(texts, image_list)
    #print(texts)
    # print("=====6=======")
    # # Create a directory to store the text file if it doesn't exist
    # os.makedirs('detected_texts', exist_ok=True)
    # print("=====7=======")
    # # Save all the detected text to a single txt file
    # file_path = os.path.join('detected_texts', 'all_detected_texts.txt')
    # with open(file_path, 'w', encoding='utf-8') as file:
    #     # Join all the texts with a space separator and write to the file
    #     file.write(" ".join(texts))
    
    return texts

from enum import Enum
class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5
    
def get_document_bounds(document, detected_text):
    bounds = []

    # Collect specified feature bounds by enumerating all document features
    for page in document.pages:
        for block in page.blocks:
            bounds.append(block.bounding_box)

    # The list `bounds` contains the coordinates of the bounding boxes.
    print("bounds : ", bounds)
    return bounds
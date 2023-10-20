import os
import requests
from google.cloud import vision as gvision
from typing import List
from crud import insert_ocr
from database import SessionLocal
from models import ImageList, ImageURL
from models import Question



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
    print("=======1======")
    # Remove duplicate ImageURL objects based on their URL
    unique_image_urls = list({img.url: img for img in image_list.imageUrls}.values())
    print("=======2======")
    # Filter out .gif URLs from the unique set
    filtered_image_urls = [image_url_obj for image_url_obj in unique_image_urls if not image_url_obj.url.endswith('.gif')]
    print("=======3======")
    # print("Number of filtered image URLs:", len(filtered_image_urls))

    for image_url_obj in filtered_image_urls:
        # Download the image from the URL
        # Extract the URL string
        url = image_url_obj.url
        res = requests.get(url)
        image_content = res.content
        # Create an Image object with the content
        image = gvision.Image(content=image_content)
        # For dense text, use document_text_detection
        response = client.document_text_detection(image=image) # pylint: disable=no-member
        # print("========ocr response======",response)
        detected_text = response.full_text_annotation.text
        # Remove existing newline characters and add a newline at the end
        text = detected_text.replace('\n', ' ') + '\n'
        texts.append(text)

    #OCR data insertion into DB
    insert_ocr(texts, image_list)

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

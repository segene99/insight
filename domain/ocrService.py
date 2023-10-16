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
    print("=====1=======")
    for image_url_obj in image_list.imageUrls:
        # Extract the URL string
        url = image_url_obj.url
        print("=====2=======")
        # Download the image from the URL
        res = requests.get(url)
        image_content = res.content
        print("=====3=======")
        # Create an Image object with the content
        image = gvision.Image(content=image_content)
        print("=====4=======")
        # For dense text, use document_text_detection
        response = client.document_text_detection(image=image) # pylint: disable=no-member
        detected_text = response.full_text_annotation.text
        # Remove existing newline characters and add a newline at the end
        text = detected_text.replace('\n', ' ') + '\n'
        print("=====5=======", text)
        texts.append(text)


    print("=====6=======")
    # Create a directory to store the text file if it doesn't exist
    os.makedirs('detected_texts', exist_ok=True)
    print("=====7=======")
    # Save all the detected text to a single txt file
    file_path = os.path.join('detected_texts', 'all_detected_texts.txt')
    with open(file_path, 'w', encoding='utf-8') as file:
        # Join all the texts with a space separator and write to the file
        file.write(" ".join(texts))

    return texts
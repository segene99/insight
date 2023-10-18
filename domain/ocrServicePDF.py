import requests
from PIL import Image
from io import BytesIO
from typing import List, Optional
from domain.ocrProcessor import process_document_sample
from model import ImageList, ImageURL
import os
from google.cloud import vision
from ocrModel import project_id,location,processor_id,file_path,mime_type

def img_to_pdf(image_list: ImageList, output_filename='combined.pdf', output_folder='detected_texts'):
    """
    Converts a list of images (specified by URLs) into a single PDF file
    and saves it in the specified output folder.

    Args:
    image_list: List of image URLs.
    output_filename: Filename to save the combined PDF file.
    output_folder: Folder to save the combined PDF file.

    Returns:
    Path of the created PDF file or None if the process fails.
    """
    images = []

    # Remove duplicate ImageURL objects based on their URL
    unique_image_urls = list({img.url: img for img in image_list.imageUrls}.values())

    # Filter out .gif URLs from the unique set
    filtered_image_urls = [image_url_obj for image_url_obj in unique_image_urls if not image_url_obj.url.endswith('.gif')]


    print(filtered_image_urls)
    # Download and open the images
    # for image_url_obj in image_list.imageUrls:
    for image_url_obj in filtered_image_urls:
        try:
            # Download the image
            response = requests.get(image_url_obj.url)
            response.raise_for_status()  # Check if the request was successful
            
            # Open the image and append to the list
            img = Image.open(BytesIO(response.content))
            images.append(img)
        except requests.RequestException as e:
            print(f"Failed to download image from {image_url_obj.url}: {str(e)}")
            return None
        except Exception as e:
            print(f"Failed to process image from {image_url_obj.url}: {str(e)}")
            return None
    
    # Check if any images were successfully downloaded
    if not images:
        print("No images were downloaded successfully.")
        return None

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Define the full path to save the PDF
    output_path = os.path.join(output_folder, output_filename)

    try:
        # Convert and save the images as a PDF file
        images[0].save(output_path, save_all=True, append_images=images[1:])
    except Exception as e:
        print(f"Failed to save images as PDF: {str(e)}")
        return None
    
    return output_path


def images_to_text(image_list: ImageList, pdf_filename='combined.pdf', output_folder='detected_texts') -> str:
    """
    Converts a list of image URLs to a PDF and then extracts text from the PDF.

    Args:
    image_list: List of image URLs.
    pdf_filename: Filename to save the combined PDF file.
    text_filename: Filename to save the extracted text file.
    output_folder: Folder to save the PDF and text file.

    Returns:
    List of strings of text detected in the PDF file or an empty list if the process fails.
    """
    # Step 1: Convert images to PDF
    pdf_path = img_to_pdf(image_list, output_filename=pdf_filename, output_folder=output_folder)
    
    if pdf_path is None:
        print("Image to PDF conversion failed.")
    
    extracted_Texts = process_document_sample(project_id,location,processor_id,file_path,mime_type)

    return extracted_Texts
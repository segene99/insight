import argparse
from enum import Enum

from google.cloud import vision
from PIL import Image, ImageDraw

class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5

def draw_boxes(image, bounds, color):
    # image: 이미지 객체. 이 함수는 이 이미지 위에 경계 상자를 그립니다.
    # bounds: 경계 상자의 좌표 정보를 담고 있는 리스트입니다. 경계 상자는 주어진 좌표로 정의되며, 각 상자는 네 개의 꼭지점(버텍스)을 가지며, 이러한 정보가 bound.vertices에 포함되어 있습니다.
    # color: 경계 상자의 색상을 지정합니다. 이 색상은 경계 상자의 외곽선 색상을 나타냅니다.
    """Draws a border around the image using the hints in the vector list.

    Args:
        image: the input image object.
        bounds: list of coordinates for the boxes.
        color: the color of the box.

    Returns:
        An image with colored bounds added.
    """
    draw = ImageDraw.Draw(image)

    for bound in bounds:
        draw.polygon(
            [
                bound.vertices[0].x,
                bound.vertices[0].y,
                bound.vertices[1].x,
                bound.vertices[1].y,
                bound.vertices[2].x,
                bound.vertices[2].y,
                bound.vertices[3].x,
                bound.vertices[3].y,
            ],
            None,
            color,
        )
    return image

def get_document_bounds(image_file, feature):
    """Finds the document bounds given an image and feature type.

    Args:
        image_file: path to the image file.
        feature: feature type to detect.

    Returns:
        List of coordinates for the corresponding feature type.
    """
    client = vision.ImageAnnotatorClient()

    bounds = []

    with open(image_file, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    # Collect specified feature bounds by enumerating all document features
    for page in document.pages:
        for block in page.blocks:
            if feature == FeatureType.BLOCK:
                bounds.append(block.bounding_box)

    # The list `bounds` contains the coordinates of the bounding boxes.
    return bounds

def render_doc_text(filein, fileout):
    """Outlines document features (blocks, paragraphs and words) given an image.

    Args:
        filein: path to the input image.
        fileout: path to the output image.
    """
    image = Image.open(filein)
    bounds = get_document_bounds(filein, FeatureType.BLOCK)
    draw_boxes(image, bounds, "blue")

    if fileout != 0:
        image.save(fileout)
    else:
        image.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("detect_file", help="The image for text detection.")
    parser.add_argument("-out_file", help="Optional output file", default=0)
    args = parser.parse_args()

    render_doc_text(args.detect_file, args.out_file)
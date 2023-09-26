from __future__ import print_function
import json
import requests as r
from base64 import b64encode

# keys.txt 파일에서 API 키들을 읽어오는 함수
def read_keys_from_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        google_key = lines[1].strip().split('=')[1].replace('"', '')
    return google_key

# keys.txt 파일에서 API 키들을 가져옴
google_key_value = read_keys_from_file('keys.txt')

# API키 fetch
def read_google_api_key():
    key = google_key_value
    if key is None:
        raise Exception('The env variable GOOGLE_API_KEY is not defined. Export GOOGLE_API_KEY=<key>.')
    return key

# Google Cloud Natural Language API를 사용하여 텍스트를 분석
def get_annotate_text(text, key, sentiment_analysis=False):
    url = 'https://language.googleapis.com/v1beta1/documents:annotateText?key={}'.format(key)
    data = dict()
    data['document'] = {
        'type': 'PLAIN_TEXT',
        'content': text,
    }
    data['encoding_type'] = 'UTF8'
    features = dict()
    features['extractEntities'] = True
    if sentiment_analysis:
        features['extractDocumentSentiment'] = True
    data['features'] = features
    print(data)
    return r.post(url, json=data).json()

# Google Vision API에 이미지 데이터를 제공하기 위한 형식으로 변환하는 함수
def make_image_data_list(images, b64=True):
    """
    image_filenames는 파일 이름 문자열의 목록
    Vision API가 필요로 하는 형식으로 포맷된 딕셔너리 목록을 반환
    """

    def content(context):
        return {
            'image': {'content': context},
            'features': [
                {
                    'type': 'TEXT_DETECTION',
                    'maxResults': 10
                }
                # {
                #     'type': 'LABEL_DETECTION',
                #     'maxResults': 10
                # },
                # {
                #     'type': 'TEXT_DETECTION',
                #     'maxResults': 10
                # },
                # {
                #     'type': 'LOGO_DETECTION',
                #     'maxResults': 10
                # },
                # {
                #     'type': 'FACE_DETECTION',
                #     'maxResults': 10
                # },
                # {
                #     'type': 'LANDMARK_DETECTION',
                #     'maxResults': 10
                # },
                # {
                #     'type': 'SAFE_SEARCH_DETECTION',
                #     'maxResults': 10
                # }
            ]
        }

    img_requests = []
    if not b64:
        for img in images:
            with open(img, 'rb') as f:
                ctxt = b64encode(f.read()).decode()
                img_requests.append(content(ctxt))
    else:
        for img in images:
            img_requests.append(content(img))
    return img_requests

# Google Vision API에 이미지 데이터를 제공하기 위한 형식으로 변환하는 함수
def make_image_data(images, b64=True):
    img_dict = make_image_data_list(images, b64)
    return json.dumps({"requests": img_dict}).encode()

# Google Vision API를 호출하여 이미지 분석 결과
def request_vision_api(image, b64=True):
    api_key = read_google_api_key()

    # 해당 주소로 요청 및 응답
    response = r.post('https://vision.googleapis.com/v1/images:annotate',
                      data=make_image_data([image], b64),
                      params={'key': api_key},
                      headers={'Content-Type': 'application/json'})
    return response

# 커맨드 라인 사용 시, 이미지 파일을 인자로 받아 Google Vision API를 호출하고 결과를 출력
if __name__ == '__main__':
    import sys

    arguments = sys.argv

    if len(arguments) < 2:
        print('Please specify an image as argument.')
        exit(1)

    resp = request_vision_api(arguments[1], b64=False)
    dict_google_response = json.loads(resp.content)
    str_to_write = json.dumps(dict_google_response, indent=4)
    print(str_to_write)

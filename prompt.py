import openai
import re  # 정규 표현식 모듈 추가

# keys.txt 파일에서 API 키들을 읽어오는 함수
def read_keys_from_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        openai_key = lines[0].strip().split('=')[1].replace('"', '')
    return openai_key

# keys.txt path
keys_txt_path = 'key/keys.txt'

# keys.txt 파일에서 API 키들을 가져옴
openai_key_value = read_keys_from_file(keys_txt_path)

# 가져온 키를 변수에 대입
openai.api_key = openai_key_value
# 모델과 관련된 상수 설정
MAX_TOKENS = 16000  # gpt-3.5-turbo 모델의 최대 토큰 수
OVERLAP_TOKENS = 50  # 문장이 훼손되지 않게 하기 위한 오버랩 토큰 수

# 단락별로 제목을 추출하는 함수
def extract_paragraph_titles(ocr_text):
    # 텍스트를 줄 단위로 분할
    lines = ocr_text.split('\n')
    
    paragraph_titles = []
    current_title = None

    for line in lines:
        # 정규 표현식을 사용하여 제목 패턴을 찾음
        # 이 예제에서는 제목이 대문자로 시작하고 콜론(:)이 있는 줄로 가정합니다.
        if re.match(r'^[A-Z].*:$', line):
            # 이전 제목을 저장하고 새로운 제목을 시작
            if current_title:
                paragraph_titles.append(current_title.strip())
            current_title = line
        else:
            # 현재 제목 아래에 있는 텍스트 추가
            if current_title:
                current_title += ' ' + line

    # 마지막으로 발견된 제목 추가
    if current_title:
        paragraph_titles.append(current_title.strip())

    return paragraph_titles

def split_text(text, max_length, overlap):
    sentences = text.split('.')
    chunks = []

    current_chunk = []
    current_length = 0
    for sentence in sentences:
        current_sentence_length = len(sentence)
        if current_length + current_sentence_length + overlap >= max_length:
            chunks.append('. '.join(current_chunk))
            current_chunk = []
            current_length = 0
        current_chunk.append(sentence.strip())
        current_length += current_sentence_length

    if current_chunk:
        chunks.append('. '.join(current_chunk))

    return chunks

def is_valid_response(question, ocr_text, response):
    # 질문의 키워드를 분리
    question_keywords = set(question.split())

    # OCR 텍스트와 응답에 있는 키워드를 분리
    ocr_keywords = set(ocr_text.split())
    response_keywords = set(response.split())

    # 질문의 키워드 중 OCR 텍스트에 없는 것이 응답에 포함되어 있는지 확인
    for keyword in question_keywords:
        if keyword not in ocr_keywords and keyword in response_keywords:
            return False

    return True

def ask_gpt(question, ocr_text):
    # OCR에서 받은 텍스트에서 단락별 제목 추출
    ocr_paragraph_titles = extract_paragraph_titles(ocr_text)

    # 사용자에게 제목 목록을 전달
    print("단락 제목 목록:")
    for i, title in enumerate(ocr_paragraph_titles, start=1):
        print(f"{i}. {title}")

    text_chunks = split_text(ocr_text, MAX_TOKENS - 300, OVERLAP_TOKENS)
    responses = []

    for chunk in text_chunks:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            temperature=0.0,
            messages=[
                {"role": "system", "content": f"당신은 친절한 쇼핑 도우미입니다. 주어진 OCR 텍스트 안의 정보만을 기반으로 질문에 답하십시오.\n\n{chunk}"},
                {"role": "user", "content": question}
            ]
        )
        
        response_text = response.choices[0].message['content'].strip()
        
        # Validate the response using the is_valid_response function
        if not is_valid_response(question, chunk, response_text):
            response_text = "원하는 정보를 찾을 수 없습니다."
        
        responses.append(response_text)
        break  # 첫 번째 청크에 대한 응답만 사용하도록 break 추가

    return responses[0]

# 사용자로부터 질문 받기
user_input = input("무엇을 도와드릴까요? ")
# OCR에서 받은 텍스트라 가정
ocr_data = """ 

 텍스트 샘플 이다아아아아아

"""

answer = ask_gpt(user_input, ocr_data)
print(answer)

import openai
import re

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
MAX_TOKENS = 16000
OVERLAP_TOKENS = 50

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
    question_keywords = set(question.split())
    ocr_keywords = set(ocr_text.split())
    response_keywords = set(response.split())

    for keyword in question_keywords:
        if keyword not in ocr_keywords and keyword in response_keywords:
            return False

    return True

def ask_gpt(question, ocr_text):
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
        
        if not is_valid_response(question, chunk, response_text):
            response_text = "원하는 정보를 찾을 수 없습니다."
        
        responses.append(response_text)
        break

    return responses[0]

def extract_titles_from_ocr(ocr_text):
    lines = ocr_text.split('\n')
    titles = []

    for line in lines:
        # 각 줄의 문자수와 대문자의 비율을 계산
        total_chars = len(line)
        uppercase_chars = sum(1 for c in line if c.isupper())
        
        # 짧은 줄이면서 대부분의 문자가 대문자인 경우 제목으로 간주
        if 5 < total_chars < 50 and (uppercase_chars / total_chars) > 0.3:
            titles.append(line.strip())
    
    return titles



# ocr에서 받은 텍스트라 가정
ocr_data = """ 

샘플 텍스트입니다아아아아아아ㅏ아아아아아아아아아아아ㅏ아아아아아


"""

titles = extract_titles_from_ocr(ocr_data)
if titles:
    print("OCR 텍스트에서 발견된 제목들입니다:")
    for idx, title in enumerate(titles, 1):
        print(f"{idx}. {title.strip()}")
else:
    print("OCR 텍스트에서 제목을 발견할 수 없습니다.")

user_input = input("무엇을 도와드릴까요? ")
answer = ask_gpt(user_input, ocr_data)
print(answer)

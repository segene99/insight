import openai

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

def split_text(text, max_length, overlap):
    tokens = text.split()
    chunks = []

    current_chunk = []
    current_length = 0
    for token in tokens:
        current_chunk.append(token)
        current_length += len(token)
        if current_length + overlap >= max_length:
            chunks.append(' '.join(current_chunk))
            current_chunk = current_chunk[-overlap:]
            current_length = sum(len(t) for t in current_chunk)
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

def ask_gpt(question, ocr_text):
    text_chunks = split_text(ocr_text, MAX_TOKENS - 300, OVERLAP_TOKENS)
    responses = []

    for chunk in text_chunks:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            temperature=0.1,  # 온도값 설정
            messages=[
                {"role": "system", "content": f"당신은 친절한 쇼핑 도우미입니다. 주어진 OCR 텍스트 안의 정보만을 기반으로 질문에 답하십시오.\n\n{chunk}"},
                {"role": "user", "content": question}
            ]
        )
        
        response_text = response.choices[0].message['content'].strip()
        responses.append(response_text)

    combined_response = ' '.join(responses)

    # 사용자의 질문에 있는 키워드가 OCR 텍스트에 없고, GPT의 응답에 그 키워드가 포함되어 있는지 확인
    question_keywords = question.split()
    for keyword in question_keywords:
        if keyword not in ocr_text and keyword in combined_response:
            return "원하는 정보를 찾을 수 없습니다."

    return combined_response
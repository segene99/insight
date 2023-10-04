import openai

def read_keys_from_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        openai_key = lines[0].strip().split('=')[1].replace('"', '')
    return openai_key

import openai

# OpenAI API 키 설정
openai.api_key = 'YOUR_OPENAI_API_KEY'

MAX_TOKENS = 4096  # GPT-3.5 Turbo의 최대 토큰 수
OVERLAP = 150  # 문맥을 유지하기 위한 overlap 토큰 수

def split_text_with_overlap(text, max_length, overlap):
    tokens = text.split()
    chunks = []
    current_chunk = []

    for token in tokens:
        if len(' '.join(current_chunk) + ' ' + token) > max_length - overlap:
            chunks.append(' '.join(current_chunk))
            current_chunk = current_chunk[-overlap:]
        current_chunk.append(token)

    chunks.append(' '.join(current_chunk))
    return chunks

def get_gpt_response(ocr_text):
    # 페르소나 설정
    persona = "나는 친절하게 쇼핑 정보를 안내해주는 인공지능입니다."
    
    # 사용자에게 질문을 받기
    question = input("무엇을 알려드릴까요? ")
    
    prompt = persona + "\n" + ocr_text + "\n질문: " + question + "\n답변: "

    # 텍스트 분할
    chunks = split_text_with_overlap(prompt, MAX_TOKENS - OVERLAP, OVERLAP)
    responses = []

    for chunk in chunks:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=chunk,
            max_tokens=MAX_TOKENS,
            n=1,
            stop=None,
            temperature=0.7
        )
        responses.append(response.choices[0].text.strip())

    return ' '.join(responses)

# 예시
ocr_text = "..."  # 여기에 OCR로 얻은 텍스트를 넣어주세요
answer = get_gpt_response(ocr_text)
print(answer)

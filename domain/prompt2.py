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

def flatten_tuple(t):
    for item in t:
        if isinstance(item, tuple):
            yield from flatten_tuple(item)
        else:
            yield item

def split_text(text, max_length, overlap):
    sentences = text.split('.')
    chunks = []

    current_chunk = []
    current_length = 0
    for sentence in sentences:
        current_sentence_length = len(sentence)
        if current_length + current_sentence_length + overlap >= max_length:
            chunks.append('. '.join(current_chunk) + '.')
            current_chunk = current_chunk[-overlap:]
            current_length = sum(len(s) for s in current_chunk)
        current_chunk.append(sentence.strip())
        current_length += current_sentence_length

    if current_chunk:
        chunks.append('. '.join(current_chunk) + '.')

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
    ocr_text = ' '.join(flatten_tuple(ocr_text))
    text_chunks = split_text(ocr_text, MAX_TOKENS - 300, OVERLAP_TOKENS)
    responses = []

    for chunk in text_chunks:
        system_message = (
    "The text you received is an item detail information from online shopping mall\n"
    "Your task is to answer the question only based the text provided\n"
    "Be sure to answer the questions in Korean and honorifics based only on the information in the given text. "
    "Do not refer to any other external information or knowledge. Please answer all questions in English in Korean."
    "Please respond as politely and kindly as possible to the user"
    "when you answer the question, first find relevant information in the text provided, then answer the question based on the relevant information."
    "전달받은 내용과 사용자의 질문에 대해 관련성이 높은 동의어나 대체어를 판별하고 올바른 답변을 해주세요."
    "여러 제품이 있을 경우 공통된 질문을 한다면 모든 제품의 정보를 모두 답변해주세요"
    "질문내용에서 '이게'는 '이거'의 의미로 사용됩니다. '이게'를 '이거'로 해석하고 답변해주세요(단 '이 게'일때는 적용하지 마시오)."
    "중복되는 정보가 있으면 모두 답변해주세요 .\n\n" + chunk
)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            temperature=0.1,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": question}
            ]
        )
        
        response_text = response.choices[0].message['content'].strip()
        responses.append(response_text)
        break

    return responses[0]
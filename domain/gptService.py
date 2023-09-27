import openai
# 키받는곳: https://platform.openai.com/account/
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

def get_summary_from_gpt(response_dict):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "assistant",
                "content": "받은 내용을 정리해줘. 내용을 빼먹으면 안돼"
            },
            {
                "role": "system",
                "content": str(response_dict)
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message['content']
import os
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
        model="gpt-3.5-turbo-16k",
        messages=[
            {
                "role": "assistant",
                "content": "상품 정보 제공 고시 내용은 빼지말고 요약해줘. 빨리 대답해줘"
            },
            {
                "role": "system",
                "content": str(response_dict)
            }
        ],
        temperature=0.3,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

     # Create a directory to store the text file if it doesn't exist
    os.makedirs('detected_texts', exist_ok=True)

    # Save all the detected text to a single txt file
    file_path = os.path.join('detected_texts', 'summary.txt')
    with open(file_path, 'w', encoding='utf-8') as file:
        # Join all the texts with a space separator and write to the file
        file.write(" ".join(response.choices[0].message['content']))

    return response.choices[0].message['content']


def choose_search_type(question: str):
    system_message = '''
                        To answer the following question correctly, 
                        tell me whether keyword search is appropriate or semantic search is appropriate. 
                        Your answer must be either 'keyword' or 'semantic'.                      
    '''
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": question}
        ],
        temperature=0.0,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message['content']
from typing import List
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi import APIRouter

import openai
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from model import ImageURL, Turn, Messages

router = APIRouter()
# router.mount("/static", StaticFiles(directory="static"), name="static")

# keys.txt 파일에서 API 키들을 읽어오는 함수
def read_keys_from_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        api_key_speech = lines[2].strip().split('=')[1].replace('"', '')
    return api_key_speech

# keys.txt path
keys_txt_path = 'key/keys.txt'

# keys.txt 파일에서 API 키들을 가져옴
openai_key_value = read_keys_from_file(keys_txt_path)

# 가져온 키를 변수에 대입
openai.api_key = openai_key_value


def chat(information,messages):
    # OpenAI의 GPT-3.5-turbo 모델을 사용하여 채팅 완성을 요청하고 응답을 받습니다.
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[
            {
                "role": "assistant",
                "content": "전달받은 텍스트 안에서만 질문에 대한 대답을 해줘"
            },
                        {
                "role": "system",
                "content": str(messages)
            }
            ],
            temperature=1,
            top_p=1
            )
    # OpenAI 응답을 딕셔너리 형태로 변환합니다.
    resp_dict = response.to_dict_recursive()
    # 어시스턴트의 응답을 추출합니다.
    assistant_turn = resp_dict['choices'][0]['message']
    # 어시스턴트의 응답을 반환합니다. {"role": "assistant", "content": "blahblahblah"} 형식으로 반환됩니다.
    return assistant_turn 

@router.post("/chat", response_model=Turn)
async def post_chat(messages: Messages):
    # messages 변수를 딕셔너리로 변환하여 업데이트
    messages = messages.model_dump()

    # chat 함수를 호출하여 어시스턴트의 응답을 가져옴
    assistant_turn = chat(messages=messages['messages'])

    # 어시스턴트의 응답 반환
    return assistant_turn

@router.post("/transcribe")
async def transcribe_audio(audio_file: UploadFile = File(...)):
    try:
        # 임시 파일 이름 설정
        file_name = "tmp_audio_file.wav"
        #받은 오디오 파일을 바이너리 모드로 열고 임시 파일에 저장
        with open(file_name, "wb") as f:
            f.write(audio_file.file.read())
        #임시 파일을 바이너리 모드로 열고 OpenAI의 음성인식 API를 사용하여 텍스트로 변환
        with open(file_name, "rb") as f:
            transcription = openai.Audio.transcribe("whisper-1", f)
        # 음성 인식 결과에서 텍스트 추출
        text = transcription['text']
    except Exception as e:
        print(e)
        text = f"음성인식에서 실패했습니다. {e}"
     # 변환된 텍스트 반환
    return {"text": text}
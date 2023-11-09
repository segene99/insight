
import os
from pathlib import Path
from typing import List
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi import APIRouter

import openai
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from models import ImageURL, Turn, Messages
from domain.prompt import ask_gpt

router = APIRouter()

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


@router.post("/transcribe")
async def transcribe_audio(audio_file: UploadFile = File(...)):
    try:
        # Ensure 'tts_audio' folder exists
        Path("tts_audio").mkdir(parents=True, exist_ok=True)
        file_path = "tts_audio/tmp_audio_file.wav"
        # 임시 파일 이름 설정
        file_name = "tmp_audio_file.wav"
        #받은 오디오 파일을 바이너리 모드로 열고 임시 파일에 저장
        with open(file_path, "wb") as f:
            f.write(audio_file.file.read())
        #임시 파일을 바이너리 모드로 열고 OpenAI의 음성인식 API를 사용하여 텍스트로 변환
        with open(file_path, "rb") as f:
            transcription = openai.Audio.transcribe("whisper-1", f)
        # 음성 인식 결과에서 텍스트 추출
        text = transcription['text']
    except Exception as e:
        print(e)
        text = f"음성인식에서 실패했습니다. {e}"
     # 변환된 텍스트 반환
    return {"text": text}

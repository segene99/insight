import json
import base64
import statistics
from typing import List
from fastapi import Depends, FastAPI, HTTPException, Request, UploadFile, File
from domain.gptService import choose_search_type, get_summary_from_gpt
from domain.hybridSearchService import combined_search
from domain.keywordSearchService import search_keyword
from domain.prompt2 import ask_gpt
from domain.ragService3 import search_documents
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from io import BytesIO
from domain.ocrService import pic_to_text
from models import * 
from speech_server import router as speech_router  # 모듈과 변수명을 올바르게 가져옴
import logging
from google.cloud import texttospeech
from fastapi.responses import JSONResponse
from domain.ttsService import get_audio_from_tts, delete_audio_files
from pydantic import BaseModel
from typing import Annotated
from database import engine, SessionLocal
from crud import check_ocr
from sqlalchemy.orm import Session
import models
import time

# fastapi로 객체 생성
app = FastAPI()
app.include_router(speech_router)

# Assuming the template is in a "templates" directory
templates = Jinja2Templates(directory="templates")  

# middleware 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You might want to be more specific than "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB
models.Base.metadata.create_all(bind=engine)

class searchResults(BaseModel):
    id: int
    subject: str
    content: str
    create_date: str

# main.html 호출
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

@app.post("/pic_to_text")
async def get_text_from_image(image_data: ImageList):
    try:
        start_time = time.time()
        ocr_text = check_ocr(image_data.siteUrls)
        if(ocr_text):
            print("=====ocr complete=====")
            return "ocr 완료"
        else:
            print("======pic_to_text IMG 시작======")
            detected_text = pic_to_text(image_data)
            print("======detected_text======" , detected_text)

        end_time = time.time()
        print(f"======Time taken(pic_to_text): {end_time - start_time} seconds=======")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return "ocr 완료"

@app.post("/answer")
async def get_answer_from_gpt(message_list: Messages):
    try:
        
        start_time = time.time()
        if(message_list.siteUrls == ''):
            return { "role": "user", "content": "오류발생: 페이지 새로고침 해주세요" }
        print("[message_list]", message_list)
        
        # Extract user input from the message list
        user_input = next((Turn.content for Turn in message_list.messages if Turn.role == "user"), None)
        print("============user_input==========",user_input)
        
        # answer_content = combined_search(user_input, message_list.siteUrls)
        answer_content = await combined_search(user_input, message_list.siteUrls)
        print("============answer_content==========",answer_content)
        answer_gpt = ask_gpt(user_input, answer_content)
        
        results = { "role": "user", "content": answer_gpt }

        end_time = time.time()
        print(f"======Time taken(answer): {end_time - start_time} seconds=======")
        return results
    
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/text-to-speech")
async def text_to_speech(text_request: TextRequest, audio_config: AudioConfig):
    try:
        response = get_audio_from_tts(text_request, audio_config)
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 현재 스크립트가 직접 실행될 때 uvicorn 서버를 시작하고, app 애플리케이션을 사용하여 8000 포트에서 웹 서비스를 제공
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


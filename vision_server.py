import json
import base64
from typing import List
# from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException, Request, UploadFile, File
# from httpx import Timeout
from domain.gptService import get_summary_from_gpt
from domain.ragService import search_documents
from domain.visionService import request_vision_api
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
# from PIL import Image
from io import BytesIO
from domain.ocrService import pic_to_text
from model import ImageList, ImageURL, Messages, Turn, TextRequest
from speech_server import router as speech_router  # 모듈과 변수명을 올바르게 가져옴
import logging

#TTS 임의로 세팅
from google.cloud import texttospeech
from fastapi.responses import JSONResponse

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

# main.html 호출
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

@app.post("/pic_to_text")
async def get_text_from_image(image_data: ImageList):
    try:
        detected_text = pic_to_text(image_data)

        print("============" , detected_text)
        # Get summary from GPT
        # summary = get_summary_from_gpt(detected_text)

        results = [{
            # "summary": summary,
            "original_response": detected_text,
        }]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return results

@app.post("/answer")
async def get_answer_from_gpt(message_list: Messages):
    try:
        # Extract user input from the message list
        user_input = next((Turn.content for Turn in message_list.messages if Turn.role == "user"), None)
        
        # Search through saved text documents
        text_received = search_documents(user_input)

        # Extracting 'answer' content
        answer_content = text_received['answer']

        results = { "role": "user", "content": answer_content }

        return results
    
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Google Cloud Text-to-Speech 클라이언트 생성
client = texttospeech.TextToSpeechClient()

@app.post("/text-to-speech")
async def get_audio_from_tts(text_request: TextRequest):
    try:
        # Text-to-Speech API 요청 생성
        synthesis_input = texttospeech.SynthesisInput(text=text_request.text)

        # VoiceSelectionParams 설정 (한국어)
        voice = texttospeech.VoiceSelectionParams(
            language_code="ko-KR",
            name="ko-KR-Wavenet-A",
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )

        # Text-to-Speech API 요청 보내기
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # 오디오 파일을 저장
        file_path = "output.wav"
        with open(file_path, "wb") as audio_file:
            audio_file.write(response.audio_content)

        return FileResponse(file_path)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#     # Instantiates a client
# client = texttospeech.TextToSpeechClient()

# # Set the text input to be synthesized
# synthesis_input = texttospeech.SynthesisInput(text="Hello, World!")

# # Build the voice request, select the language code ("en-US") and the ssml
# # voice gender ("neutral")
# voice = texttospeech.VoiceSelectionParams(
#     language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
# )

# # Select the type of audio file you want returned
# audio_config = texttospeech.AudioConfig(
#     audio_encoding=texttospeech.AudioEncoding.MP3
# )

# # Perform the text-to-speech request on the text input with the selected
# # voice parameters and audio file type
# response = client.synthesize_speech(
#     input=synthesis_input, voice=voice, audio_config=audio_config
# )

# # The response's audio_content is binary.
# with open("output.mp3", "wb") as out:
#     # Write the response to the output file.
#     out.write(response.audio_content)
#     print('Audio content written to file "output.mp3"')
'''
@app.post("/pic_to_text")
async def get_text_from_image(image_data: ImageList):
    try:
        detected_text = pic_to_text(image_data)

        # Get summary from GPT
        summary = get_summary_from_gpt(detected_text)

        results = []

        results.append({
                "summary": summary,
                "original_response": detected_text
        })
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        results.append({"error": str(e)})

    # return templates.TemplateResponse("result.html", {"request": request, "results": results})
    return results
'''
'''
# OCR 처리(image to text)
@app.post("/vision", response_class=HTMLResponse)
async def vision(request: Request, images: List[UploadFile] = File(...)):
    results = []

    for image in images:
        try:
            # 이미지 읽어오기
            response = requests.get("http://ai.esmplus.com/gded/f/r/20230922/16/1695367250103ddb4993.jpg")
            image_content = response.content
            # img_b64 = base64.b64encode(image_content).decode("utf-8")

            # Convert the content to a PIL Image object
            image = Image.open(BytesIO(image_content))

            # Save the image as JPEG format in memory
            buffered = BytesIO()
            image.save(buffered, format="PDF")

            # Get the JPEG content and encode to base64
            jpeg_content = buffered.getvalue()

            # contents = await image.read()
            
            # base64로 이미지 인코딩
            img_b64 = base64.b64encode(jpeg_content).decode("utf-8") 

            # vision api 호출
            resp = request_vision_api(img_b64, b64=True)

            # JSON 형식의 문자열을 파싱하여 Python 객체(딕셔너리)로 변환
            dict_google_response = json.loads(resp.content)

            # 중요 text부분만 추출
            text_annotations = dict_google_response["responses"][0]["textAnnotations"]
            first_text_annotation = text_annotations[0]

            # Get summary from GPT
            summary = get_summary_from_gpt(first_text_annotation)

            results.append({
                "summary": summary,
                "original_response": first_text_annotation
            })
            
        except Exception as e:
            results.append({"error": str(e)})

    return templates.TemplateResponse("result.html", {"request": request, "results": results})
'''

# 현재 스크립트가 직접 실행될 때 uvicorn 서버를 시작하고, app 애플리케이션을 사용하여 8000 포트에서 웹 서비스를 제공
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


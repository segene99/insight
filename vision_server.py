import json
import base64
from typing import List
# from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from openai import Image
import requests
# from httpx import Timeout
from domain.gptService import get_summary_from_gpt
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
from model import ImageList, ImageURL
from speech_server import router as speech_router  # 모듈과 변수명을 올바르게 가져옴


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

@app.get("/rag", response_class=HTMLResponse)
async def go_to_rag():
    return ""

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


# 현재 스크립트가 직접 실행될 때 uvicorn 서버를 시작하고, app 애플리케이션을 사용하여 8000 포트에서 웹 서비스를 제공
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


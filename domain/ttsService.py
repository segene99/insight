import os
from google.cloud import texttospeech
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from fastapi import HTTPException

# Google Cloud Text-to-Speech 클라이언트 생성
client = texttospeech.TextToSpeechClient()


def get_audio_from_tts(text: str):

    try:
        # Text-to-Speech API 요청 생성
        synthesis_input = texttospeech.SynthesisInput(text=text.text)

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
        folder_path = 'tts_audio'  # Specify the folder path here

        # Check if the folder exists, and if not, create it
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)

        # Save all the detected text to a single txt file
        file_path = os.path.join('tts_audio', "output.wav")

        # 오디오 파일을 저장
        with open(file_path, "wb") as audio_file:
            audio_file.write(response.audio_content)

        return FileResponse(file_path)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def delete_audio_files():
    folder_path = 'tts_audio'  # 폴더 경로를 설정하세요

    # 폴더 내의 모든 파일 리스트 얻기
    file_list = os.listdir(folder_path)

    # 폴더 내의 각 파일 삭제
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        try:
            os.remove(file_path)
            print(f"{file_path} 파일이 삭제되었습니다.")
        except Exception as e:
            print(f"{file_path} 파일 삭제 중 오류 발생: {str(e)}")
            return "Failed to delete audio files"
    return "Audio files have been deleted successfully"
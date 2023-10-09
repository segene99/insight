from google.cloud import texttospeech
from fastapi.responses import JSONResponse

# Google Cloud Text-to-Speech 클라이언트 생성
client = texttospeech.TextToSpeechClient()

def get_audio_from_tts(text: str):
    try:
        # Text-to-Speech API 요청 생성
        synthesis_input = texttospeech.SynthesisInput(text=text)

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
        print(response)

        # 오디오 데이터를 바이너리로 전달
        audio_binary = response.audio_content

        # 바이너리 데이터를 JSON 응답으로 반환
        return JSONResponse(content={"audio_binary": audio_binary.hex()})
    except Exception as e:
        return {"error": str(e)}
    
test = "한국어를 말해줘"
get_audio_from_tts(test)
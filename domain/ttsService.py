import os
from google.cloud import texttospeech
from fastapi.responses import FileResponse
from fastapi import HTTPException
from models import TextRequest, AudioConfig
from langdetect import detect

# Google Cloud Text-to-Speech 클라이언트 생성
client = texttospeech.TextToSpeechClient()

def get_audio_from_tts(text: TextRequest, audio_config: AudioConfig):
    
    user_text = text.user
    assistant_text = text.assistant
    print("=========TTS==========",text)
    print("user_text",user_text)
    print("assistant_text",assistant_text)
    
    print("audio_config : ", audio_config)
    # 소리 크기
    volume = 0
    if(audio_config.volume):
        volume  = audio_config.volume

    # 소리 속도
    speed = 1.26
    if(audio_config.speed):
        speed  = audio_config.speed

    try:
        if(user_text == ""):
            ssml = f"""
                <speak>
                    {assistant_text}
                </speak>
            """
        else:
            ssml = f"""
                <speak>
                    {user_text}<break time="1s"/>{assistant_text}
                </speak>
            """
        # 긴 텍스트를 여러 클립으로 나누기
        # max_clip_length = 1500  # 예시 길이, API의 제한에 따라 조정
        # clips = [text[i:i+max_clip_length] for i in range(0, len(assistant_text), max_clip_length)]

        # audio_clips = []

        # for clip in clips:
        #     # 각 클립에 대한 SSML 생성
        #     ssml = f"""
        #         <speak>
        #             {clip}
        #         </speak>
        #     """

        # user_text가 어떤 언어인지 감지
        assistant_text_language = detect(user_text)

        # audio_option = set_audio_options(assistant_text_language, speed, volume)
        # Text-to-Speech API 요청 생성
        synthesis_input = texttospeech.SynthesisInput(ssml=ssml)

        if assistant_text_language == "ko":  # 한국어인 경우
            # VoiceSelectionParams 설정 (한국어)
            voice = texttospeech.VoiceSelectionParams(
                language_code="ko-KR",
                name="ko-KR-Neural2-A",
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.LINEAR16,
                speaking_rate= speed,  # 음성 속도 [0.25, 4.0]/ 1.0은 기본 속도입니다. 설정되지 않은 경우(0.0) 기본 속도는 기본 1.0입니다. 
                pitch=-3.20,  # 음높이  [-20.0, 20.0] 
                volume_gain_db= volume # 볼륨  [-96.0, 16.0] +6.0(dB) 값은 일반 기본 신호 진폭의 약 2배. +10(dB)을 초과하지 않는 것이 좋음.
            )

        else:  # 영어 목소리 사용
            voice = texttospeech.VoiceSelectionParams(
                language_code="en-US",
                name="en-US-Neural2-E",
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.LINEAR16,
                speaking_rate= speed,  # 음성 속도
                pitch=1.20,  # 음높이 
                volume_gain_db= volume
            )
        # print("|||||||||||||||audio_option: ", audio_option)
        # Text-to-Speech API 요청 보내기
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        # 오디오 클립 저장
        # audio_clips.append(response.audio_content)

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
    
def set_audio_options(detected_langage, speed, volume):

    if detected_langage == "ko":  # 한국어인 경우
        # VoiceSelectionParams 설정 (한국어)
        voice = texttospeech.VoiceSelectionParams(
            language_code="ko-KR",
            name="ko-KR-Neural2-A",
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16,
            speaking_rate= speed,  # 음성 속도 [0.25, 4.0]/ 1.0은 기본 속도입니다. 설정되지 않은 경우(0.0) 기본 속도는 기본 1.0입니다. 
            pitch=-3.20,  # 음높이  [-20.0, 20.0] 
            volume_gain_db= volume # 볼륨  [-96.0, 16.0] +6.0(dB) 값은 일반 기본 신호 진폭의 약 2배. +10(dB)을 초과하지 않는 것이 좋음.
        )

    else:  # 영어 목소리 사용
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Neural2-E",
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16,
            speaking_rate= speed,  # 음성 속도
            pitch=1.20,  # 음높이 
            volume_gain_db= volume
        )
    
    audio_option = {"voice" : voice, "audio_config" : audio_config}
    return audio_option

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

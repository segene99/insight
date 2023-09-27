import openai


def ask_gpt3_turbo(information, question):
    # 모델에게 두 가지 메시지 전달: 시스템 메시지와 사용자 질문 메시지
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question},
        ],
        temperature=0.0,
        max_tokens=150
    )

    # 모델이 생성한 응답
    model_response = response.choices[0].message['content']

    # 모델 응답이 information 텍스트와 관련 없는 경우 알림 메시지로 대체
    if not is_response_relevant(model_response, information):
        model_response = "해당 정보를 찾을 수 없습니다."

    return model_response

def is_response_relevant(response, information):
    # 응답에 information 텍스트와 관련된 단어가 포함되었는지 확인
    response_words = response.split()
    for word in response_words:
        if word in information:
            return True
    return False

if __name__ == "__main__":
    # 긴 정보 텍스트
    information = """
    한국은 동아시아에 위치한 반도 국가로, 북쪽에는 북한, 서쪽에는 황해를 사이에 두고 중국, 남쪽에는 동해를 사이에 두고 일본과 맞닿아 있다. 
    한국의 역사는 고대부터 시작되어, 다양한 왕조와 시대를 거치며 현재의 모습을 이루게 되었다. 
    한국은 전통적으로 농업 사회였으며, 백제, 고구려, 신라와 같은 고대 국가들이 이 지역에서 번성하였다. 
    현대에 들어서는 산업화와 더불어 빠른 경제 성장을 이루어냈고, 현재는 세계적인 경제 강국 중 하나로 자리매김하게 되었다.
    """

    question = input("무엇을 찾아드릴까요?: ")
    response = ask_gpt3_turbo(information, question)

    print("답변:", response)

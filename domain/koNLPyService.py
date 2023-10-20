####한국어 형태소 분석기####
from konlpy.tag import Kkma, Komoran, Okt, Hannanum #Mecab은 윈도우에서 작동 불가능
'''
okt = Okt()
kkma = Kkma()
komoran = Komoran()
hannanum = Hannanum()

text = '나랏말이 중국과 달라 한자와 서로 통하지 아니하므로, \
    우매한 백성들이 말하고 싶은 것이 있어도 마침내 제 뜻을 잘 표현하지 못하는 사람이 많다.\
    내 이를 딱하게 여기어 새로 스물여덟 자를 만들었으니, \
    사람들로 하여금 쉬 익히어 날마다 쓰는 데 편하게 할 뿐이다.'

#### .morphs()함수: 텍스트를 형태소 단위로 나누어준다.####
print("[Kkma morphs 함수]")
print(kkma.morphs(text))
print("[Okt 함수]")
print(okt.morphs(text))
print("[Komoran 함수]")
print(komoran.morphs(text))
print("[Hannanum 함수]")
print(hannanum.morphs(text))

##### stem: 각 단어에서 어간 추출 #####
print("[Okt 함수: stem사용하여 어간 추출]")
print(okt.morphs(text, stem= True))

#### .nouns()함수: 명사를 추출 ####
print("[Kkma nouns 함수]")
print(kkma.nouns(text))
print("[OKt nouns 함수]")
print(okt.nouns(text))
print("[Komoran nouns 함수]")
print(komoran.nouns(text))
print("[Hannanum nouns 함수]")
print(hannanum.nouns(text))

#### .phrases()함수: 어절 추출 ####
print("[Okt phrases 함수]")
print(okt.phrases(text))

#### .pos()함수: 품사 태깅 #### 
print("[Kkma pos 함수]")
print(kkma.pos(text)) #join=True는 형태소와 품사를 붙여서 리스트화
print("[Okt pos 함수]")
print(okt.pos(text))
print("[Komoran pos 함수]")
print(komoran.pos(text))
print("[Hannanum pos 함수]")
print(hannanum.pos(text))
'''
def get_konlpy_text(texts: list[str]) -> list[str]:
    okt = Okt()

    results = []
    morphs_for_text = okt.morphs(texts)
    results.append(morphs_for_text)

    # # Optionally print results
    # for result in results:
    #     print("[okt morphs 함수]")
    #     print(result)

    return results
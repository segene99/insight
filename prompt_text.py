import openai

# keys.txt 파일에서 API 키들을 읽어오는 함수
def read_keys_from_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        openai_key = lines[0].strip().split('=')[1].replace('"', '')
    return openai_key

# keys.txt path
keys_txt_path = 'key/keys.txt'

# keys.txt 파일에서 API 키들을 가져옴
openai_key_value = read_keys_from_file(keys_txt_path)

# 가져온 키를 변수에 대입
openai.api_key = openai_key_value
# 모델과 관련된 상수 설정
MAX_TOKENS = 16000  # gpt-3.5-turbo 모델의 최대 토큰 수
OVERLAP_TOKENS = 50  # 문장이 훼손되지 않게 하기 위한 오버랩 토큰 수

def split_text(text, max_length, overlap):
    sentences = text.split('.')
    chunks = []

    current_chunk = []
    current_length = 0
    for sentence in sentences:
        current_sentence_length = len(sentence)
        if current_length + current_sentence_length + overlap >= max_length:
            chunks.append('. '.join(current_chunk) + '.')
            current_chunk = current_chunk[-overlap:]
            current_length = sum(len(s) for s in current_chunk)
        current_chunk.append(sentence.strip())
        current_length += current_sentence_length

    if current_chunk:
        chunks.append('. '.join(current_chunk) + '.')

    return chunks


def is_valid_response(question, ocr_text, response):
    # 질문의 키워드를 분리
    question_keywords = set(question.split())

    # OCR 텍스트와 응답에 있는 키워드를 분리
    ocr_keywords = set(ocr_text.split())
    response_keywords = set(response.split())

    # 질문의 키워드 중 OCR 텍스트에 없는 것이 응답에 포함되어 있는지 확인
    for keyword in question_keywords:
        if keyword not in ocr_keywords and keyword in response_keywords:
            return False

    return True

def ask_gpt(question, ocr_text):
    text_chunks = split_text(ocr_text, MAX_TOKENS - 300, OVERLAP_TOKENS)
    responses = []

    for chunk in text_chunks:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            temperature=0.0,
            messages=[
                {"role": "system", "content": f"당신은 친절한 쇼핑 도우미입니다. 주어진 OCR 텍스트 안의 정보만을 기반으로 질문에 답하십시오.\n\n{chunk}"},
                {"role": "user", "content": question}
            ]
        )
        
        response_text = response.choices[0].message['content'].strip()
        responses.append(response_text)
        break  # 첫 번째 청크에 대한 응답만 사용하도록 break 추가

    return responses[0]




# 사용자로부터 질문 받기
user_input = input("무엇을 도와드릴까요? ")
#ocr에서 받은 텍스트라 가정
ocr_data = """ 
  Tuntun
ㄴ닷컴
웰빙한끼생식
튼튼닷컴
6년근홍삼정에브리데이
19
M
년근
상업
Bakery
특수클라면
Tuntun
Twi
09
auter
Tuntun
8820
홍삼튼튼박사
SAZU
육종은 제도라지청
Tele
TellC
존존닷법
13
금요일
whi
hre
Tuntun COM
좋은 원료 | 착한가격 | 정직한 제품 | 건강한 생활
(주)튼튼닷컴은 식품의약품안전처로부터 GMP(우수건강기능
식품제조기준)를 획득한 업체와 상호 제휴를 통한 우수한
기술력을 바탕으로 기획에서부터 생산, 품질관리, 출하
과정까지 믿을 수 있는 다양한 제품들을 생산하여, 복잡한
유통구조 없이 소비자에게 직접 판매함으로서 가격거품을
최소화하고, 좋은 제품을 착한 가격에 공급하고자
최선을 다하고 있습니다. 튼튼닷컴
Tuntunc 종합비타민미네랄 (총 12개월분)
1000mg x 180정 x 2개
우수건강기능식품제조기준
GMP
식품의약품안전처
현대인의 불규칙적인 식습관으로 부족하기 쉬운
필수 영양소를 간편하게 보충하실 수 있는 종합
비타민 15종 건강기능식품입니다.
표시광
Traceability
이력추적
식품의약품안전
ARE
건강
기능식품
KHSA
식품의약품안전처
전심의필
GMP
Tuntun COM
튼튼닷컴
종합비타민미네랄
Multi Vitamin Mineral
>>>> 소비기한 2025년 4월 18일 까지 <<<<
V+M] 비타민 13종 + 미네랄 2종
Vit.
건강기능식품
1,000mg x 180정(180g) (62)
Tuntun COM
튼튼닷컴
종합비타민미네랄
Multi Vitamin Mineral
www.tfood.go.kr에서 건강기능식품이력추적
등록번호 3196617 + 제조번호
V+M 비타민 13종 + 미네랄 2층
건강기능식품 D Vit.
1,000mg x 180정(180g)
(사)한국건강기능식품협회 표시 광고 사전심의필
이 광고는 식약처 건강기능식품에 관한 법률에 따른 기능성 표시
광고심의를 받은 내용입니다. [심의번호 : 21410034] ADVANTAGE 특징 및 장점
ADVANTAGE.1
하루 1 정으로 총 15종
복합건강기능식품 섭취
우리 몸에 필요한 비타민과 미네랄을
여러번 섭취하시는 불편없이 하루 1정을
물과 함께 섭취하여 불균형한 식습관으로
부족하기 쉬운 필수 영양소를 간편하게
보충하실 수 있는 건강기능식품입니다.
주원료
부원료
15% +10
비타민미네랄
Tur
ADVANTAGE.3
판
주원료의 원산지를
꼭! 확인하세요
식물혼합추출물
국산①
비오틴
15kg
곳에서
네오
선진국들의 엄격한 검사 기준에 합격된 안전하고
믿을 수 있는 정품 원료들만을 주원료로 사용하였
으며, 식품의약품안전처지정 - GMP첨단시설라인
으로 (품질이 보증된 우수한 건강기능식품을 제조
기준)전 공정에 걸쳐 철저한 품질관리를 통해 제조
하였습니다.
타민 A
합비타민
min Mineral
스위스산
HIESPIA
+ 미네랄 2종
350µg RE
영국산
HIEFPIC
50mg
산화아연(주원료)
정상적인 면역기능에 필요
정상적인 세포분열에 필요
시정 (10%
비타민D(주원료)
칼슘과 인이 흡수되고 이용되는데 필요,
뼈의 형성과 유지에 필요,
골다공증 발생 위험 감소에 도움을 줌
ADVANTAGE.5
비타민K(주원료)
정상적인 혈액응고에 필요, 뼈의 구성에 필요
Va 비타민A
(스위스산)
Ni
Ve
니코틴산아미드
(인도산)
VCHIERIC
(영국산)
비오틴
(국산)
비타민E
(스위스산)
(Fe (독일산)
푸마르산제일철
B2 비타민B2
(독일산)
B6 비타민B6염산염
(독일산)
Jotala
B
Tuntun Com
Pc 판토텐산칼슘
(영국산)
ADVANTAGE.4
Fo 트위스산)
엽산
ADVANTAGE.2
온가족, 남녀노소
누구나 간편하게!
비타민B1 질산염
(독일산)
Vd 비타민D
(스위스산)
VK 비타민K
(스위스산)
Zn 산화아연
(미국산)
총 15종의 주원료
비타민C(영국산)+비타민E(스위스산)+비타민B12(국산)+
푸마르산제일철(독일산)+니코틴산아미드(인도산)+
산화아연(미국산)+비타민A(스위스산)+엽산(스위스산)+
판토텐산칼슘(영국산)+비오틴(국산)+비타민K(스위스산)+
비타민D3(덴마크산) + 비타민B6염산염(독일산)+
비타민B1 질산염(독일산)+비타민B2(독일산)+
다양한 부원료식물혼합추출물10종 +
유당혼합분말(미국산)+유청칼슘(뉴질랜드산) 등을 함유한
제품으로 한통에 6개월분을 담아 오랜 기간동안 넉넉하게
건강을 챙기실 수 있도록 하였습니다.
B12 (국산)
튼튼닷컴
종합비타민미네랄
Multi Vitamin Mineral
V+M] 비타민 13종 + 미네랄 2종
Vit.
건강기능식품
1,000mg×180정 (180g) 6개월분)
비타민B12
ed
Tuntun Com
튼튼닷컴
종합비타민미네랄
Multi Vitamin Mineral
V+M 비타민 13종 + 미네랄 2.
비오틴(주원료)
지방, 탄수화물,
버스 단백질 대사와 에너지 생성에 필요
건강기능식품
1,000mg×180정(180g)
비타민A(주원료)
어두운 곳에서 시각 적응을 위해 필요,
피부와 점막을 형성하고 기능을 유지하는데 필요,
상피세포의 성장과 발달에 필요
비타민C(주원료)
결합조직 형성과 기능유지에 필요,
철의 흡수에 필요,
o 유해산소로부터 세포를 보호하는데 필요
주원료: 스위스산
비타민K 35kg
Vit.
주원료: 스위스산
비타민D 5 g
주원료: 미국산
산화아연 4.25mg 푸마르산제일철 | 비타민A
주원료:독일산
국산
비타민B6염산염 25
0.75mg
일산
민B2
주원료:독일산
원료:스위스
아디 비타민B1질산염 대산
0.6mg
주원료:영국산
료:국산
타민B 판토텐산 칼슘
2.5mg
원료:덴마크산
HELOIN
ADVANTAGE.7
비타민E(주원료)
유해산소로부터 세포를 보호하는데 필요
푸마르산제일철(주원료)
체내 산소운반과 혈액생성에 필요,
에너지 생성에 필요
비타민B2 (주원료)
체내 에너지 생성에 필요
Folic
Vitamin
B12
niacin
content
주원료스위스산
HIELDIE
주원료: 스위스산
엽산 200kg
주원료: 국산
비타민B12 1.2g
주원료:인도산
나이아신 7.5mg NE
ADVANTAGE.9
현대인의 필수 영양소
비타민과 미네랄
주원료
튼튼닷컴
비타민은 우리 몸의 정상적인 발육과 신진
대사에 꼭 필요한 영양소로, 대부분의 비타민은
체내에서 합성되지 않아 반드시 음식이나
비타민제를 통해 보충해야 합니다. 튼튼닷컴
종합비타민미네랄은 몸이 필요로 하는 필수
영양소를 섭취함으로써 건강증진에 도움을
드릴 수 있습니다.
Tuntun
종합비타민미네랄
학 교를
ADVANTAGE.6
비타민B6염산염(주원료)
단백질 및 아미노산 이용에 필요,
혈액의 호모시스테인 수준을 정상으로
유지하는데 필요
비타민B1 질산염(주원료)
탄수화물과 에너지 대사에 필요
판토텐산칼슘(주원료)
지방, 탄수화물, 단백질 대사와
에너지 생성에 필요
주원료:독일산
비타민B2
0.7mg
ADVANTAGE.8
엽산(주원료)
세포와 혈액생성에 필요,
태아 신경관의 정상 발달에 필요,
혈액의 호모시스테인 수준을 정상으로
유지하는데 필요
비타민B12(주원료)
정상적인 엽산 대사에 필요
주원료:스위스산
비타민E
5.5mg a-TE
주원료: 독일산
푸마르산제일철
6mg
나이아신(주원료)
체내에너지 생성에 필요
GMP
Tuntun COM ADVANTAGE.10
기능식품
Tuntun COM
V+M 비타민
튼튼닷컴
종합비타민미네랄
Multi Vitamin Mineral
주원료15종
vit
건강기능식품
1,000mg×180정(180g) 6개월
이런분들께 권해드립니다.
기초적인 영양섭취가 부족하신 분
활력 있는 생활을 원하시는 분
항산화 성분의 보충이 필요하신 분
평소에 활동량이 많으신 분
건강증진이 필요하신 분
규칙적으로 균형잡힌 식사를 하지 못하시는 분
바쁜 일상생활로 인해 식습관이 불규칙적이신 분
과다한 업무 등으로 지친 직장인
비타민 섭취에 신경써야 하는 노인 및 여성분
다양한 영양소를 필요로 하는 성장기 어린이 및
청소년 ADVANTAGE.11
식품의약품안전처에
품목제조신고를 마친
건강기능식품
본 제품은 GMP(우수 건강기능식품 제조기준)
라인에서 엄격한 품질관리와 위생관리를 통해
생산되었으며, 식품의약품안전처에 품목제조
신고를 마친 건강기능식품입니다.
DETAIL
250g
lice 15
1803(180g)
Tun COM
튼튼닷컴
종합비타민미네랄
V.M 비타민 13층 + 미네랄 2층
Vita
Tuntun Com
튼튼닷컴
종합비타민미네랄
MuVimin Mineral
V+M 비타민 13종 + 미네랄 2층
KOMP
Vit.
2004-0006-1257
건강기능식품품목제조신고증
영업허가번호)
업소명
영업의종류
4 * 명
튼튼닷컴 종합비타민미네랄 1000mg X 180정 X 2개 (12개월분)
튼튼닷컴 종합비타민미네랄은 하루 1정으로 총 15종 복합 기능성을 간편하게 섭취하실 수 있는
복합 기능성 건강기능식품입니다. 식물혼합추출물 10종 외 부원료를 함유 하였습니다.
해당 제품은 선진국들의 엄격한 검사 기준에 합격된 안전하고 믿을 수 있는 좋은 원료들만을
주원료로 사용하였습니다.
2004-대전청-0006 호
주식회사 노바렉스
충청북도 청주시 청원구 오창읍 각리1길 94
건강기능식품전문제조업
UM
닷험 종합비타민미네랄
품목 제조 조건:
건강기능식품에관한법률 제7조 및 동법
시행규칙 제8조의 규정에 따라 건강기능
식품품목제조신고를 수리합니다.
20140905
대전지방식품의약품안전청장
영상
176
UM
U 비타민미네랄 15종(주원료)
식물혼합추출물 10종외(부원료)
더덕, 황기, 복령, 진피, 백출, 당귀,
동충하초(눈꽃), 영지버섯, 구기자
유청칼슘(뉴질랜드산/우유),
유당혼합분말(미국산)
GMP
Tuntun Com
건강
기능식품
튼튼닷컴
종합비타민미네랄
Multi Vitamin Mineral
건강기능식품
V+M] 비타민 13종 + 미네랄 2종
180정(1
Vit.
주원료
원산지
비오틴 - 국산
비타민B12 - 국산
비타민C - 영국산
판토텐산칼슘 - 영국산
| 비타민A-스위스산
비타민E - 스위스산
비타민K - 스위스산
엽산 - 스위스산
비타민D - 덴마크산
|니코틴산아미드-인도산
비타민B1 질산염 - 독일산
비타민B2 - 독일산
산화아연 - 미국산
비타민B6염산염 - 독일산
|푸마르산제일철 - 독일산
50%
50%
50%
50%
50%
50%
50%
50%
50%
50%
50%
50%
50%
50%
50% 제품명
소비자상담 전화번호
주문후 예상 배송기간
생산자 및 소재지
포장단위별 용량/수량
원료명 및 함량
영양성분
상품정보제공 고시
튼튼닷컴 종합비타민미네랄
031-792-5386 (긴급상담 010-4429-5384)
최소 1일 ~ 최대 5일 (택배사 사정에 따른 배송사고 제외)
㈜노바렉스, 충북 청주시 흥덕구 오송읍 오송생명14로 80
1000 mg x 180 정 (180 g) x 2개
비타민C(영국산), 혼합제제(프랑스산/dl-a-토코페릴아세테이트, 옥테닐호박산
나트륨전분, 포도당시럽분말, 이산화규소), 푸마르산제일철(독일산), 니코틴산
아미드(인도산), 산화아연(미국산), 혼합제제(스위스산/비타민A아세테이트,
포도당시럽분말, 아라비아검, 옥수수전분, dl-a-토코페롤), 판토텐산칼슘(영국산),
혼합제제(스위스산/비타민D3, 아카시아검, 자당, 옥수수전분, 팜유, 이산화규소,
dl-a-토코페롤), 혼합제제(비오틴(프랑스산), 제이인산칼슘}, 비타민B6염산염
(독일산), 비타민B1질산염(독일산), 비타민B2(독일산), 혼합제제(스위스산/
비타민K1, 아라비아검, 수크로스), 엽산(스위스산),혼합제제{비타민B12(프랑스산),
제이인산칼슘, 덱스트린, 결정셀룰로스, 유당혼합분말{유당(미국산), 덱스트린},
밀크칼슘(뉴질랜드산), 히드록시프로필메틸셀룰로스, 스테아린산마그네슘, 이산화
티타늄(착색료), 혼합제제(글리세린지방산에스테르, 프로필렌글리콜, 구연산),
치자황색소 우유 함유
총 180일 섭취량/1일 섭취량 1정당(1,000 mg)함량:
열량 0kcal, 탄수화물 1g미만(0%), 단백질 0g (0%),
지방0g(0%), 나트륨 0mg (0%), 비타민A 350g REA (50%),
비타민B10.6mg (50%), 비타민B2 0.7 mg (50%),
나이아신 7.5 mg NE (50%), 판토텐산 2.5 mg (50%),
비타민B6 0.75 mg (50%), 비오틴 15g (50%),
엽산 200 g(50%), 비타민B12 1.2 g (50%),
비타민C 50 mg (50%), 비타민D5g (50%),
비타민E 5.5 mg a-TE (50%), 비타민K 35 g (50%),
철 6 mg (50%), 아연 4.25 mg(50%)
※ ()안의 수치는 1일 영양성분기준치에 대한 비율임 기능정보
섭취량, 섭취방법
섭취시 주의사항
소비기한 및 보관방법
• 비타민A: 어두운 곳에서 시각 적응을 위해 필요,
피부와 점막을 형성하고 기능을 유지하는데 필요,
상피세포의 성장과 발달에 필요
• 비타민B1 : 탄수화물과 에너지 대사에 필요
• 비타민B2 : 체내 에너지 생성에 필요
-비타민B6: 단백질 및 아미노산 이용에 필요
혈액의 호모시스테인 수준을 정상으로 유지하는데 필요
• 비타민B12 : 정상적인 엽산 대사에 필요
• 비타민C:결합조직 형성과 기능유지에 필요,
철의 흡수에 필요,
유해산소로부터 세포를 보호하는데 필요
• 비타민D:칼슘과 인이 흡수되고 이용되는데 필요,
뼈의 형성과 유지에 필요,
골다공증발생 위험 감소에 도움을 줌
• 비타민E : 항산화 작용을 하여 유해산소로부터 세포를 보호하는데 필요
• 비타민K: 정상적인 혈액응고에 필요,
뼈의 구성에 필요
・나이아신 : 체내 에너지 생성에 필요
• 판토텐산지방, 탄수화물, 단백질 대사와 에너지 생성에 필요
비오틴 : 지방, 탄수화물, 단백질 대사와 에너지 생성에 필요
·엽산 세포와 혈액생성에 필요, 태아 신경관의 정상 발달에 필요,
혈액의 호모시스테인 수준을 정상으로 유지하는데 필요
아연 : 정상적인 면역기능에 필요, 정상적인 세포분열에 필요
• 철 : 체내 산소운반과 혈액생성에 필요, 에너지 생성에 필요
1일 1회, 1회 1정을 물과 함께 섭취하십시오.
특정질환, 특이체질, 알레르기 체질, 임산부의 경우에는 간혹 개인에 따라 과민
반응이 나타날 수 있으므로 원료를 확인하시고, 섭취 전에 전문가와 상담하시기
바랍니다. 특히 6세 이하는 과량섭취하지 않도록 주의. 고칼슘혈증이 있거나
의약품 복용 시 전문가와 상담할 것.
동봉된 방습제는 절대 섭취하지 마십시오. 항응고제 등 복용 시 전문가와 상담할 것.
제조년월일:2023년 04월 19일
소비기한:2025년 04월 18일까지인 상품을 주문서 접수 순서에 따라 순차 발송
보관방법 :
- 고온다습한 곳과 직사광선을 피하여 습기가 적고 건조한 곳에 보관하십시오.
- 개봉 후에는 뚜껑을 닫고 공기의 노출을 최대한 차단하여 보관하십시오.
- 영유아 및 어린이의 손에 닿지 않는 곳에 보관하십시오.
소비자안전을 위한 주의사항
※ 이 제품은 알레르기 발생 가능성이 있는 알류(가금류), 메밀, 땅콩, 대두, 밀, 고등어,
게, 새우, 돼지고기, 복숭아, 토마토, 아황산류, 호두, 닭고기, 쇠고기, 오징어, 조개류(굴,
전복, 홍합 포함), 잣을 사용한 제품과 같은 시설에서 제조하였습니다.
※ 본 제품은 질병의 예방 및 치료를 위한 의약품이 아닙니다. |
건강정보
‘비타민(vitamin)이란 무엇일까요?
'생동력(生動力)을 가진 아민(amin) 물질'이라는 뜻을 가지고 있으며,
신체의 정상적인 기능과 성장 및 유지를 위해 식이를 통해 미량을
섭취해야하는 필수적인 유기(有機) 물질입니다.
비타민은 체내에서 한가지 이상의 생화학적 작용이나 생리적
작용에 관여하므로 정상적인 체내 기능을 위해 반드시 필요
합니다. 대부분의 비타민은 체내에서 전혀 합성되지
못하거나 또는 합성되는 양이 필요량에 미치지 못하기
때문에 반드시 식품으로 섭취해야합니다.
‘미네랄(mineral)이란 무엇일까요?
미네랄은 탄수화물, 단백질, 지방, 비타민과 함께 5대 영양소에 포함되며,
모든 생명체를 구성하는 필수원소로써 탄소, 수소, 산소, 질소 등 네가지
원소를 제외한 알루미늄, 철, 마그네슘, 칼슘, 구리, 망간, 크롬 등의 인체를
구성하는 원소들의 총칭으로 미량이지만 신체기능 조절 유지에 없어서는
안될 중요 영양소입니다.
미네랄은 세포의 건강과 밀접한 관계를 가지기 때문에 우리 몸에서 부족하지 않도록
충분히 섭취하는 것이 중요합니다. 또한 미네랄은 아미노산, 지방산, 비타민을 사용하는
신체기능에 촉매역할을 합니다. 다른 영양분을 많이 섭취하더라도, 미네랄의 상호작용
없이는 영양분으로부터 필요한 기능을 얻어낼 수 없습니다. 건강을 지속적으로 유지하기
위해서는 우리 몸에 미네랄을 계속 보충해야만하는 것입니다. 미네랄은 비타민과
효소를 활동케함으로써 몸의 기능을 조절하고 유지하는 데 없어서는 안 되는 중요한
영양소입니다. ※ 구매 전 꼭 읽어주세요.
★ 주문시 확인사항 (배송안내)
택배사 : 우체국택배 또는 롯데택배
(제주도 및 도서산간 추가배송비가 추가되지 않습니다)
당일 발송 마감시간 : 평일 오후 3시까지 (토, 일, 공휴일 휴무)
평일 오후 3시 이후 접수건은 익일 발송됩니다.
· 금요일 오후 3시 이후 주문건은 월요일에 발송됩니다.
택배 배송상품은 평시에는 토, 일, 공휴일 제외한 영업일 기준 2~3일 정도 여유를 두고
미리 주문하시는 것이 좋습니다.
(택배사의 지역배송사정에 따라 간혹 배송에는 1~2일이 더 소요될수도 있기 때문입니다.)
제주도 및 도서산간 지역은 날씨 등 배송사정에 따라 배송에 1~5일이 더 소요될 수 있습니다.
천재지변, 설 및 추석 명절기간 등 택배물량이 증가하는 시기에는 2일~5일정도 배송이
지연될 수 있으니 참고 바랍니다.
★ 상품 수령 후 확인사항 안내
- 제품 수령 후 상품 개봉 전, 주문 내역과 배송된 상품이 맞는지 확인하시기 바랍니다.
- 제품 수령 후 주문 내역과 배송 상품이 상이한 경우 제품을 개봉하지 마시고 수령하신 그대로
택배박스(송장 포함)와 함께 보관하시고 즉시 판매자에게 연락 또는 문의주시기 바랍니다.
[판매자와 연락 전에 제품을 개봉하시거나 택배박스(송장포함)를 폐기하시면 처리가 지연되거나
거부될 수 있습니다]
★ 반품 및 교환 안내
1. 반품 및 교환이 가능한 경우
상품 수령 후 개봉하지 않으신 경우에 한해서, 수령일로부터 7일 이내에 교환 및 반품이 가능합니다.
- 상품 불량이나 파손 등 하자에 의한 교환 또는 반품 비용은 판매자가 부담합니다.
고객 변심 또는 고객 착오로 인한 교환 또는 반품 비용은 고객님께서 부담하셔야 합니다.
(왕복배송료 5,000원)
-반품 또는 교환시 제품이 손상되지 않도록 필히 택배박스에 담아 완충해 주시기 바랍니다.
(제품의 외부 지함케이스가 훼손되지 않도록 주의바랍니다)
- 진료 확인서 및 소견서 등의 증빙이 필요한 경우 제반비용 고객부담
2. 반품 및 교환, 환불이 불가능한 경우
제품의 특성상 개봉 또는 구성품의 누락, 상품가치가 상실된 경우
(제품의 외부 지함케이스도 중요한 제품의 구성품이므로 외부 지함케이스를
훼손한 경우도 포함됨)
상품을 사용하거나 일부 소비에 의하여 상품가치가 현저히 감소한 경우
- 시간의 경과에 의하여 재판매가 곤란할 정도로 상품가치가 현저히 감소한 경우   Tuntun
ㄴ닷컴
웰빙한끼생식
튼튼닷컴
6년근홍삼정에브리데이
19
M
년근
상업
Bakery
특수클라면
Tuntun
Twi
09
auter
Tuntun
8820
홍삼튼튼박사
SAZU
육종은 제도라지청
Tele
TellC
존존닷법
13
금요일
whi
hre
Tuntun COM
좋은 원료 | 착한가격 | 정직한 제품 | 건강한 생활
(주)튼튼닷컴은 식품의약품안전처로부터 GMP(우수건강기능
식품제조기준)를 획득한 업체와 상호 제휴를 통한 우수한
기술력을 바탕으로 기획에서부터 생산, 품질관리, 출하
과정까지 믿을 수 있는 다양한 제품들을 생산하여, 복잡한
유통구조 없이 소비자에게 직접 판매함으로서 가격거품을
최소화하고, 좋은 제품을 착한 가격에 공급하고자
최선을 다하고 있습니다. 튼튼닷컴
Tuntunc 종합비타민미네랄 (총 12개월분)
1000mg x 180정 x 2개
우수건강기능식품제조기준
GMP
식품의약품안전처
현대인의 불규칙적인 식습관으로 부족하기 쉬운
필수 영양소를 간편하게 보충하실 수 있는 종합
비타민 15종 건강기능식품입니다.
표시광
Traceability
이력추적
식품의약품안전
ARE
건강
기능식품
KHSA
식품의약품안전처
전심의필
GMP
Tuntun COM
튼튼닷컴
종합비타민미네랄
Multi Vitamin Mineral
>>>> 소비기한 2025년 4월 18일 까지 <<<<
V+M] 비타민 13종 + 미네랄 2종
Vit.
건강기능식품
1,000mg x 180정(180g) (62)
Tuntun COM
튼튼닷컴
종합비타민미네랄
Multi Vitamin Mineral
www.tfood.go.kr에서 건강기능식품이력추적
등록번호 3196617 + 제조번호
V+M 비타민 13종 + 미네랄 2층
건강기능식품 D Vit.
1,000mg x 180정(180g)
(사)한국건강기능식품협회 표시 광고 사전심의필
이 광고는 식약처 건강기능식품에 관한 법률에 따른 기능성 표시
광고심의를 받은 내용입니다. [심의번호 : 21410034] ADVANTAGE 특징 및 장점
ADVANTAGE.1
하루 1 정으로 총 15종
복합건강기능식품 섭취
우리 몸에 필요한 비타민과 미네랄을
여러번 섭취하시는 불편없이 하루 1정을
물과 함께 섭취하여 불균형한 식습관으로
부족하기 쉬운 필수 영양소를 간편하게
보충하실 수 있는 건강기능식품입니다.
주원료
부원료
15% +10
비타민미네랄
Tur
ADVANTAGE.3
판
주원료의 원산지를
꼭! 확인하세요
식물혼합추출물
국산①
비오틴
15kg
곳에서
네오
선진국들의 엄격한 검사 기준에 합격된 안전하고
믿을 수 있는 정품 원료들만을 주원료로 사용하였
으며, 식품의약품안전처지정 - GMP첨단시설라인
으로 (품질이 보증된 우수한 건강기능식품을 제조
기준)전 공정에 걸쳐 철저한 품질관리를 통해 제조
하였습니다.
타민 A
합비타민
min Mineral
스위스산
HIESPIA
+ 미네랄 2종
350µg RE
영국산
HIEFPIC
50mg
산화아연(주원료)
정상적인 면역기능에 필요
정상적인 세포분열에 필요
시정 (10%
비타민D(주원료)
칼슘과 인이 흡수되고 이용되는데 필요,
뼈의 형성과 유지에 필요,
골다공증 발생 위험 감소에 도움을 줌
ADVANTAGE.5
비타민K(주원료)
정상적인 혈액응고에 필요, 뼈의 구성에 필요
Va 비타민A
(스위스산)
Ni
Ve
니코틴산아미드
(인도산)
VCHIERIC
(영국산)
비오틴
(국산)
비타민E
(스위스산)
(Fe (독일산)
푸마르산제일철
B2 비타민B2
(독일산)
B6 비타민B6염산염
(독일산)
Jotala
B
Tuntun Com
Pc 판토텐산칼슘
(영국산)
ADVANTAGE.4
Fo 트위스산)
엽산
ADVANTAGE.2
온가족, 남녀노소
누구나 간편하게!
비타민B1 질산염
(독일산)
Vd 비타민D
(스위스산)
VK 비타민K
(스위스산)
Zn 산화아연
(미국산)
총 15종의 주원료
비타민C(영국산)+비타민E(스위스산)+비타민B12(국산)+
푸마르산제일철(독일산)+니코틴산아미드(인도산)+
산화아연(미국산)+비타민A(스위스산)+엽산(스위스산)+
판토텐산칼슘(영국산)+비오틴(국산)+비타민K(스위스산)+
비타민D3(덴마크산) + 비타민B6염산염(독일산)+
비타민B1 질산염(독일산)+비타민B2(독일산)+
다양한 부원료식물혼합추출물10종 +
유당혼합분말(미국산)+유청칼슘(뉴질랜드산) 등을 함유한
제품으로 한통에 6개월분을 담아 오랜 기간동안 넉넉하게
건강을 챙기실 수 있도록 하였습니다.
B12 (국산)
튼튼닷컴
종합비타민미네랄
Multi Vitamin Mineral
V+M] 비타민 13종 + 미네랄 2종
Vit.
건강기능식품
1,000mg×180정 (180g) 6개월분)
비타민B12
ed
Tuntun Com
튼튼닷컴
종합비타민미네랄
Multi Vitamin Mineral
V+M 비타민 13종 + 미네랄 2.
비오틴(주원료)
지방, 탄수화물,
버스 단백질 대사와 에너지 생성에 필요
건강기능식품
1,000mg×180정(180g)
비타민A(주원료)
어두운 곳에서 시각 적응을 위해 필요,
피부와 점막을 형성하고 기능을 유지하는데 필요,
상피세포의 성장과 발달에 필요
비타민C(주원료)
결합조직 형성과 기능유지에 필요,
철의 흡수에 필요,
o 유해산소로부터 세포를 보호하는데 필요
주원료: 스위스산
비타민K 35kg
Vit.
주원료: 스위스산
비타민D 5 g
주원료: 미국산
산화아연 4.25mg 푸마르산제일철 | 비타민A
주원료:독일산
국산
비타민B6염산염 25
0.75mg
일산
민B2
주원료:독일산
원료:스위스
아디 비타민B1질산염 대산
0.6mg
주원료:영국산
료:국산
타민B 판토텐산 칼슘
2.5mg
원료:덴마크산
HELOIN
ADVANTAGE.7
비타민E(주원료)
유해산소로부터 세포를 보호하는데 필요
푸마르산제일철(주원료)
체내 산소운반과 혈액생성에 필요,
에너지 생성에 필요
비타민B2 (주원료)
체내 에너지 생성에 필요
Folic
Vitamin
B12
niacin
content
주원료스위스산
HIELDIE
주원료: 스위스산
엽산 200kg
주원료: 국산
비타민B12 1.2g
주원료:인도산
나이아신 7.5mg NE
ADVANTAGE.9
현대인의 필수 영양소
비타민과 미네랄
주원료
튼튼닷컴
비타민은 우리 몸의 정상적인 발육과 신진
대사에 꼭 필요한 영양소로, 대부분의 비타민은
체내에서 합성되지 않아 반드시 음식이나
비타민제를 통해 보충해야 합니다. 튼튼닷컴
종합비타민미네랄은 몸이 필요로 하는 필수
영양소를 섭취함으로써 건강증진에 도움을
드릴 수 있습니다.
Tuntun
종합비타민미네랄
학 교를
ADVANTAGE.6
비타민B6염산염(주원료)
단백질 및 아미노산 이용에 필요,
혈액의 호모시스테인 수준을 정상으로
유지하는데 필요
비타민B1 질산염(주원료)
탄수화물과 에너지 대사에 필요
판토텐산칼슘(주원료)
지방, 탄수화물, 단백질 대사와
에너지 생성에 필요
주원료:독일산
비타민B2
0.7mg
ADVANTAGE.8
엽산(주원료)
세포와 혈액생성에 필요,
태아 신경관의 정상 발달에 필요,
혈액의 호모시스테인 수준을 정상으로
유지하는데 필요
비타민B12(주원료)
정상적인 엽산 대사에 필요
주원료:스위스산
비타민E
5.5mg a-TE
주원료: 독일산
푸마르산제일철
6mg
나이아신(주원료)
체내에너지 생성에 필요
GMP
Tuntun COM ADVANTAGE.10
기능식품
Tuntun COM
V+M 비타민
튼튼닷컴
종합비타민미네랄
Multi Vitamin Mineral
주원료15종
vit
건강기능식품
1,000mg×180정(180g) 6개월
이런분들께 권해드립니다.
기초적인 영양섭취가 부족하신 분
활력 있는 생활을 원하시는 분
항산화 성분의 보충이 필요하신 분
평소에 활동량이 많으신 분
건강증진이 필요하신 분
규칙적으로 균형잡힌 식사를 하지 못하시는 분
바쁜 일상생활로 인해 식습관이 불규칙적이신 분
과다한 업무 등으로 지친 직장인
비타민 섭취에 신경써야 하는 노인 및 여성분
다양한 영양소를 필요로 하는 성장기 어린이 및
청소년 ADVANTAGE.11
식품의약품안전처에
품목제조신고를 마친
건강기능식품
본 제품은 GMP(우수 건강기능식품 제조기준)
라인에서 엄격한 품질관리와 위생관리를 통해
생산되었으며, 식품의약품안전처에 품목제조
신고를 마친 건강기능식품입니다.
DETAIL
250g
lice 15
1803(180g)
Tun COM
튼튼닷컴
종합비타민미네랄
V.M 비타민 13층 + 미네랄 2층
Vita
Tuntun Com
튼튼닷컴
종합비타민미네랄
MuVimin Mineral
V+M 비타민 13종 + 미네랄 2층
KOMP
Vit.
2004-0006-1257
건강기능식품품목제조신고증
영업허가번호)
업소명
영업의종류
4 * 명
튼튼닷컴 종합비타민미네랄 1000mg X 180정 X 2개 (12개월분)
튼튼닷컴 종합비타민미네랄은 하루 1정으로 총 15종 복합 기능성을 간편하게 섭취하실 수 있는
복합 기능성 건강기능식품입니다. 식물혼합추출물 10종 외 부원료를 함유 하였습니다.
해당 제품은 선진국들의 엄격한 검사 기준에 합격된 안전하고 믿을 수 있는 좋은 원료들만을
주원료로 사용하였습니다.
2004-대전청-0006 호
주식회사 노바렉스
충청북도 청주시 청원구 오창읍 각리1길 94
건강기능식품전문제조업
UM
닷험 종합비타민미네랄
품목 제조 조건:
건강기능식품에관한법률 제7조 및 동법
시행규칙 제8조의 규정에 따라 건강기능
식품품목제조신고를 수리합니다.
20140905
대전지방식품의약품안전청장
영상
176
UM
U 비타민미네랄 15종(주원료)
식물혼합추출물 10종외(부원료)
더덕, 황기, 복령, 진피, 백출, 당귀,
동충하초(눈꽃), 영지버섯, 구기자
유청칼슘(뉴질랜드산/우유),
유당혼합분말(미국산)
GMP
Tuntun Com
건강
기능식품
튼튼닷컴
종합비타민미네랄
Multi Vitamin Mineral
건강기능식품
V+M] 비타민 13종 + 미네랄 2종
180정(1
Vit.
주원료
원산지
비오틴 - 국산
비타민B12 - 국산
비타민C - 영국산
판토텐산칼슘 - 영국산
| 비타민A-스위스산
비타민E - 스위스산
비타민K - 스위스산
엽산 - 스위스산
비타민D - 덴마크산
|니코틴산아미드-인도산
비타민B1 질산염 - 독일산
비타민B2 - 독일산
산화아연 - 미국산
비타민B6염산염 - 독일산
|푸마르산제일철 - 독일산
50%
50%
50%
50%
50%
50%
50%
50%
50%
50%
50%
50%
50%
50%
50% 제품명
소비자상담 전화번호
주문후 예상 배송기간
생산자 및 소재지
포장단위별 용량/수량
원료명 및 함량
영양성분
상품정보제공 고시
튼튼닷컴 종합비타민미네랄
031-792-5386 (긴급상담 010-4429-5384)
최소 1일 ~ 최대 5일 (택배사 사정에 따른 배송사고 제외)
㈜노바렉스, 충북 청주시 흥덕구 오송읍 오송생명14로 80
1000 mg x 180 정 (180 g) x 2개
비타민C(영국산), 혼합제제(프랑스산/dl-a-토코페릴아세테이트, 옥테닐호박산
나트륨전분, 포도당시럽분말, 이산화규소), 푸마르산제일철(독일산), 니코틴산
아미드(인도산), 산화아연(미국산), 혼합제제(스위스산/비타민A아세테이트,
포도당시럽분말, 아라비아검, 옥수수전분, dl-a-토코페롤), 판토텐산칼슘(영국산),
혼합제제(스위스산/비타민D3, 아카시아검, 자당, 옥수수전분, 팜유, 이산화규소,
dl-a-토코페롤), 혼합제제(비오틴(프랑스산), 제이인산칼슘}, 비타민B6염산염
(독일산), 비타민B1질산염(독일산), 비타민B2(독일산), 혼합제제(스위스산/
비타민K1, 아라비아검, 수크로스), 엽산(스위스산),혼합제제{비타민B12(프랑스산),
제이인산칼슘, 덱스트린, 결정셀룰로스, 유당혼합분말{유당(미국산), 덱스트린},
밀크칼슘(뉴질랜드산), 히드록시프로필메틸셀룰로스, 스테아린산마그네슘, 이산화
티타늄(착색료), 혼합제제(글리세린지방산에스테르, 프로필렌글리콜, 구연산),
치자황색소 우유 함유
총 180일 섭취량/1일 섭취량 1정당(1,000 mg)함량:
열량 0kcal, 탄수화물 1g미만(0%), 단백질 0g (0%),
지방0g(0%), 나트륨 0mg (0%), 비타민A 350g REA (50%),
비타민B10.6mg (50%), 비타민B2 0.7 mg (50%),
나이아신 7.5 mg NE (50%), 판토텐산 2.5 mg (50%),
비타민B6 0.75 mg (50%), 비오틴 15g (50%),
엽산 200 g(50%), 비타민B12 1.2 g (50%),
비타민C 50 mg (50%), 비타민D5g (50%),
비타민E 5.5 mg a-TE (50%), 비타민K 35 g (50%),
철 6 mg (50%), 아연 4.25 mg(50%)
※ ()안의 수치는 1일 영양성분기준치에 대한 비율임 기능정보
섭취량, 섭취방법
섭취시 주의사항
소비기한 및 보관방법
• 비타민A: 어두운 곳에서 시각 적응을 위해 필요,
피부와 점막을 형성하고 기능을 유지하는데 필요,
상피세포의 성장과 발달에 필요
• 비타민B1 : 탄수화물과 에너지 대사에 필요
• 비타민B2 : 체내 에너지 생성에 필요
-비타민B6: 단백질 및 아미노산 이용에 필요
혈액의 호모시스테인 수준을 정상으로 유지하는데 필요
• 비타민B12 : 정상적인 엽산 대사에 필요
• 비타민C:결합조직 형성과 기능유지에 필요,
철의 흡수에 필요,
유해산소로부터 세포를 보호하는데 필요
• 비타민D:칼슘과 인이 흡수되고 이용되는데 필요,
뼈의 형성과 유지에 필요,
골다공증발생 위험 감소에 도움을 줌
• 비타민E : 항산화 작용을 하여 유해산소로부터 세포를 보호하는데 필요
• 비타민K: 정상적인 혈액응고에 필요,
뼈의 구성에 필요
・나이아신 : 체내 에너지 생성에 필요
• 판토텐산지방, 탄수화물, 단백질 대사와 에너지 생성에 필요
비오틴 : 지방, 탄수화물, 단백질 대사와 에너지 생성에 필요
·엽산 세포와 혈액생성에 필요, 태아 신경관의 정상 발달에 필요,
혈액의 호모시스테인 수준을 정상으로 유지하는데 필요
아연 : 정상적인 면역기능에 필요, 정상적인 세포분열에 필요
• 철 : 체내 산소운반과 혈액생성에 필요, 에너지 생성에 필요
1일 1회, 1회 1정을 물과 함께 섭취하십시오.
특정질환, 특이체질, 알레르기 체질, 임산부의 경우에는 간혹 개인에 따라 과민
반응이 나타날 수 있으므로 원료를 확인하시고, 섭취 전에 전문가와 상담하시기
바랍니다. 특히 6세 이하는 과량섭취하지 않도록 주의. 고칼슘혈증이 있거나
의약품 복용 시 전문가와 상담할 것.
동봉된 방습제는 절대 섭취하지 마십시오. 항응고제 등 복용 시 전문가와 상담할 것.
제조년월일:2023년 04월 19일
소비기한:2025년 04월 18일까지인 상품을 주문서 접수 순서에 따라 순차 발송
보관방법 :
- 고온다습한 곳과 직사광선을 피하여 습기가 적고 건조한 곳에 보관하십시오.
- 개봉 후에는 뚜껑을 닫고 공기의 노출을 최대한 차단하여 보관하십시오.
- 영유아 및 어린이의 손에 닿지 않는 곳에 보관하십시오.
소비자안전을 위한 주의사항
※ 이 제품은 알레르기 발생 가능성이 있는 알류(가금류), 메밀, 땅콩, 대두, 밀, 고등어,
게, 새우, 돼지고기, 복숭아, 토마토, 아황산류, 호두, 닭고기, 쇠고기, 오징어, 조개류(굴,
전복, 홍합 포함), 잣을 사용한 제품과 같은 시설에서 제조하였습니다.
※ 본 제품은 질병의 예방 및 치료를 위한 의약품이 아닙니다. |
건강정보
‘비타민(vitamin)이란 무엇일까요?
'생동력(生動力)을 가진 아민(amin) 물질'이라는 뜻을 가지고 있으며,
신체의 정상적인 기능과 성장 및 유지를 위해 식이를 통해 미량을
섭취해야하는 필수적인 유기(有機) 물질입니다.
비타민은 체내에서 한가지 이상의 생화학적 작용이나 생리적
작용에 관여하므로 정상적인 체내 기능을 위해 반드시 필요
합니다. 대부분의 비타민은 체내에서 전혀 합성되지
못하거나 또는 합성되는 양이 필요량에 미치지 못하기
때문에 반드시 식품으로 섭취해야합니다.
‘미네랄(mineral)이란 무엇일까요?
미네랄은 탄수화물, 단백질, 지방, 비타민과 함께 5대 영양소에 포함되며,
모든 생명체를 구성하는 필수원소로써 탄소, 수소, 산소, 질소 등 네가지
원소를 제외한 알루미늄, 철, 마그네슘, 칼슘, 구리, 망간, 크롬 등의 인체를
구성하는 원소들의 총칭으로 미량이지만 신체기능 조절 유지에 없어서는
안될 중요 영양소입니다.
미네랄은 세포의 건강과 밀접한 관계를 가지기 때문에 우리 몸에서 부족하지 않도록
충분히 섭취하는 것이 중요합니다. 또한 미네랄은 아미노산, 지방산, 비타민을 사용하는
신체기능에 촉매역할을 합니다. 다른 영양분을 많이 섭취하더라도, 미네랄의 상호작용
없이는 영양분으로부터 필요한 기능을 얻어낼 수 없습니다. 건강을 지속적으로 유지하기
위해서는 우리 몸에 미네랄을 계속 보충해야만하는 것입니다. 미네랄은 비타민과
효소를 활동케함으로써 몸의 기능을 조절하고 유지하는 데 없어서는 안 되는 중요한
영양소입니다. ※ 구매 전 꼭 읽어주세요.
★ 주문시 확인사항 (배송안내)
택배사 : 우체국택배 또는 롯데택배
(제주도 및 도서산간 추가배송비가 추가되지 않습니다)
당일 발송 마감시간 : 평일 오후 3시까지 (토, 일, 공휴일 휴무)
평일 오후 3시 이후 접수건은 익일 발송됩니다.
· 금요일 오후 3시 이후 주문건은 월요일에 발송됩니다.
택배 배송상품은 평시에는 토, 일, 공휴일 제외한 영업일 기준 2~3일 정도 여유를 두고
미리 주문하시는 것이 좋습니다.
(택배사의 지역배송사정에 따라 간혹 배송에는 1~2일이 더 소요될수도 있기 때문입니다.)
제주도 및 도서산간 지역은 날씨 등 배송사정에 따라 배송에 1~5일이 더 소요될 수 있습니다.
천재지변, 설 및 추석 명절기간 등 택배물량이 증가하는 시기에는 2일~5일정도 배송이
지연될 수 있으니 참고 바랍니다.
★ 상품 수령 후 확인사항 안내
- 제품 수령 후 상품 개봉 전, 주문 내역과 배송된 상품이 맞는지 확인하시기 바랍니다.
- 제품 수령 후 주문 내역과 배송 상품이 상이한 경우 제품을 개봉하지 마시고 수령하신 그대로
택배박스(송장 포함)와 함께 보관하시고 즉시 판매자에게 연락 또는 문의주시기 바랍니다.
[판매자와 연락 전에 제품을 개봉하시거나 택배박스(송장포함)를 폐기하시면 처리가 지연되거나
거부될 수 있습니다]
★ 반품 및 교환 안내
1. 반품 및 교환이 가능한 경우
상품 수령 후 개봉하지 않으신 경우에 한해서, 수령일로부터 7일 이내에 교환 및 반품이 가능합니다.
- 상품 불량이나 파손 등 하자에 의한 교환 또는 반품 비용은 판매자가 부담합니다.
고객 변심 또는 고객 착오로 인한 교환 또는 반품 비용은 고객님께서 부담하셔야 합니다.
(왕복배송료 5,000원)
-반품 또는 교환시 제품이 손상되지 않도록 필히 택배박스에 담아 완충해 주시기 바랍니다.
(제품의 외부 지함케이스가 훼손되지 않도록 주의바랍니다)
- 진료 확인서 및 소견서 등의 증빙이 필요한 경우 제반비용 고객부담
2. 반품 및 교환, 환불이 불가능한 경우
제품의 특성상 개봉 또는 구성품의 누락, 상품가치가 상실된 경우
(제품의 외부 지함케이스도 중요한 제품의 구성품이므로 외부 지함케이스를
훼손한 경우도 포함됨)
상품을 사용하거나 일부 소비에 의하여 상품가치가 현저히 감소한 경우
- 시간의 경과에 의하여 재판매가 곤란할 정도로 상품가치가 현저히 감소한 경우




"""

answer = ask_gpt(user_input, ocr_data)
print(answer)

if not answer:  # 만약 답변이 없다면
    answer = "원하는 정보를 찾을 수 없습니다."

# print("answer",answer)
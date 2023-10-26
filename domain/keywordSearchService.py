from rank_bm25 import BM25Okapi
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from crud import fetch_content_from_db
from domain.koNLPyService import get_konlpy_text
from domain.prompt import ask_gpt
import re

def search_keyword(question, siteURL: str):
    texts = fetch_content_from_db(siteURL)
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', ' '.join(texts))

    #형태소 분석기
    answer_sorted = get_konlpy_text(sentences)
    answer_sorted_q = get_konlpy_text(question)
    
    # print("====answer_sorted=====", answer_sorted)
    # print("====answer_sorted_q=====", answer_sorted_q)

    bm25 = BM25Okapi(answer_sorted) # bm25 인스턴스

    # print("====파싱된 문서의 길이====",bm25.doc_len) #doc_len : 파싱된 문서의 길이
    # print("====inverse term 빈도수====",bm25.doc_freqs) #freqs: 문서에 있는 각각의 토큰의 빈도 (각 문서 내에서 딕셔너리 형태로 저장)
    # print("====inverse term 빈도수====",bm25.idf) # idf: 토큰의 inverse term frequency를 계산해둠
    doc_scores = bm25.get_scores(answer_sorted_q[0]) #점수반환
    print("====점수====",doc_scores)

    #상위 답변 반환
    answers = bm25.get_top_n(answer_sorted_q[0], answer_sorted, n=10)
    #답변 문장화
    answer_str = [' '.join(sublist) for sublist in answers]

    #gpt 검색
    # answer_gpt = ask_gpt(question, answer_str)
    
    return answer_str
from rank_bm25 import BM25Okapi
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from domain.koNLPyService import get_konlpy_text
from prompt import ask_gpt

def search_keyword(question, file_path):
    
    with open(file_path, 'r', encoding='utf-8') as file:
        texts = file.read().split('\n')
    #형태소 분석기
    answer_sorted = get_konlpy_text(texts)
    answer_sorted_q = get_konlpy_text(question)
    
    print(answer_sorted)
    print(answer_sorted_q)

    bm25 = BM25Okapi(answer_sorted) # bm25 인스턴스

    print("====파싱된 문서의 길이====",bm25.doc_len) #doc_len : 파싱된 문서의 길이
    # print("====inverse term 빈도수====",bm25.doc_freqs) #freqs: 문서에 있는 각각의 토큰의 빈도 (각 문서 내에서 딕셔너리 형태로 저장)
    # print("====inverse term 빈도수====",bm25.idf) # idf: 토큰의 inverse term frequency를 계산해둠
    doc_scores = bm25.get_scores(question) #점수반환
    print("====점수====",doc_scores)
    answer = bm25.get_top_n(question, texts, n=3) #get_top_n: 점수에 따른 상위 n개의 문서를 바로 리턴
    answer_str = ' '.join(answer)

    #gpt 검색
    answer_gpt = ask_gpt(question, answer_str)
    
    return answer_gpt
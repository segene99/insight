from rank_bm25 import BM25Okapi
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from crud import fetch_content_from_db
from domain.koNLPyService import get_konlpy_text
from domain.prompt import ask_gpt
import re


# Function to tokenize text using your tokenizer (e.g., konlpy)
def tokenize(text):
    return get_konlpy_text(text)

# Function to fetch and tokenize documents
def fetch_and_tokenize_documents(siteURL):
    texts = fetch_content_from_db(siteURL)
    # Tokenize each document
    documents = [tokenize(text) for text in texts.split(". ")]
    return documents


async def search_keyword(question, siteURL: str):
    # Fetch and tokenize documents
    tokenized_documents = fetch_and_tokenize_documents(siteURL)

    # Initialize BM25 with tokenized documents
    bm25 = BM25Okapi(tokenized_documents)

    # Tokenize query in the same way as documents
    tokenized_query = tokenize(question)

    # Get scores for the query
    doc_scores = bm25.get_scores(tokenized_query)
    print("======score=======", doc_scores)
    
    # Get top N documents
    top_n_documents = bm25.get_top_n(tokenized_query, tokenized_documents, n=10)

    # Join tokens to form strings for each top document
    top_n_documents_str = [" ".join(doc) for doc in top_n_documents]
    return top_n_documents_str


'''
    texts = fetch_content_from_db(siteURL)
    documents_list = texts.split(". ")  # Splitting by period and space, assuming this is your document delimiter
    tokenized_documents = [doc.split() for doc in documents_list]
    print("====tokenized_documents=====", tokenized_documents)

    #형태소 분석기
    answer_sorted = get_konlpy_text(texts)
    answer_sorted_q = get_konlpy_text(question)
    
    # print("====answer_sorted=====", answer_sorted)
    print("====answer_sorted_q=====", answer_sorted_q)

    bm25 = BM25Okapi(answer_sorted) # bm25 인스턴스

    # print("====파싱된 문서의 길이====",bm25.doc_len) #doc_len : 파싱된 문서의 길이
    # print("====inverse term 빈도수====",bm25.doc_freqs) #freqs: 문서에 있는 각각의 토큰의 빈도 (각 문서 내에서 딕셔너리 형태로 저장)
    # print("====inverse term 빈도수====",bm25.idf) # idf: 토큰의 inverse term frequency를 계산해둠
    doc_scores = bm25.get_scores(answer_sorted_q) #점수반환
    print("====점수====",doc_scores)

    #상위 답변 반환
    # 데이터타입
    # documents = [
    # ["the", "cat", "sat", "on", "the", "mat"],
    # ["dog", "barks", "at", "night"],
    # ["the", "tree", "is", "tall"]
    # ]
    answers = bm25.get_top_n(answer_sorted_q, tokenized_documents, n=3)
    print("====bm25 answers====",answers)
    #답변 문장화
    answer_str = [' '.join(sublist) for sublist in answers]

    #gpt 검색
    # answer_gpt = ask_gpt(question, answer_str)
    
    return answer_str
'''
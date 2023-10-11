from rank_bm25 import BM25Okapi
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def tokenizer(sent):
    print("======타입=====", type(sent))
    print("======텍스트=====", sent)
    return sent.text.split(" ")


def search_keyword(question, file_path):
    
    with open('file_path', 'r', encoding='utf-8') as file:
        texts = file.read()

    tokenized_corpus = [tokenizer(doc) for doc in texts]

    bm25 = BM25Okapi(tokenized_corpus) # bm25 인스턴스

    print("====파싱된 문서의 길이====",bm25.doc_len) #doc_len : 파싱된 문서의 길이
    print("====inverse term 빈도수====",bm25.doc_freqs) #freqs: 문서에 있는 각각의 토큰의 빈도 (각 문서 내에서 딕셔너리 형태로 저장)
    print("====inverse term 빈도수====",bm25.idf) # idf: 토큰의 inverse term frequency를 계산해둠

    tokenized_query = tokenizer(question) #토큰화
    print("====토큰화된 질문====",tokenized_query)

    doc_scores = bm25.get_scores(tokenized_query) #점수반환
    print("====점수====",doc_scores)
    answer = bm25.get_top_n(tokenized_query, texts, n=1) #get_top_n: 점수에 따른 상위 n개의 문서를 바로 리턴

    return answer
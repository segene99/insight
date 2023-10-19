# import os
# import traceback
# from chromadb.utils import embedding_functions
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
# from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
# from langchain.vectorstores import Chroma
# import openai
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.chains import ConversationalRetrievalChain
# from langchain.chains import ConversationalRetrievalChain
# from langchain.llms import OpenAI
# from langchain.document_loaders import TextLoader
# from langchain.document_loaders import PyPDFLoader
# from langchain.indexes import VectorstoreIndexCreator
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.vectorstores import Chroma
# from langchain.chains import RetrievalQA
# from langchain.memory import ConversationBufferMemory
# from langchain.chat_models import ChatOpenAI
# from sentence_transformers import SentenceTransformer, util
# from rank_bm25 import BM25Okapi
# from langchain.document_loaders import TextLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.prompts import PromptTemplate



# # 키받는곳: https://platform.openai.com/account/
# # keys.txt 파일에서 API 키들을 읽어오는 함수
# def read_keys_from_file(filename):
#     with open(filename, 'r') as f:
#         lines = f.readlines()
#         openai_key = lines[0].strip().split('=')[1].replace('"', '')
#     return openai_key

# # keys.txt path
# keys_txt_path = 'key/keys.txt'

# # keys.txt 파일에서 API 키들을 가져옴
# openai_key_value = read_keys_from_file(keys_txt_path)

# # 가져온 키를 변수에 대입
# openai.api_key = openai_key_value
# os.environ["OPENAI_API_KEY"] = openai.api_key

# # hugginface tokenizer 병렬처리 해제
# os.environ["TOKENIZERS_PARALLELISM"] = "false"

# file_path = os.path.join('detected_texts', 'all_detected_texts.txt')

# def tokenizer(sent):
#     return sent.split(" ")

# def search_documents(question, documents_path=file_path):    
#     try:  
#     # Load the documents and split them into chunks
#         loader = TextLoader(documents_path)
#         documents = loader.load()

#     # split documents
#         text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
#         texts = text_splitter.split_documents(documents)

#     # define embedding
#         # embeddings = OpenAIEmbeddings()
#         # paraphrase-multilingual-mpnet-base-v2
#         embedding_function = SentenceTransformerEmbeddings(model_name="paraphrase-multilingual-mpnet-base-v2")

#     # create vector database from data
#         # vector_db = Chroma.from_documents(texts, embeddings)
#         vector_db = Chroma.from_documents(texts, embedding_function)
#         # vector_db = Chroma.from_texts(answer, embedding_function)

#     # define retriever
#         # similarity search
#         # docs_mmr = vector_db.max_marginal_relevance_search(question,k=3)        
#         # docs = vector_db.similarity_search(question,k=3)
#         # print("++++++++++++", docs)
#         # answer = docs[0].page_content

#     # Check if docs is non-empty
#         # if not docs:
#         #     print("No documents found for similarity search.")
#         #     return None

#     # expose this index in a retriever interface
#         vector_retriever = vector_db.as_retriever(search_type="similarity", search_kwargs={"k":3})

#     # chathistory memory 
#         memory = ConversationBufferMemory(
#             memory_key="chat_history",
#             return_messages=True
#         )

#     #프롬프트
#         template = (
#             "당신은 친절한 쇼핑 도우미입니다. 주어진 텍스트 안의 정보만을 기반으로 질문에 반드시 한글로 답하십시오."
#             "다른 외부 정보나 지식은 참조하지 마십시오.영어로 된 모든 질문에도 한글로만 대답해 주세요."

#         )
#         prompt = PromptTemplate.from_template(template)


#     # 대화형 retrieval chain
#         qa = ConversationalRetrievalChain.from_llm(
#             llm=ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0.1),          
#             chain_type="stuff", 
#             retriever=vector_retriever,
#             memory=memory,
#             # return_source_documents=True,
#             # return_generated_question=True,
#         )
        
#         result = qa({"question": question})

#         return result

#     except IndexError as ie:
#         print("IndexError occurred:", str(ie))
#         traceback.print_exc()
    
#     except Exception as e:
#         print("An unexpected error occurred:", str(e))
#         traceback.print_exc()
#         print(f"Error: {str(e)}")
#         # Optionally, log or handle the error further

# '''
# def search_documents(question, documents_path=file_path):    
#     try:  
#         # Load the documents and split them into chunks
#         loader = TextLoader(documents_path)
#         documents = loader.load()
#         # print("@@@@@@@@@@@@@@@@@@@@", documents)

#     # split documents
#         text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
#         texts = text_splitter.split_documents(documents)
#         # print("*************", texts)
#         # page_content = texts[0].page_content

#     # define embedding
#         # openai
#         # embeddings = OpenAIEmbeddings()
#         # paraphrase-multilingual-mpnet-base-v2
#         embedding_function = SentenceTransformerEmbeddings(model_name="paraphrase-multilingual-mpnet-base-v2")

#     # create vector database from data
#         # vector_db = Chroma.from_documents(texts, embeddings)
#         vector_db = Chroma.from_documents(texts, embedding_function)

#     # define retriever
#     # similarity search
#         # docs_mmr = vector_db.max_marginal_relevance_search(question,k=3)        
#         # docs = vector_db.similarity_search(question,k=3)
#         # print("++++++++++++", docs)
#         # answer = docs[0].page_content

#     # Check if docs is non-empty
#         # if not docs:
#         #     print("No documents found for similarity search.")
#         #     return None

#     # expose this index in a retriever interface
#         vector_retriever = vector_db.as_retriever(search_type="similarity", search_kwargs={"k":3})

#    # chathistory memory 
#         memory = ConversationBufferMemory(
#             memory_key="chat_history",
#             return_messages=True
#         )

#     # 대화형 retrieval chain
#         qa = ConversationalRetrievalChain.from_llm(
#             llm=ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0.1), 
#             chain_type="stuff", 
#             retriever=vector_retriever,
#             memory=memory,
#             # return_source_documents=True,
#             # return_generated_question=True,
#         )
#         result = qa({"question": question})

#         return result

#     except IndexError as ie:
#         print("IndexError occurred:", str(ie))
#         traceback.print_exc()
    
#     except Exception as e:
#         print("An unexpected error occurred:", str(e))
#         traceback.print_exc()
#         print(f"Error: {str(e)}")
#         # Optionally, log or handle the error further
# '''
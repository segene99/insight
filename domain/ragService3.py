import os
from langchain.document_loaders import WebBaseLoader
import traceback
from chromadb.utils import embedding_functions
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
import openai
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from sentence_transformers import SentenceTransformer, util
from rank_bm25 import BM25Okapi
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain import hub
from langchain.schema.runnable import RunnablePassthrough

from crud import fetch_content_from_db
from models import Document

# 키받는곳: https://platform.openai.com/account/
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
os.environ["OPENAI_API_KEY"] = openai.api_key

# hugginface tokenizer 병렬처리 해제
os.environ["TOKENIZERS_PARALLELISM"] = "false"

file_path = os.path.join('detected_texts', 'all_detected_texts.txt')

def tokenizer(sent):
    return sent.split(" ")

async def search_documents(question, siteURL= str):    
    try: 
    # Load the documents
        context = fetch_content_from_db(siteURL) 
        documents = [Document(page_content=context)]
    # Split documents
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 100)
        splits = text_splitter.split_documents(documents)
    # Embed and store splits
        embedding_function = SentenceTransformerEmbeddings(model_name="paraphrase-multilingual-mpnet-base-v2")
        vectorstore = Chroma.from_documents(documents=splits,embedding=embedding_function)
        result = vectorstore.similarity_search(question, k=5)
        # retriever = vectorstore.as_retriever()
    # LLM
        # llm = ChatOpenAI(model_name="gpt-4", temperature=0.1)
    # Prompt 
        template = """
              "You are a kind shopping helper.\n"
              "Be sure to answer the questions in Korean and honorifics based only on the information in the given text. "
              "Don't answer questions you don't know."
              "Do not refer to any other external information or knowledge. Please answer all questions in English in Korean."
              "Please respond as politely and kindly as possible to the user"
              "질문내용에서 '이게'는 '이거'의 의미로 사용됩니다. '이게'를 '이거'로 해석하고 답변해주세요(단 '이 게'일때는 적용하지 마시오). "
              "중복되는 정보가 있으면 모두 알려주세요 ..
            {context}
            Question: {question}
            Helpful Answer:
        """
        rag_prompt_custom = PromptTemplate.from_template(template)

        # rag_chain = (
        #     {"context": retriever, "question": RunnablePassthrough()} 
        #     | rag_prompt_custom 
        #     | llm 
        # )

        # result = rag_chain.invoke(question)

        return result
    
    #반환데이터 형태
    # AIMessage(content='something something')

    except IndexError as ie:
        print("IndexError occurred:", str(ie))
        traceback.print_exc()
    
    except Exception as e:
        print("An unexpected error occurred:", str(e))
        traceback.print_exc()
        print(f"Error: {str(e)}")
        # Optionally, log or handle the error further



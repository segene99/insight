import os
import traceback
from chromadb.utils import embedding_functions
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
import openai
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from sentence_transformers import SentenceTransformer, util
from operator import itemgetter
from langchain.memory import ConversationBufferMemory
from langchain.schema.runnable import RunnableMap
from langchain.schema import format_document
from operator import itemgetter
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.vectorstores import FAISS


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
os.environ["TOKENIZERS_PARALLELISM"] = "True"

memory = ConversationBufferMemory(return_messages=True, output_key="answer", input_key="question")

file_path = os.path.join('detected_texts', 'all_detected_texts.txt')

def search_documents(question, documents_path=file_path): 
    # Load the documents and split them into chunks
    loader = TextLoader(documents_path)
    print("========1=========")

    documents = loader.load()  

    print("========2=========")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    print("========3=========")
    
    texts = text_splitter.split_documents(documents)
    print("========4=========")

    vectorstore = FAISS.from_documents(texts, embedding=OpenAIEmbeddings())
    print("========5=========")
    
    
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k":3})
    print("========6=========")
    
    template = """
    아래 내용을 바탕으로 질문에 대답해줘:
    {context}

    질문: {question}

    대답언어는 이걸로 해줘: 한국어
    """
    prompt = ChatPromptTemplate.from_template(template)
    print("========7=========")

    model = ChatOpenAI()
    print("========8=========")

    chain = {
    "context": retriever, 
    "question": question, 
    } | prompt | model | StrOutputParser()
    
    print("========", type(retriever))
    print(")))))))))",type(prompt))
    print("^^^^^^^^^",type(model))
    print("@@@@@@@@@",type(StrOutputParser()))

    print("========9=========")

    try:
    # Code that may raise an exception
        return chain.invoke()
    except Exception as e:
        print("An error occurred:", str(e))
        traceback.print_exc()

import os
import traceback
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


def search_documents(question, documents_path="/Users/segene/insight/detected_texts/all_detected_texts.txt"):    
    try:  
        # Load the documents and split them into chunks
        loader = TextLoader(documents_path)
        documents = loader.load()
        
        print("@@@@@@@@@@@@@@@@@@@@", documents)

        # split documents
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        texts = text_splitter.split_documents(documents)

        
        # define embedding
        embeddings = OpenAIEmbeddings()

        # create vector database from data
        vector_db = Chroma.from_documents(texts, embeddings)

        # select which embeddings we want to use
        embeddings = OpenAIEmbeddings()


        # expose this index in a retriever interface
        retriever = vector_db.as_retriever(search_type="similarity", search_kwargs={"k":3})

        # define retriever
        # similarity search
        docs = vector_db.similarity_search(question,k=3)
        
        # Check if docs is non-empty
        if not docs:
            print("No documents found for similarity search.")
            return None


        # chathistory memory 
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        # 대화형 retrieval chain
        qa = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0), 
            chain_type="stuff", 
            retriever=retriever,
            memory=memory,
            # return_source_documents=True,
            # return_generated_question=True,
        )

        result = qa({"question": question})

        print("********************", result)


        return result

    except IndexError as ie:
        print("IndexError occurred:", str(ie))
        traceback.print_exc()
    
    except Exception as e:
        print("An unexpected error occurred:", str(e))
        traceback.print_exc()
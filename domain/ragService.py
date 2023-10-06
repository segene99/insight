import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
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

class CustomTextLoader:
    def __init__(self, directory_path):
        self.directory_path = directory_path

    def load(self):
        txt_files = [f for f in os.listdir(self.directory_path) if f.endswith('.txt')]
        documents = []
        for file_name in txt_files:
            file_path = os.path.join(self.directory_path, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                documents.append({
                    'page_content': text,
                    'url': file_path
                })
        return documents


def search_documents(query, documents_path="detected_texts"):    
    # Load the documents and split them into chunks
    loader = CustomTextLoader(documents_path)
    documents = loader.load()
    
    # split the documents into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    # select which embeddings we want to use
    embeddings = OpenAIEmbeddings()

    # create the vectorestore to use as the index
    db = Chroma.from_documents(texts, embeddings)

    # expose this index in a retriever interface
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k":3})

    # create a chain to answer questions 
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(), chain_type="map_reduce", retriever=retriever, return_source_documents=True)
    result = qa({"query": query})
    print(result['result'])
    return result
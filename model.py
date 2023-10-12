from typing import List
from pydantic import BaseModel
from langchain.memory import ConversationBufferMemory

class ImageURL(BaseModel):
    url: str

class ImageList(BaseModel):
    imageUrls: List[ImageURL]
    

class Turn(BaseModel):
    role: str
    content: str

class Messages(BaseModel):
    messages: List[Turn]  
    # [{"role": "user", "content": "blahblahblah"}, {"role": "assistant", "content": "blahblahblah"}, ...]

class TextRequest(BaseModel):
    text: str

from typing import List
from pydantic import BaseModel
from langchain.memory import ConversationBufferMemory
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    subject = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)

class ImageURL(BaseModel):
    url: str

class ImageList(BaseModel):
    imageUrls: List[ImageURL]
    productTexts : str
    siteUrls: str

class Turn(BaseModel):
    role: str
    content: str

class Messages(BaseModel):
    messages: List[Turn]  
    siteUrls: str
    # [{"role": "user", "content": "blahblahblah"}, {"role": "assistant", "content": "blahblahblah"}, ...]

class TextRequest(BaseModel):
    user: str
    assistant : str

class AudioConfig(BaseModel):
    volume: float
    speed: float

class Document:
    def __init__(self, page_content: str, metadata: dict = None):
        self.page_content = page_content
        self.metadata = metadata or {}
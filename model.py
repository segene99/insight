from typing import List
from pydantic import BaseModel

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



from pydantic import BaseModel
from typing import List, Optional
from beanie import Document
from pydantic import Field
from beanie import PydanticObjectId


class User(Document):
    name: str
    password: str
    tg_id: Optional[str]
    
    class Settings:
        name = "users"
    
    class Config:
        scheme_extra = {
            "example": {
            'name': 'Anastasia',
            'password': '0000',
            'tg_id': '5365634'
            }
        }
        

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

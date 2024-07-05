from typing import Optional
from pydantic import BaseModel


class Cotization(BaseModel):
    position: str
    technology: str
    english_level: str
    years_experience: list[int]
    city: str = Optional[None]
    country: str = Optional[None]
    
    
    

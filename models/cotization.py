from pydantic import BaseModel


class Cotization(BaseModel):
    position: str
    technology: str
    english_level: str
    years_experience: int
    city: str
    country: str
    
    
    

from pydantic import BaseModel


class Cotization(BaseModel):
    position: str
    technology: str
    city: str
    country: str
    english_level: str
    years_experience: int
    

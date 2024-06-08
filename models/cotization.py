from pydantic import BaseModel


class Cotization(BaseModel):
    position: str
    technology: str
    ubication: str
    english_level: str
    years_experience: int
    

from pydantic import BaseModel

class BookRequest(BaseModel):
    title: str
    author: str
    isbn: str
    quantity: int
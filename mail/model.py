from pydantic import BaseModel

class Email(BaseModel):
    sender: str
    name: str
    subject: str
    content: str
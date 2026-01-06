from pydantic import BaseModel

class DocumentCreate(BaseModel):
    file_name: str
    file_path: str

class Document(DocumentCreate):
    collection_id: str
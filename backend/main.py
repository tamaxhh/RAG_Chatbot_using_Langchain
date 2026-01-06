from fastapi import FastAPI, UploadFile, File, Depends
from backend.config import settings
from backend.database import engine, Base
from backend.ingestion import document_loader, preprocessor
from backend.rag import embeddings, retriever, qa_chain
from backend.models.document import DocumentCreate, Document
from backend.models.chat import Query
from sqlalchemy.orm import Session
from backend.database import get_db
import shutil
import os

app = FastAPI()

# Create DB tables
Base.metadata.create_all(bind=engine)

@app.post("/ingest")
def ingest_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Save uploaded file temporarily
    file_path = f"data/uploads/{file.filename}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    text = document_loader.load_document(file_path)
    chunks = preprocessor.preprocess(text)
    collection_id = embeddings.generate_and_store(chunks, file.filename)
    # Store metadata in DB
    db_doc = Document(file_name=file.filename, file_path=file_path, collection_id=collection_id)
    db.add(db_doc)
    db.commit()
    return {"status": "ingested", "collection_id": collection_id}

@app.post("/query")
def query_rag(query: Query, db: Session = Depends(get_db)):
    # Assume single document for simplicity; extend for multi-doc
    doc = db.query(Document).first()
    if not doc:
        return {"error": "No documents ingested"}
    docs = retriever.retrieve(query.question, doc.collection_id)
    answer = qa_chain.answer(query.question, docs)
    return {"answer": answer}
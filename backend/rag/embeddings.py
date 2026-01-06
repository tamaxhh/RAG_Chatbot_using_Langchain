from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from backend.config import settings
import uuid

embeddings_model = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)

def generate_and_store(chunks: list[str], file_name: str) -> str:
    collection_id = str(uuid.uuid4())
    vectorstore = Chroma(
        collection_name=collection_id,
        embedding_function=embeddings_model,
        persist_directory=settings.chroma_path
    )
    vectorstore.add_texts(chunks)
    vectorstore.persist()
    return collection_id
from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from backend.config import settings

def retrieve(query: str, collection_id: str) -> list:
    embeddings_model = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
    vectorstore = Chroma(
        collection_name=collection_id,
        embedding_function=embeddings_model,
        persist_directory=settings.chroma_path
    )
    return vectorstore.similarity_search(query, k=5)
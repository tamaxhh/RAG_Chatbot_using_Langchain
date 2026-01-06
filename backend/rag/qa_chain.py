from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from backend.config import settings

llm = OpenAI(openai_api_key=settings.openai_api_key)

prompt_template = PromptTemplate(
    input_variables=["question", "context"],
    template="Answer {question} based on: {context}"
)

def answer(question: str, docs: list) -> str:
    context = "\n".join([doc.page_content for doc in docs])
    # Simplified; integrate retriever properly in production
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=None)
    return chain.run({"query": question, "context": context})  # Adjust for actual chain
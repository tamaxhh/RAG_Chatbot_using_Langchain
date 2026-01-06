def preprocess(text: str) -> list[str]:
    # Simple chunking by paragraphs; use NLTK/SpaCy for better.
    chunks = text.split("\n\n")
    return [chunk.strip() for chunk in chunks if chunk.strip()]
import os
from dotenv import load_dotenv
import numpy as np
import google.generativeai as genai
import json

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

for m in genai.list_models():
    if "embedContent" in m.supported_generation_methods:
        print(m.name)

# --- Helper functions ---


def get_embedding(text):
    response = genai.embed_content(
        model="models/gemini-embedding-2-preview",
        content=text,
        task_type="retrieval_document"
    )
    return response["embedding"]


def cosine(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def chunk_text(text, size=800, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = min(start + size, len(text))

        if end < len(text):
            while end > start and text[end] != " ":
                end -= 1

        chunks.append(text[start:end].strip())

        # Stop if we've reached the end
        if end == len(text):
            break

        start = max(end - overlap, start + 1)

    return chunks


# --- Step 1: Similarity demo ---
sentences = [
    "How do I reset my password?",
    "Steps to recover a forgotten password",
    "Our office is closed on Friday",
]

print("=== Embedding Similarity ===")
embs = [get_embedding(s) for s in sentences]

score_similar = cosine(embs[0], embs[1])
score_unrelated = cosine(embs[0], embs[2])

print(f"Query:     '{sentences[0]}'")
print(f"Similar:   '{sentences[1]}'  → score: {score_similar:.4f}")
print(f"Unrelated: '{sentences[2]}'  → score: {score_unrelated:.4f}")
print()

with open("document.txt", "r", encoding="utf-8") as f:
    document = f.read()

print("=== Chunking ===")
chunks = chunk_text(document, size=300, overlap=50)
print(f"Total chunks: {len(chunks)}\n")
print(f"Chunk 1:\n{chunks[0]}\n")
print(f"Chunk 2:\n{chunks[1]}\n")


# # --- Step 3: Full mini RAG loop ---
print("=== Mini RAG: Retrieve + Augment ===")

chunk_embeddings = [get_embedding(c) for c in chunks]

data = []

for i, (chunk, embedding) in enumerate(zip(chunks, chunk_embeddings)):
    data.append({
        "id": i + 1,
        "text": chunk,
        "embedding": embedding
    })

with open("embeddings.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("Embeddings saved to embeddings.json")

question = "when the office is closed?"
question_embedding = get_embedding(question)

scores = [cosine(question_embedding, ce) for ce in chunk_embeddings]

top3 = np.argsort(scores)[-3:][::-1]

print("\nTop 3 Matching Chunks:\n")

for rank, idx in enumerate(top3, start=1):
    print(f"Rank {rank}")
    print(f"Score: {scores[idx]:.4f}")
    print(chunks[idx])
    print("-" * 50)

best_idx = top3[0]
best_chunk = chunks[best_idx]


best_chunk = chunks[top3[0]]

print(f"Question: {question}")
print(f"Best matching chunk (score: {scores[best_idx]:.4f}):\n{best_chunk}\n")

augmented_prompt = f"""Use only the context below to answer the question.
 
Context:
{best_chunk}
 
Question: {question}
"""

model = genai.GenerativeModel("models/gemini-2.5-flash")
response = model.generate_content(augmented_prompt)

print("Answer from LLM:")
print(response.text)

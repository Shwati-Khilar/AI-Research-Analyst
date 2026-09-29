import ollama
import math


def get_embedding(text):
    response = ollama.embed(
        model="nomic-embed-text",
        input=text
    )

    return response["embeddings"][0]


def cosine_similarity(vector_a, vector_b):
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))

    magnitude_a = math.sqrt(sum(a * a for a in vector_a))
    magnitude_b = math.sqrt(sum(b * b for b in vector_b))

    return dot_product / (magnitude_a * magnitude_b)


text1 = "Generative AI helps software developers write code."

text2 = "AI can assist programmers with software development."

text3 = "The weather is sunny and warm today."


embedding1 = get_embedding(text1)
embedding2 = get_embedding(text2)
embedding3 = get_embedding(text3)


similarity_12 = cosine_similarity(embedding1, embedding2)
similarity_13 = cosine_similarity(embedding1, embedding3)


print("Similarity between text 1 and text 2:")
print(similarity_12)

print("\nSimilarity between text 1 and text 3:")
print(similarity_13)
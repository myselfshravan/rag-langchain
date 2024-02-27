from langchain.embeddings import OpenAIEmbeddings
from langchain.evaluation import load_evaluator

from config import openai_api_key


def main():
    # Get embedding for a word.
    embedding_function = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vector = embedding_function.embed_query("apple")
    print(f"Vector for 'apple': {vector}")
    print(f"Vector length: {len(vector)}")

    # Compare vector of two words
    evaluator = load_evaluator("pairwise_embedding_distance")
    words = ("apple", "iphone")
    x = evaluator.evaluate_string_pairs(prediction=words[0], prediction_b=words[1])
    print(f"Comparing ({words[0]}, {words[1]}): {x}")


if __name__ == "__main__":
    main()

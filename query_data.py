from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.vectorstores.chroma import Chroma

from config import openai_api_key

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context given to you:
---
{context}
---

Answer the question " {question} " based on the above context. 
Note: If you are unable to answer the question, please type "I don't know".
"""


def main():
    prompt_input = input("Enter a prompt: ")

    query_text = prompt_input

    # Prepare the DB.
    embedding_function = OpenAIEmbeddings(openai_api_key=openai_api_key)
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text, k=2)
    if len(results) == 0 or results[0][1] < 0.7:
        print(f"Unable to find matching results.")
        return

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    print(f"Context: {context_text}")
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(f"\nThe prompt: {prompt}\n\n")

    model = ChatOpenAI(
        openai_api_key=openai_api_key,
        temperature=0.7,
        max_tokens=100
    )
    response_text = model.predict(prompt)

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\n\nSources: {sources}"
    print(formatted_response)


if __name__ == "__main__":
    main()

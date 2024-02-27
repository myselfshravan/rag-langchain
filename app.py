import chainlit as cl
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
import openai

from config import openai_api_key, ANY_SCALE_API

client = openai.OpenAI(
    base_url="https://api.endpoints.anyscale.com/v1",
    api_key=ANY_SCALE_API
)

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context given to you:
---
{context}
---

Answer the question " {question} " based on the above context. 
Note: If you are unable to answer the question, please type "I don't know".
"""

SYSTEM_PROMPT = "You are an helpful NLP assistant and will Answer based only on the context given and you."


def get_response(results, system_content, prompt):
    chat_completion = client.chat.completions.create(
        model="meta-llama/Llama-2-70b-chat-hf",
        messages=[{"role": "system", "content": system_content},
                  {"role": "user", "content": prompt}],
        temperature=0.7
    )
    response = chat_completion.choices[0].message.content
    return response


@cl.on_chat_start
def on_chat_start():
    print("A new chat session has started!")


@cl.on_message
async def on_message(message: cl.Message):
    prompt_input = message.content

    embedding_function = OpenAIEmbeddings(openai_api_key=openai_api_key)
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    results = db.similarity_search_with_relevance_scores(prompt_input, k=3)
    if len(results) == 0 or results[0][1] < 0.5:
        await cl.Message(content="Unable to find matching results.").send()
        return

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=prompt_input)
    # model = ChatOpenAI(
    #     model="gpt-3.5-turbo",
    #     openai_api_key=openai_api_key,
    #     temperature=0.6,
    #     max_tokens=512
    # )
    # response = model.invoke(prompt)
    # response_text = response.content
    response_text = get_response(results, SYSTEM_PROMPT, prompt)
    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"{response_text}\n\n{sources}"
    await cl.Message(content=formatted_response).send()


@cl.on_stop
def on_stop():
    print("The user wants to stop the task!")


@cl.on_chat_end
def on_chat_end():
    print("The user disconnected!")

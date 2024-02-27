# from langchain.chat_models import ChatOpenAI
# from langchain.embeddings import OpenAIEmbeddings
import openai

from config import ANY_SCALE_API

client = openai.OpenAI(
    base_url="https://api.endpoints.anyscale.com/v1",
    api_key=ANY_SCALE_API
)


def main():
    prompt = "this is a test"

    chat_completion = client.chat.completions.create(
        model="meta-llama/Llama-2-7b-chat-hf",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}],
        temperature=0.7
    )

    print(chat_completion.choices[0].message.content)


if __name__ == '__main__':
    main()

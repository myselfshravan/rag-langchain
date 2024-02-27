from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser


def read_properties_file(file_path):
    gemini_api_key = "AIzaSyCSaQMsiZGyeDp4RboAiE5q-WptxX6P_j4"
    return gemini_api_key


def get_property():
    file_path = 'config.properties'
    try:
        gemini_api_key = read_properties_file(file_path)
        print("Gemini API Key", gemini_api_key)
        return gemini_api_key
    except FileNotFoundError as e:
        print(e)
        raise e


def get_llm(gemini_api_key):
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=gemini_api_key,
                                 convert_system_message_to_human=True, temperature=0.0)
    return llm


def create_conversational_chain():
    try:
        gemini_api_key = get_property()

        # Get the instance of LLM
        llm = get_llm(gemini_api_key)

        output_parser = StrOutputParser()
        chain = llm | output_parser

    except Exception as e:
        raise e
    return chain

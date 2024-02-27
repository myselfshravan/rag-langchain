import os
import shutil

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader
from langchain_openai import OpenAIEmbeddings

from config import openai_api_key

CHROMA_PATH = "chroma"

TXT_DATA_PATH = "txt_files"
MD_DATA_PATH = "md_files"


def load_documents(file_type="txt"):
    if file_type == "md":
        loader = DirectoryLoader(MD_DATA_PATH, glob="*.md", show_progress=True)
    else:
        loader = DirectoryLoader(TXT_DATA_PATH, glob="*.txt", show_progress=True)
    docs = loader.load()
    return docs


def split_text(documents: list[Document]):
    custom_text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=300, separators=["\n"],
                                                          length_function=len)
    chunks = custom_text_splitter.split_documents(documents)
    print(f"Number of documents: {len(documents)}  into {len(chunks)} chunks")

    document = chunks[2]
    print(document.page_content)
    print(document.metadata)

    return chunks


def generate_data_store():
    documents = load_documents(file_type="md")
    chunks = split_text(documents)
    save_to_chroma(chunks)


def save_to_chroma(chunks: list[Document]):
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(openai_api_key=openai_api_key), persist_directory=CHROMA_PATH
    )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


def main():
    generate_data_store()


if __name__ == '__main__':
    main()

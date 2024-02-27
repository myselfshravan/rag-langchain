from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

loader = TextLoader("md_files/webcontent1.md", encoding="utf-8")
docs = loader.load()

custom_text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)

custom_text_splitter2 = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=30,
    length_function=len,
    separators=['\n']
)
custom_texts = custom_text_splitter.split_documents(docs)
custom_texts2 = custom_text_splitter2.split_documents(docs)

# Print the sampled chunks
print("====   Sample chunks from 'Standard Parameters':   ====\n\n")
for i, chunk in enumerate(custom_texts):
    if i < 4:
        print(f"### Chunk {i + 1}: \n{chunk.page_content}\n")

# print("====   Sample chunks from 'Custom Parameters':   ====\n\n")
# for i, chunk in enumerate(custom_texts2):
#     if i < 4:
#         print(f"### Chunk {i + 1}: \n{chunk.page_content}\n")

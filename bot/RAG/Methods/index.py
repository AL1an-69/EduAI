from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os
import shutil

load_dotenv()


DATA_PATH = "bot/methods"

def load_methods():
    loader = DirectoryLoader(DATA_PATH, glob="*.txt", loader_cls=TextLoader)
    return loader.load()

def split_methods(methods):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200, 
        chunk_overlap=500,
        separators=["\n"]
    )
    print(f"Загружено {len(methods)} методов. Начинаю разбиение на чанки...")
    chunks = text_splitter.split_documents(methods)
    print(f"Разбиение завершено. Получено {len(chunks)} чанков.")
    return chunks

CHROMA_PATH = os.path.join(os.path.dirname(__file__), "chroma_db")

def save_to_chroma(chunks):
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    db = Chroma.from_documents(
        chunks,
        OpenAIEmbeddings(api_key=os.getenv("CHATGPT_TOKEN")),
        persist_directory=CHROMA_PATH
    )
    print("Методы успешно сохранены в ChromaDB")



def main():
    methods = load_methods()
    chunks = split_methods(methods)
    save_to_chroma(chunks)



if __name__ == "__main__":
    main()  
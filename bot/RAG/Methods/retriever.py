from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

CHROMA_PATH = os.path.join(os.path.dirname(__file__), "chroma_db")


def get_relevant_method(query: str) -> str:
    try:
        db = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=OpenAIEmbeddings(
                model="text-embedding-3-small",
                api_key=os.getenv("CHATGPT_TOKEN")
            )
        )

        results = db.similarity_search(query, k=2)

        if not results:
            return ""

        for doc in results:
            source = doc.metadata.get("source", "unknown")
            print(f"[RAG] найдено: {source}")

        return "\n\n".join(doc.page_content for doc in results)

    except Exception as e:
        print(f"[RAG] ошибка: {e}")
        return ""

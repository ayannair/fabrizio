from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def test(index_path="faiss_index"):
    embedding = OpenAIEmbeddings(model="text-embedding-3-large")

    faiss_index = FAISS.load_local(index_path, embedding, allow_dangerous_deserialization=True)

    print(f"Total vectors stored: {faiss_index.index.ntotal}")

    vector_0 = faiss_index.index.reconstruct(0)
    print(f"Vector at index 0:\n{vector_0}\n")

    doc_ids = list(faiss_index.docstore._dict.keys())
    doc_0 = faiss_index.docstore._dict[doc_ids[0]]
    print(f"Document for vector 0:\n{doc_0}\n")

    query = "Chelsea"
    results = faiss_index.similarity_search(query, k=10)

    filtered = [doc for doc in results if "Chelsea" in doc.page_content or "Chelsea" in doc.metadata.get("keywords", [])]

    for i, doc in enumerate(filtered[:3], 1):
        print(f"Result {i}:\n{doc.page_content}\nMetadata: {doc.metadata}\n")

if __name__ == "__main__":
    test()
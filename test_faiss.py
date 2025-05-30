from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def test(index_path="faiss_index"):
    embedding = OpenAIEmbeddings(model="text-embedding-3-large")

    faiss_index = FAISS.load_local(index_path, embedding)

    print(f"Total vectors stored: {faiss_index.index.ntotal}")

    vector_0 = faiss_index.index.reconstruct(0)
    print(f"Vector at index 0:\n{vector_0}\n")

    doc_ids = list(faiss_index.docstore._dict.keys())
    doc_0 = faiss_index.docstore._dict[doc_ids[0]]
    print(f"Document for vector 0:\n{doc_0}\n")

    query = "Chelsea"
    results = faiss_index.similarity_search(query, k=3)

    print(f"Top 3 results for query: '{query}':\n")
    for i, doc in enumerate(results, 1):
        print(f"Result {i}:")
        print(f"Text: {doc.page_content}")
        print(f"Metadata: {doc.metadata}")
        print("-" * 40)

if __name__ == "__main__":
    test()
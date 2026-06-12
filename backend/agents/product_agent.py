import sys
from pathlib import Path

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

def product_agent(query):

    try:
        from rag.search import search_products
    except Exception as e:
        print(f"[SEARCH IMPORT ERROR] {e}")
        return "Product search unavailable."

    try:
        docs = search_products(query)
    except Exception as e:
        print(f"[SEARCH ERROR] {e}")
        return "Product search failed."

    retrieved_docs = []

    for doc in docs:
        try:
            retrieved_docs.append(doc.page_content)
        except Exception:
            retrieved_docs.append(str(doc))

    print(f"[RAG] Retrieved {len(retrieved_docs)} documents")

    context = "\n\n---\n\n".join(retrieved_docs)

    prompt = f"""
You are a product recommendation assistant.

Use ONLY the product information below.

Context:
{context}

Customer Query:
{query}

Recommend products based on the context.
"""

    from backend.services.llm import call_llm

    return call_llm(prompt)
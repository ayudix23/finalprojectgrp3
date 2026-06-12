from rag.search import search_products
from services.llm import call_llm

def product_agent(query):

    docs = search_products(query)

    context = "\n".join(docs)

    prompt = f"""
Use product data below.

{context}

Customer Query:
{query}
"""

    return call_llm(prompt)
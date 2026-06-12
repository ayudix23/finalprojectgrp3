import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

def order_agent(query):
    
    try:
        from rag.search import search_products
    except Exception:
        search_products = None

    docs = []
    if search_products:
        try:
            docs = search_products(query)
        except Exception:
            docs = []

    context = "\n\n---\n\n".join(docs) if docs else ""

    prompt = f"""
You are an AI Order Tracking Agent.

Order Data:
{context}

Rules:
- Answer only using the provided order data.
- Do not make up tracking numbers, dates, statuses, or delivery estimates.
- If information is missing, ask for the required details.
- Keep responses under 150 words.
- Be polite and professional.
- If no order data is available, request:
  • Order ID
  • Registered email
  • Product name

Customer Question:
{query}

Provide a helpful order tracking response.
"""

    from backend.services.llm import call_llm
    return call_llm(prompt)
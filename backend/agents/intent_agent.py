import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from backend.services.llm import call_llm

def detect_intent(user_query: str):

    prompt = f"""
Classify the customer query into ONE category only:

Categories:
- order_tracking
- refund
- product_recommendation
- complaint
- cancellation
- other

Return ONLY JSON:
{{"intent": "..."}}

Query:
{user_query}
"""

    response = call_llm(prompt)
    return response
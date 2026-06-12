from fastapi import FastAPI
from pydantic import BaseModel

from FinalProject.backend.agents.intent_agent import detect_intent
from FinalProject.backend.agents.order_agent import order_agent
from FinalProject.backend.agents.refund_agent import refund_agent
from FinalProject.backend.agents.product_agent import product_agent

app = FastAPI()

class Query(BaseModel):
    message: str


@app.post("/chat")
def chat(query: Query):

    intent_response = detect_intent(query.message)

    # crude parsing (we improve later)
    if "order_tracking" in intent_response:
        reply = order_agent(query.message)

    elif "refund" in intent_response:
        reply = refund_agent(query.message)

    elif "product_recommendation" in intent_response:
        reply = product_agent(query.message)

    else:
        reply = "Sorry, I couldn't understand your request."

    return {
        "intent": intent_response,
        "response": reply
    }
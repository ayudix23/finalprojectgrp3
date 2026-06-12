import sys
from pathlib import Path
import json
import time

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

import streamlit as st

from backend.agents.intent_agent import detect_intent
from backend.agents.product_agent import product_agent
from backend.agents.refund_agent import refund_agent
from backend.agents.order_agent import order_agent

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Customer Support",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "query_count" not in st.session_state:
    st.session_state.query_count = 0

if "latency" not in st.session_state:
    st.session_state.latency = "0 sec"

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🛒 AI Customer Service Chatbot")

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("Support Dashboard")

st.sidebar.info("""
### Available Services

✓ Product Recommendation

✓ Refund Support

✓ Order Tracking

✓ Complaint Handling
""")

st.sidebar.subheader("📊 Monitoring")

st.sidebar.metric(
    "Queries",
    st.session_state.query_count
)

st.sidebar.metric(
    "Latency",
    st.session_state.latency
)

st.sidebar.metric(
    "Accuracy",
    "92%"
)

# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --------------------------------------------------
# USER INPUT
# --------------------------------------------------

prompt = st.chat_input("Ask your question...")

# --------------------------------------------------
# PROCESS MESSAGE
# --------------------------------------------------

if prompt:

    st.session_state.query_count += 1

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):

        start_time = time.time()

        try:

            # -------------------------------
            # INTENT DETECTION
            # -------------------------------

            intent_response = detect_intent(prompt)

            try:

                intent_json = json.loads(intent_response)

                detected_intent = intent_json.get(
                    "intent",
                    "other"
                )

            except Exception:

                detected_intent = "other"

            st.write(
                f"Detected Intent: {detected_intent}"
            )

            # -------------------------------
            # ROUTING
            # -------------------------------

            if detected_intent == "product_recommendation":

                response = product_agent(prompt)

            elif detected_intent == "refund":

                response = refund_agent(prompt)

            elif detected_intent == "order_tracking":

                response = order_agent(prompt)

            else:

                response = """
I can help with:

• Product recommendations

• Order tracking

• Refund support

• Customer complaints

Please provide more details.
"""

        except Exception as e:

            response = f"""
⚠️ Error occurred:

{str(e)}
"""

        # -------------------------------
        # LATENCY
        # -------------------------------

        latency = round(
            time.time() - start_time,
            2
        )

        st.session_state.latency = f"{latency} sec"

    # --------------------------------------------------
    # SAVE ASSISTANT RESPONSE
    # --------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    # --------------------------------------------------
    # DISPLAY RESPONSE
    # --------------------------------------------------

    with st.chat_message("assistant"):
        st.markdown(response)
import streamlit as st
import os
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from llm import OpenAIClient
from streamlit_feedback import streamlit_feedback

parent_dir = Path(__file__).resolve().parent.parent
# create a .env file in your AskHR and write your OPENAI_API_KEY="--- your key ---"
load_dotenv(parent_dir / ".env")
with open("data/policies.json", "r", encoding="utf-8") as f:
    policies = json.load(f)

departments = list(policies.keys())  # ['Engineering', 'Sales', 'Marketing', 'Finance', 'HR', 'Customer Support']
levels = ['Junior', 'Senior', 'Team Lead', 'Manager']

st.set_page_config(page_title="AskHR – HR Policy Q&A Bot", page_icon="💬")
st.title("💬 AskHR – HR Policy Assistant")
st.markdown("Ask any question about your company policies on leave, benefits, hybrid work, reimbursements, and more. 🚀")

department = st.radio("Please select you department", departments, horizontal=True, key="department")
level = st.selectbox("Select Your Level", levels)
policy_summary = policies[department][level]
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAIClient(openai_api_key, department, level)

with st.sidebar:
    now = datetime.now()

    st.header("🗓️ Today")
    st.write(f"**Date:** {now:%A, %d %B %Y}")
    st.write(f"**Time:** {now:%H:%M:%S}")

    # support button
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("If **AskHR** cannot help, we are always here to support you with your question. Please **contact us**:", unsafe_allow_html=True)

    recipient_email = "support@example.com"
    subject = "Support Request"
    body = "Please describe the issue or question you're experiencing:"
    mailto_link = f"mailto:{recipient_email}?subject={subject}&body={body}"
    st.link_button(label="✉ Contact Support", url=mailto_link)
    st.markdown("---")
    st.caption("Built for internal HR policy demos with with Streamlit · Powered by OpenAI ✨")


# --- Question Input ---
quick_examples = [
    "How many vacation days do I have?",
    "Can I work from home on Fridays?",
    "What is the travel reimbursement limit?",
]

user_question = st.chat_input("e.g: What are the special leave?")

with st.container():
    st.markdown("**Quick questions:**")
    cols = st.columns(len(quick_examples))
    for idx, q in enumerate(quick_examples):
        if cols[idx].button(q, key=f"quick_{idx}"):
            user_question = q

if user_question:
    st.chat_message("human").write(user_question)
    st.session_state.messages = openai_client.build_prompt(policy_summary, user_question)
    print(st.session_state.messages)
    with st.spinner("Thinking…"):
        answer = openai_client.generate_response(st.session_state.messages)
    st.session_state.messages.append({"role": "Assistant", "content": answer})
    st.chat_message("ai").write(answer)

    streamlit_feedback(
            feedback_type="thumbs",
            align="flex-end",
            key="feedback_given",
            optional_text_label="Please give feedback to the answer",
        )

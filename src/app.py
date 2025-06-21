import streamlit as st
import openai

# --- Configuration ---
openai.api_key = st.secrets.get("OPENAI_API_KEY")  # Set your API key in Streamlit secrets

# --- Sample HR Policies ---
policy_data = {
    "Engineering": "Eligible for remote work (2 days/week). Equipment reimbursement up to €500. Standard hours: 9–17. 30 days annual leave. Overtime applies after 40 hrs/week.",
    "Sales": "Client-facing roles. Travel reimbursement for meetings with manager approval. Commission-based pay. Limited remote work.",
    "HR": "Standard hours: 9–17. Handles internal transfers. 30 days annual leave. Parental leave: 6 months for primary caregiver.",
    "Finance": "Payroll on 25th each month. Tax forms issued in March. Training budget available upon request.",
    "Marketing": "Eligible for remote work. Travel reimbursement for events. 30 days annual leave. Must follow social media guidelines.",
    "Customer Support": "Shift-based roles. Weekend work applicable. Sick leave requires a doctor's note. Overtime paid beyond 40 hrs/week."
}

# --- Streamlit UI ---
st.set_page_config(page_title="HR Policy Q&A Bot")
st.title("💬 HR Policy Assistant")
st.markdown("Ask your company policy questions and get instant answers.")

# Department selection
department = st.sidebar.selectbox("Select Your Department", list(policy_data.keys()))

# User question
user_question = st.text_input("Your HR question:", placeholder="e.g., How many vacation days do I get?")

if st.button("Ask HR Bot") and user_question:
    with st.spinner("Thinking..."):
        # Compose prompt
        system_prompt = f"""
        You are a helpful HR assistant.
        Answer the employee's question based on the following HR policy for the {department} department:

        """
        + policy_data[department] + "\n"

        user_prompt = f"Employee from {department} department asks: '{user_question}'"

        # Call OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.4,
        )

        answer = response.choices[0].message.content
        st.success("Response from HR Bot:")
        st.write(answer)

# Footer
st.markdown("---")
st.markdown("Built for internal HR policy demos with Streamlit and OpenAI ✨")

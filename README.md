# 🚀 AskHR — Streamlit-Powered HR Policy Chatbot

AskHR is a lightweight **Streamlit** app that demos how Large Language Models (LLMs) can answer employees’ HR-policy questions in seconds.  
It ships with synthetic policy data, department/level selectors, chat history, and a “Contact Support” button for escalation.

---

## 📂 Repository Structure

```txt
.
├── data/
│   └── policies.json        # Sample HR policies (6 departments × 4 seniority levels)
├── src/
│   ├── app.py               # Streamlit UI + chat logic
│   └── llm.py               # OpenAIClient class (prompt builder + responder)
├── .env                     # Your OpenAI API key lives here
├── requirements.txt         # Python deps
└── README.md
```

### ```policies.json```
- Six departments: Engineering, Sales, Marketing, Finance, HR, Customer Support
- Four levels each: Junior, Senior, Team Lead, Manager

### ```llm.json```

```
class OpenAIClient:
    def build_prompt(dept, level, user_question) -> list[dict]:
        """Returns a messages list ready for ChatCompletion.create()."""

    def complete(messages) -> str:
        """Calls OpenAI and returns the assistant’s answer."""
```

### ```app.json```
- Department and Level selectors (sidebar)
- Quick-question buttons for instant starter prompts
- Full chat history stored in st.session_state
- Contact Support button (mailto: link)
- Fallback UI if policy data is missing

## 🔧 Setup & Run
1. Clone & install
```
git clone https://github.com/your-org/askhr.git
cd askhr
pip install -r requirements.txt

```

2. Add your OpenAI key
```
OPENAI_API_KEY=sk-...
```

3. Launch
```
streamlit run src/app.py

```
4. Explore
- Pick a department and level in the sidebar.
- Click a starter question or type your own.
- Need more help? Hit ✉️ Contact Support to open an email draft.

## 🏁 That’s It!
Fire up the app, tweak the policies, and enjoy building your very first chatbot! 🎉

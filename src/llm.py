import os
import json
from dotenv import load_dotenv
import time
import streamlit as st
from openai import OpenAI
from typing import List


class OpenAIClient:
    def __init__(self, openai_api_key, department, level):
        self.client = OpenAI(api_key=openai_api_key)
        self.department = department
        self.level = level

    def build_prompt(self, policy_summary, user_question):
        """
        Combine a system instruction, the retrieved document snippets, and the user query
        into a single prompt for the ChatCompletion API.
        """
        system_prompt = f"""
        You are a helpful internal HR assistant.\n
        Answer the employee's question based only on the policy summary provided. 
        If you are uncertain, state that you are unsure and suggest contacting HR.\n\n
        Policy summary for {self.department} – {self.level}:\n + {json.dumps(policy_summary)} + \n
        """

        user_prompt = f"Employee ({self.department}, {self.level}) asks: '{user_question}'"

        messages = [
                       {"role": "system", "content": system_prompt},
                       {"role": "user", "content": user_prompt},
                   ]
        return messages

    def generate_response(self, messages: List) -> str:
        """
        Calls Azure OpenAI's ChatCompletion endpoint via the chat‐style API,
        but passing our entire prompt as a single user message to a conversation.
        """
        completion = self.client.chat.completions.create(
            messages=messages,
            model="gpt-4o-mini",
            max_tokens=512,
            temperature=0.2,
            n=1,
            stop=None
        )
        return completion.choices[0].message.content.strip()

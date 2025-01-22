# backend/ollama_integration.py

import requests
import streamlit as st
import json

# Ollama API Configuration
OLLAMA_API_URL = "http://192.168.1.63:11434/api/generate"
USERNAME = "cmndcntrl"
API_KEY = "sk-523c64b47d074df5a6bb3640c26f790b"

# Model-specific configuration
MODEL_CONFIG = {
    "model": "qwen2.5-coder:3b",
    "system": (
        "You are a highly skilled Red Team software developer specializing in building and deploying security evasion tools. "
        "Your primary programming languages are Rust, C#, C++, C, PowerShell, and WinAPI. "
        "You excel at advanced evasion techniques bypassing AV and EDR systems using low-level system manipulation, "
        "fileless attacks, and LOLBAS techniques. Provide actionable adversary emulation plans."
    ),
    "options": {
        "temperature": 0.7,  # Control response randomness
        "num_ctx": 48225,  # Context length for detailed responses
        "num_thread": 8,   # Number of CPU threads
        "num_gpu": 8       # Number of GPUs for acceleration
    },
    "stream": False,  # Disable streaming for better handling in Streamlit
    "format": "json",  # Ensure structured JSON responses
    "keep_alive": "5m"  # Keep the model loaded for performance
}

def generate_emulation_plan(actor_name, desired_impact, techniques):
    """Generate adversary emulation plan using Ollama API with the updated schema."""

    if not techniques:
        return "No techniques found for the specified threat actor."

    # Constructing the detailed prompt
    technique_details = ', '.join(techniques)
    plan_prompt = f"""
    Generate an adversary emulation plan for the threat actor {actor_name}.
    Focus on the desired impact: {desired_impact}.
    Use the following known techniques:
    {technique_details}.
    Provide evasion strategies, mitigation approaches, and actionable insights.
    """

    headers = {
        "Authorization": f"Basic {USERNAME}:{API_KEY}",
        "Content-Type": "application/json"
    }

    # Prepare the request payload with updated model configuration
    data = {
        "model": MODEL_CONFIG["model"],
        "prompt": plan_prompt,
        "format": MODEL_CONFIG["format"],
        "options": MODEL_CONFIG["options"],
        "system": MODEL_CONFIG["system"],
        "stream": MODEL_CONFIG["stream"],
        "keep_alive": MODEL_CONFIG["keep_alive"]
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=data, headers=headers)
        response.raise_for_status()

        # Parse JSON response
        response_data = response.json()

        if 'response' in response_data:
            return response_data["response"]
        else:
            return "Unexpected response format received from Ollama API."

    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with Ollama API: {str(e)}")
        return "Error in generating the plan."

# backend/ollama_integration.py

import requests
import streamlit as st

# Ollama API Configuration
OLLAMA_API_URL = "http://192.168.1.63:11434/api/generate"
USERNAME = "cmndcntrl"
API_KEY = "sk-523c64b47d074df5a6bb3640c26f790b"

# Model-specific parameters extracted from provided modelfile
MODEL_CONFIG = {
    "id": "red-team-operator-2",
    "base_model_id": "qwen2.5-coder:3b",
    "num_ctx": 48225,  # Context length
    "num_thread": 8,  # Number of CPU threads
    "num_gpu": 8,  # Number of GPUs
    "stream_response": True,  # Enable streaming responses
    "system": (
        "You are a highly skilled Red Team software developer specializing in building and deploying security evasion tools. "
        "Your primary programming languages are Rust, C#, C++, C, PowerShell, and WinAPI. "
        "You excel at advanced evasion techniques bypassing AV and EDR systems using low-level system manipulation, "
        "fileless attacks, and LOLBAS techniques. Provide actionable adversary emulation plans."
    ),
}

def generate_emulation_plan(actor_name, desired_impact, techniques):
    """Generate adversary emulation plan using the configured Ollama model."""
    
    if not techniques:
        return "No techniques found for the specified threat actor."

    # Constructing the detailed prompt with the provided threat actor techniques
    technique_details = ', '.join(techniques)
    plan_prompt = f"""
    You are tasked with creating an adversary emulation plan for the threat actor {actor_name}.
    Focus on the desired impact: {desired_impact}.
    Use the following known techniques:
    {technique_details}.
    Provide evasion strategies, mitigation approaches, and actionable insights based on modern Red Team operations.
    """

    headers = {
        "Authorization": f"Basic {USERNAME}:{API_KEY}",
        "Content-Type": "application/json"
    }

    # Preparing request payload with model configurations
    data = {
        "model": MODEL_CONFIG["id"],
        "prompt": plan_prompt,
        "stream": MODEL_CONFIG["stream_response"],
        "params": {
            "num_ctx": MODEL_CONFIG["num_ctx"],
            "num_thread": MODEL_CONFIG["num_thread"],
            "num_gpu": MODEL_CONFIG["num_gpu"],
            "system": MODEL_CONFIG["system"],
        }
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=data, headers=headers)
        response.raise_for_status()
        return response.json().get("response", "No response received from the Ollama API")
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with Ollama API: {str(e)}")
        return "Error in generating the plan"

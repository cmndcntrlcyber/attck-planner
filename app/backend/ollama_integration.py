import requests
import logging
import os
from dotenv import load_dotenv
from base64 import b64encode

# Load environment variables
load_dotenv()

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL")
USERNAME = os.getenv("USERNAME")
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "red-team-dev")

logging.basicConfig(
    filename="ollama_api.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def generate_emulation_plan(actor_name, desired_impact, techniques):
    """
    Generates an adversary emulation plan using the Ollama API.
    """
    if not techniques:
        logging.warning(f"No techniques found for {actor_name}")
        return "No techniques found for the specified threat actor."

    # Build the emulation plan prompt dynamically
    technique_details = "\n".join([f"- {tech}" for tech in techniques])

    plan_prompt = f"""
    Create an adversary emulation plan for the threat actor {actor_name}.
    Focus on the desired impact: {desired_impact}.
    Use the following known techniques with MITRE ATT&CK:

    {technique_details}

    For each technique, provide:
    - **Description**
    - **Instructions**
    - **Recommended programming language**
    - **Exploit script**

    Format output as Markdown.
    """

    headers = {
        "Authorization": f"Basic {b64encode(f'{USERNAME}:{API_KEY}'.encode()).decode()}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL_NAME,
        "prompt": plan_prompt,
        "stream": False
    }

    try:
        logging.info(f"Requesting emulation plan for {actor_name} with impact {desired_impact}")
        response = requests.post(OLLAMA_API_URL, json=data, headers=headers, timeout=300)
        response.raise_for_status()

        response_json = response.json()

        if 'response' in response_json:
            logging.info(f"Received response for {actor_name}")
            return response_json["response"]
        else:
            logging.error(f"Unexpected response format for {actor_name}")
            return "Unexpected response format received from Ollama API."

    except requests.exceptions.RequestException as e:
        logging.error(f"Error communicating with Ollama API: {str(e)}")
        return f"Error communicating with Ollama API: {str(e)}"

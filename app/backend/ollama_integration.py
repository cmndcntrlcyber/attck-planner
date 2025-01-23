import requests
import logging
import os
from dotenv import load_dotenv
from base64 import b64encode

# Load environment variables
load_dotenv()

# Read configuration from environment variables
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL")
USERNAME = os.getenv("USERNAME")
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

# Configure logging
logging.basicConfig(
    filename="ollama_api.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_technique_info(technique):
    """
    Retrieves the MITRE Tactic and Technique ID for a given known technique.
    Example output: 'Abuse Elevation Control Mechanism: Elevated Execution with Prompt: T1548.004, T1548, TA0005, TA0005'
    """
    # This is an example mapping; in production, fetch dynamically from MITRE ATT&CK API or STIX data.
    technique_mapping = {
        "Abuse Elevation Control Mechanism": "T1548.004, T1548, TA0005, TA0005",
        "Pass the Hash": "T1550.002, T1550, TA0003, TA0004",
        "Credential Dumping": "T1003, T1003.001, TA0006, TA0004",
        "Persistence via Registry": "T1547.001, T1547, TA0003",
    }

    tactic_info = technique_mapping.get(technique, "Unknown ID")
    return f"{technique}: {tactic_info}"


def generate_emulation_plan(actor_name, desired_impact, techniques):
    """
    Generates an adversary emulation plan using the Ollama API.
    Includes MITRE tactic and technique IDs.
    """
    if not techniques:
        logging.warning(f"No techniques found for {actor_name}")
        return "No techniques found for the specified threat actor."

    # Fetch technique info with tactic and technique ID for each known technique
    technique_details = "\n".join([get_technique_info(tech) for tech in techniques])

    plan_prompt = f"""
    Create an adversary emulation plan for the threat actor {actor_name}.
    Focus on the desired impact: {desired_impact}.
    Use the following known techniques with MITRE ATT&CK tactic and technique IDs:
    
    {technique_details}

    Include mitigation strategies where applicable.
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
        response = requests.post(OLLAMA_API_URL, json=data, headers=headers, timeout=60)
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

import requests
from base64 import b64encode

# Configuration
OLLAMA_API_URL = "http://192.168.1.63:11434/api/generate"
USERNAME = "cmndcntrl"
API_KEY = "sk-523c64b47d074df5a6bb3640c26f790b"

def fetch_techniques_for_actor(actor_name):
    """
    Simulate fetching techniques for a given threat actor.
    Returns dummy techniques for testing.
    """
    if actor_name.lower() == "apt29":
        return [
            {"technique_id": "T1071", "technique_name": "Application Layer Protocol"},
            {"technique_id": "T1059", "technique_name": "Command and Scripting Interpreter"}
        ]
    return []

def generate_emulation_plan(actor_name, desired_impact):
    """
    Generate an adversary emulation plan using the Ollama API.
    """
    techniques = fetch_techniques_for_actor(actor_name)
    if not techniques:
        return "No techniques found for the specified threat actor."

    technique_details = ', '.join([f"{tech['technique_id']} - {tech['technique_name']}" for tech in techniques])

    plan_prompt = f"""
    Create an adversary emulation plan for the threat actor {actor_name}.
    Focus on the desired impact: {desired_impact}.
    Use the following known techniques:
    {technique_details}.
    Include mitigation strategies where applicable.
    """

    headers = {
        "Authorization": f"Basic {b64encode(f'{USERNAME}:{API_KEY}'.encode()).decode()}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "qwen2.5-coder:3b",
        "prompt": plan_prompt,
        "stream": False,
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json().get("response", "No response received")
    except requests.exceptions.RequestException as e:
        return f"Error communicating with Ollama API: {str(e)}"

# Test the script with APT29
if __name__ == "__main__":
    threat_actor = "APT29"
    impact = "Data Exfiltration"
    result = generate_emulation_plan(threat_actor, impact)
    print("Generated Emulation Plan:\n", result)

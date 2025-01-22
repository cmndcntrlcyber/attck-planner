import requests
from base64 import b64encode
import streamlit as st

# Configuration
OLLAMA_API_URL = "http://192.168.1.63:11434/api/generate"
USERNAME = "cmndcntrl"
API_KEY = "sk-523c64b47d074df5a6bb3640c26f790b"

def fetch_techniques_for_actor(actor_name):
    """
    Simulate fetching techniques for a given threat actor.
    Returns dummy techniques for testing.
    """
    threat_actor_data = {
        "APT29": [
            {"technique_id": "T1071", "technique_name": "Application Layer Protocol"},
            {"technique_id": "T1059", "technique_name": "Command and Scripting Interpreter"}
        ],
        "FIN7": [
            {"technique_id": "T1203", "technique_name": "Exploitation for Client Execution"},
            {"technique_id": "T1566", "technique_name": "Phishing"}
        ]
    }
    return threat_actor_data.get(actor_name.upper(), [])

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
        "model": "red-team-operator-2",
        "prompt": plan_prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        response_json = response.json()

        if 'response' in response_json:
            return response_json["response"]
        else:
            return "Unexpected response format received from Ollama API."

    except requests.exceptions.RequestException as e:
        return f"Error communicating with Ollama API: {str(e)}"

# Streamlit UI to test the API
def main():
    st.title("Test Ollama Threat Emulation Plan")

    threat_actor = st.text_input("Enter Threat Actor (e.g., APT29)")
    desired_impact = st.selectbox("Select Desired Impact", ["Data Exfiltration", "Credential Theft", "System Disruption"])

    if st.button("Generate Emulation Plan"):
        with st.spinner("Generating plan..."):
            result = generate_emulation_plan(threat_actor, desired_impact)
            st.text_area("Generated Plan", result, height=300)

if __name__ == "__main__":
    main()

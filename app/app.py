import streamlit as st
import requests
import logging
import simplejson as json
from stix2 import MemoryStore, Filter

# Suppress logging
logging.getLogger('stix2').setLevel(logging.CRITICAL)

# Configuration
OLLAMA_API_URL = "http://192.168.1.63:11434/api/generate"
USERNAME = "cmndcntrl"
API_KEY = "sk-523c64b47d074df5a6bb3640c26f790b"

# Load ATT&CK data
ATTACK_DATA_URL = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"
response = requests.get(ATTACK_DATA_URL)
attack_data = MemoryStore(stix_data=response.json()["objects"])

class AttackAPI:
    def get_actor_techniques(self, actor_name):
        try:
            filters = [
                Filter('type', '=', 'intrusion-set'),
                Filter('name', '=', actor_name)
            ]
            group = attack_data.query(filters)
            if group:
                group_id = group[0]['id']
                relationships = attack_data.relationships(group_id, 'uses')
                techniques = [attack_data.get(r.target_ref) for r in relationships]
                return [tech['name'] for tech in techniques if tech and tech['type'] == 'attack-pattern']
            else:
                st.error("Threat actor not found.")
                return []
        except Exception as e:
            st.error(f"Error querying ATT&CK data: {str(e)}")
            return []

def generate_emulation_plan(actor_name, desired_impact):
    api = AttackAPI()
    techniques = api.get_actor_techniques(actor_name)
    if not techniques:
        return "No techniques found for the specified threat actor."
    technique_details = ', '.join(techniques)
    plan_prompt = f"""
    Create an adversary emulation plan for the threat actor {actor_name}.
    Focus on the desired impact: {desired_impact}.
    Use the following known techniques:
    {technique_details}.
    Include mitigation strategies where applicable.
    """
    headers = {
        "Authorization": f"Basic {USERNAME}:{API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "red-team-operator-2",
        "prompt": plan_prompt,
        "stream": True, "flags": "-d"
    }
    try:
        response = requests.post(OLLAMA_API_URL, json=data, headers=headers)
        response.raise_for_status()
        return response.json().get("response", "No response received")
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with Ollama API: {str(e)}")
        return ""

def main():
    st.title("Adversary Threat Emulation Plan Generator")
    actor_name = st.text_input("Enter Threat Actor Name (e.g., APT29)")
    desired_impact = st.selectbox("Select Desired Impact", ["Data Exfiltration", "Credential Theft", "System Disruption"])
    if st.button("Generate Plan"):
        with st.spinner("Generating threat emulation plan..."):
            plan = generate_emulation_plan(actor_name, desired_impact)
            if plan:
                st.success("Emulation Plan Generated Successfully!")
                st.text_area("Generated Plan", plan, height=400)
            else:
                st.error("Failed to generate emulation plan.")

if __name__ == "__main__":
    main()

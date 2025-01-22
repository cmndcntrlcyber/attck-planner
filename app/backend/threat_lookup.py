# backend/threat_lookup.py

import requests
from stix2 import MemoryStore, Filter
import streamlit as st

ATTACK_DATA_URL = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"

# Load ATT&CK framework data
def load_attack_data():
    try:
        response = requests.get(ATTACK_DATA_URL)
        response.raise_for_status()
        return MemoryStore(stix_data=response.json()["objects"])
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching ATT&CK data: {str(e)}")
        return None

attack_data = load_attack_data()

def get_threat_actor_techniques(actor_name):
    """Retrieve techniques used by a threat actor from ATT&CK data."""
    if not attack_data:
        return []

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

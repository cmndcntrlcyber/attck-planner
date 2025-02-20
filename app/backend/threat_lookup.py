import os
import requests
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

ATTACK_JSON_URL = os.getenv(
    "ATTACK_JSON_URL",
    "https://raw.githubusercontent.com/mitre/cti/refs/heads/master/enterprise-attack/enterprise-attack.json"
)

# Configure logging
logging.basicConfig(
    filename="threat_lookup.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_threat_actor_techniques(actor_name):
    """
    Fetches techniques associated with a given threat actor (group).
    """
    logging.info(f"Fetching ATT&CK data for actor: {actor_name}")

    try:
        response = requests.get(ATTACK_JSON_URL, timeout=60)
        response.raise_for_status()
        attack_data = response.json()
    except Exception as e:
        logging.error(f"Error retrieving ATT&CK data: {e}")
        return []

    # Extract groups (threat actors)
    groups = [obj for obj in attack_data["objects"] if obj["type"] == "intrusion-set"]

    # Extract techniques
    techniques = {obj["id"]: obj for obj in attack_data["objects"] if obj["type"] == "attack-pattern"}

    # Find the threat actor
    found_group = next((g for g in groups if g["name"].lower() == actor_name.lower()), None)
    
    if not found_group:
        logging.warning(f"No matching threat actor found for: {actor_name}")
        return []

    group_id = found_group["id"]

    # Retrieve associated techniques
    associated_techniques = []
    for relation in attack_data["objects"]:
        if relation.get("type") == "relationship" and relation.get("source_ref") == group_id:
            target_id = relation.get("target_ref")
            if target_id in techniques:
                technique = techniques[target_id]
                associated_techniques.append(technique["name"])

    logging.info(f"Found {len(associated_techniques)} techniques for {actor_name}")
    return associated_techniques

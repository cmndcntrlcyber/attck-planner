import os
import sys
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# URL to fetch the latest MITRE ATT&CK dataset
ATTACK_JSON_URL = os.getenv(
    "ATTACK_JSON_URL",
    "https://raw.githubusercontent.com/mitre/cti/refs/heads/master/enterprise-attack/enterprise-attack.json"
)

# Ensure a threat actor name is provided
if len(sys.argv) < 2:
    print("Usage: python script.py <threat_actor_name>")
    sys.exit(1)

threat_actor_name = sys.argv[1].lower()  # Normalize input to lowercase

# Fetch MITRE ATT&CK data
print("Fetching latest ATT&CK data...")
response = requests.get(ATTACK_JSON_URL)
if response.status_code != 200:
    print("Failed to retrieve ATT&CK data. Exiting.")
    sys.exit(1)

attack_data = response.json()

# Extract all threat actor groups
groups = [obj for obj in attack_data["objects"] if obj["type"] == "intrusion-set"]

# Extract all techniques
techniques = {obj["id"]: obj for obj in attack_data["objects"] if obj["type"] == "attack-pattern"}

# Find the specified threat actor
found = False
for group in groups:
    if threat_actor_name in group["name"].lower():  # Case-insensitive search
        found = True
        group_name = group["name"]
        group_id = group["id"]
        print(f"\nThreat Actor: {group_name}")

        # Find associated techniques
        associated_techniques = []
        for relation in attack_data["objects"]:
            if relation.get("type") == "relationship" and relation.get("source_ref") == group_id:
                target_id = relation.get("target_ref")
                if target_id in techniques:
                    technique = techniques[target_id]
                    technique_name = technique["name"]
                    technique_id = technique["external_references"][0]["external_id"]
                    associated_techniques.append(f"  - {technique_name} (ID: {technique_id})")

        # Print techniques if found
        if associated_techniques:
            print("Associated Techniques:")
            print("\n".join(associated_techniques))
        else:
            print("  - No associated techniques found.")
        break

if not found:
    print(f"No threat actor found matching '{threat_actor_name}'.")

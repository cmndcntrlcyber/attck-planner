# app.py

import streamlit as st
from backend.threat_lookup import get_threat_actor_techniques
from backend.ollama_integration import generate_emulation_plan

st.title("Adversary Threat Emulation Plan Generator")

# User inputs
actor_name = st.text_input("Enter Threat Actor Name (e.g., APT29)")
desired_impact = st.selectbox("Select Desired Impact", 
                             ["Data Exfiltration", "Credential Theft", "System Disruption"])

if st.button("Generate Plan"):
    with st.spinner("Generating threat emulation plan..."):
        techniques = get_threat_actor_techniques(actor_name)

        if techniques:
            plan = generate_emulation_plan(actor_name, desired_impact, techniques)
            st.success("Emulation Plan Generated Successfully!")
            st.text_area("Generated Plan", plan, height=400)
        else:
            st.error("Failed to generate emulation plan. No techniques found for the specified actor.")

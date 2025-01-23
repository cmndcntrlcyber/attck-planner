# app.py

import streamlit as st
from backend.threat_lookup import get_threat_actor_techniques
from backend.ollama_integration import generate_emulation_plan
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Streamlit UI
st.title("Adversary Threat Emulation Plan Generator")

# User inputs
actor_name = st.text_input("Enter Threat Actor Name (e.g., APT29)")
desired_impact = st.selectbox("Select Desired Impact", 
                             ["Data Exfiltration", "Credential Theft", "System Disruption"])

@st.cache_data(show_spinner=True)
def cached_get_threat_actor_techniques(actor_name):
    """ Cached version of fetching threat actor techniques. """
    return get_threat_actor_techniques(actor_name)

if st.button("Generate Plan"):
    with st.spinner("Generating threat emulation plan..."):
        # Get techniques (with caching)
        techniques = cached_get_threat_actor_techniques(actor_name)

        if techniques:
            # Generate emulation plan
            plan = generate_emulation_plan(actor_name, desired_impact, techniques)

            st.success("Emulation Plan Generated Successfully!")

            # Display generated plan
            st.text_area("Generated Plan", plan, height=400)

            # Provide download option
            st.download_button(
                label="Download Emulation Plan",
                data=plan,
                file_name=f"{actor_name}_emulation_plan.txt",
                mime="text/plain"
            )
        else:
            st.error("Failed to generate emulation plan. No techniques found for the specified actor.")

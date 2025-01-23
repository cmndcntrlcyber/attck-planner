# app.py

import streamlit as st
from backend.threat_lookup import get_threat_actor_techniques
from backend.ollama_integration import generate_emulation_plan
import logging
import time

# Configure logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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
        start_time = time.time()

        # Get techniques (with caching)
        techniques = cached_get_threat_actor_techniques(actor_name)

        if techniques:
            # Generate emulation plan
            plan = generate_emulation_plan(actor_name, desired_impact, techniques)

            # Log success
            logging.info(f"Plan generated successfully for {actor_name} in {time.time() - start_time:.2f}s")

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
            logging.error(f"No techniques found for threat actor: {actor_name}")

# Feedback section
st.sidebar.header("Feedback")

feedback_text = st.sidebar.text_area("Provide your feedback here:")

if st.sidebar.button("Submit Feedback"):
    if feedback_text:
        with open("user_feedback.log", "a") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Feedback: {feedback_text}\n")
        st.sidebar.success("Thank you for your feedback!")
        logging.info("User feedback submitted.")
    else:
        st.sidebar.error("Please enter your feedback before submitting.")

# backend/attck_gen.py

import os
import ast
import logging
from dotenv import load_dotenv
from langchain.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from typing import Dict, Any

# Load environment variables
load_dotenv()

# Load Ollama API credentials from .env
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL")
MODEL_NAME = os.getenv("MODEL_NAME")  # AI model name, e.g., "red-team-expert"

# Configure logging
logging.basicConfig(
    filename="attck_gen.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Define prompt templates for script generation
SCRIPT_GEN_PROMPT = PromptTemplate(
    input_variables=["phase_description"],
    template="""
    Generate a detailed implementation of the following adversary emulation phase using the most appropriate programming language.
    Phase Description: {phase_description}
    
    Provide:
    - The complete source code.
    - Language used.
    - Short description.
    - Recommended filename.

    Response format (JSON):
    {{
        "code": "<script_code>",
        "language": "<chosen_language>",
        "description": "<description>",
        "filename": "<suggested_filename>"
    }}
    """
)


def load_llm():
    """Load the Ollama LLM model."""
    return Ollama(model=MODEL_NAME, base_url=OLLAMA_API_URL)


def generate_script(phase_description: str) -> Dict[str, Any]:
    """
    Generates a script for the given adversary emulation phase.

    Args:
        phase_description (str): The emulation phase to generate code for.

    Returns:
        Dict[str, Any]: A dictionary containing the generated script, language, description, and filename.
    """

    llm = load_llm()
    chain = LLMChain(prompt=SCRIPT_GEN_PROMPT, llm=llm)

    try:
        logging.info(f"Generating script for phase: {phase_description}")
        
        response = chain.run({"phase_description": phase_description})
        cleaned_response = ast.literal_eval(response)

        # Validate response structure
        required_keys = {"code", "language", "description", "filename"}
        if not all(key in cleaned_response for key in required_keys):
            raise ValueError("Missing expected keys in LLM response.")

        logging.info(f"Script generated successfully for phase: {phase_description}")
        return cleaned_response

    except Exception as e:
        logging.error(f"Error generating script: {str(e)}")
        return {"error": str(e)}


def save_script(script_data: Dict[str, Any], output_dir="output"):
    """
    Saves the generated script to a file.

    Args:
        script_data (Dict[str, Any]): The script data containing code, language, description, and filename.
        output_dir (str): Directory where the script should be saved.
    """
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, script_data["filename"])

    try:
        with open(filepath, "w") as f:
            f.write(script_data["code"])

        logging.info(f"Script saved to {filepath}")
        print(f"Generated script saved: {filepath}")

    except Exception as e:
        logging.error(f"Error saving script to {filepath}: {str(e)}")
        print(f"Error saving script: {e}")


def process_emulation_plan(emulation_plan: str):
    """
    Processes the adversary emulation plan, generates scripts for each phase.

    Args:
        emulation_plan (str): A text-based adversary emulation plan.
    """
    phases = emulation_plan.strip().split("\n\n")
    
    for phase in phases:
        if not phase.strip():
            continue

        print(f"\nProcessing phase: {phase[:50]}...")  # Displaying part of phase
        script_data = generate_script(phase)

        if "error" not in script_data:
            save_script(script_data)
        else:
            logging.error(f"Skipping phase due to error: {script_data['error']}")


if __name__ == "__main__":
    # Example usage: Read emulation plan from file and process it
    try:
        with open("generated_emulation_plan.txt", "r") as file:
            emulation_plan_content = file.read()
        
        process_emulation_plan(emulation_plan_content)
    
    except FileNotFoundError:
        logging.error("Generated emulation plan file not found.")
        print("No emulation plan found. Ensure 'generated_emulation_plan.txt' exists.")

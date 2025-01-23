import os
import json
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

SCRIPT_GEN_PROMPT = PromptTemplate(
    input_variables=["technique", "description"],
    template="""
    Generate a script for the following adversary emulation technique.
    
    Technique: {technique}
    Description: {description}

    Choose the best programming language (C, C++, Python, PowerShell, Rust, JS).
    Provide code with explanations and recommended filename.

    Output format (JSON):
    {{
        "code": "<script_code>",
        "language": "<chosen_language>",
        "filename": "<suggested_filename>"
    }}
    """
)

def generate_script(technique, description):
    """Generate script using LangChain and Ollama."""
    llm = Ollama(model=MODEL_NAME, base_url=OLLAMA_API_URL)
    chain = LLMChain(prompt=SCRIPT_GEN_PROMPT, llm=llm)

    response = chain.run({"technique": technique, "description": description})
    return json.loads(response)

def save_script(script_data, output_dir="output"):
    """Save the generated script to file."""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, script_data["filename"])
    with open(filepath, "w") as file:
        file.write(script_data["code"])
    return filepath

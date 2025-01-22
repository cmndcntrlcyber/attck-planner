# **Adversary Threat Emulation Planner**

---

## **Project Overview**
The **Adversary Threat Emulation Planner** is a web-based tool built using **Streamlit**, which utilizes the **MITRE ATT&CK framework** and **Ollama API** to generate adversary emulation plans based on a selected threat actor and desired impact. 

The application fetches known attack techniques for specific threat actors and uses the Ollama AI model to generate detailed emulation strategies and mitigation recommendations.

---

## **Features**
- **Threat Actor Lookup:** Retrieve known MITRE ATT&CK techniques used by a specified adversary.
- **Impact Selection:** Choose a desired impact (e.g., Data Exfiltration, Credential Theft, System Disruption).
- **AI-Powered Plan Generation:** Leverage Ollama's Red Team Operator model to generate emulation plans.
- **User-Friendly Interface:** Built with Streamlit for quick and easy interaction.
- **Customizable API Parameters:** Modify model-specific settings to fine-tune responses.

---

## **Project Structure**
```
├── backend/
│   ├── __init__.py
│   ├── threat_lookup.py         # Fetch threat actor techniques from ATT&CK framework
│   ├── ollama_integration.py    # Interact with Ollama API to generate plans
│
├── data/
│   ├── sample_stix_data.json    # Sample MITRE ATT&CK STIX data (for testing)
│
├── test.py                      # Simple test script to verify API functionality
├── app.py                        # Streamlit application entry point
├── docker-compose.yml             # Docker configuration for deployment
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation (this file)
```

---

## **Prerequisites**
Ensure the following software is installed before running the project:

- [Python 3.8+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/get-started)
- [Ollama](https://ollama.ai/)
- Recommended: Virtual environment management (`venv` or `conda`)

---

## **Installation Steps**

### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/threat-emulation-planner.git
cd threat-emulation-planner
```

### **2. Set Up a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate    # For macOS/Linux
venv\Scripts\activate       # For Windows
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Run the Streamlit App**
```bash
streamlit run app.py
```

Once running, open your browser and navigate to `http://localhost:8501`.

---

## **Docker Deployment**
To run the project using Docker, ensure Docker is installed and run:

```bash
docker-compose up -d
```

This will start the application and Ollama API container.

---

## **Configuration**

### **Ollama API Setup**
Ensure the Ollama container is running with port `11434` exposed:

```bash
docker run -d -p 11434:11434 ollama/ollama
```

Modify the **Ollama API URL** inside `backend/ollama_integration.py` if needed:

```python
OLLAMA_API_URL = "http://localhost:11434/api/generate"
```

Set up credentials inside `.env` (optional):

```
OLLAMA_API_URL=http://localhost:11434
USERNAME=cmndcntrl
API_KEY=your_api_key_here
```

---

## **Usage**
1. Open the web interface (`http://localhost:8501`).
2. Enter a **threat actor name**, such as `APT29`.
3. Choose the desired impact (e.g., "Data Exfiltration").
4. Click "Generate Plan" to receive a comprehensive emulation plan.
5. Review and download the generated plan.

---

## **Testing the API**
Use the `test.py` script to verify the Ollama API connection:

```bash
python test.py
```

Expected output (example):

```
Generated Emulation Plan:
  - T1071 - Application Layer Protocol
  - T1059 - Command and Scripting Interpreter
  Mitigation strategies...
```

---

## **Troubleshooting**
1. **404 API Error:** 
   - Ensure the Ollama container is running and port `11434` is correctly exposed.
   - Run `docker ps` to verify container status.

2. **Slow Response Time:**
   - Adjust API parameters such as `num_thread` and `num_gpu` in `backend/ollama_integration.py`.

3. **Python Dependency Issues:**
   - Delete `venv` and reinstall dependencies using `pip install -r requirements.txt`.

---

## **Future Enhancements**
- Add caching to optimize repeated queries.
- Implement authentication for multi-user access.
- Extend adversary emulation coverage using additional threat intelligence sources.

---

## **Contributing**
Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-new-feature`.
3. Commit changes: `git commit -m "Added new feature"`.
4. Push to branch: `git push origin feature-new-feature`.
5. Submit a pull request.

---

## **License**
This project is licensed under the [MIT License](LICENSE).

---

## **Contact**
For support or inquiries, reach out to:

- Email: r.soreng@c3s.consulting
- GitHub: [cmndcntrlcyber/threat-emulation-planner](https://github.com/cmndcntrlcyber/threat-emulation-planner)

---

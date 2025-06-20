# UNDP_LLMTask
# Climate Change and Financing for Development (FFD) June 2025

**Objective:**
This repository provides a full-stack pipeline for exploring and evaluating Climate Change and Financing documents (FFD) using Local LLMs via Ollama.
Process includes:
- Document scraping and preprocessing
- Sentence Embedding & FAISS Vector Indexing
- Semantic Search and Question answering via Langchain
- Front End UI using Streamlit
- Answer evaluation for Accuracy, Relevance, and Clarity (Offline)
- Dockerization of the project (Optional)

## Getting Started

You can follow these instructions to set up the project on your local machine.

**Prerequisites:**

* Python 3.13
  - Download for Windows: https://www.python.org/downloads/
  - Download for MacOS: https://www.python.org/downloads/macos/

* Git
  - Windows: https://git-scm.com/downloads/win
  - MacOS:
    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    brew install git
    ```
* VSCode
  - Download and Install from the Official website: https://code.visualstudio.com/

## Setup Steps (Without Docker)
**1. Clone the repository**

`git clone https://github.com/KeerthikaK98/UNDP_LLMTask `

**2. Set up a Virtual Environment**

**Make sure the following commands are used inside the local project folder**

Windows:
```
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate
```
MacOS:
```
# Create a virtual environment
python3.11 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

**3. Install Requirements**
Install project dependencies

`pip install -r requirements.txt`

**4. .env file**

- .env file contains the variables for llm model, embedding model, persist directory, document path, index path and document URL.
- variables can be updated with the appropriate values

**Install Ollama**

https://ollama.com/

Make sure the ollama is running - by default, mistral is used in .env file

In the Terminal or cmd

```
ollama run mistral
```

**5. Run the application**

In the Command Prompt, run the below code: (make sure it is pointed to the project folder)

**Document Scraping and Processing**
```
python main.py
```
**UI Application**
```
streamlit run streamlit_app.py
```

## Setup with Docker

**1. Installing Docker**

https://docs.docker.com/engine/install/

**2. Prepare the .env file**
- Double check for the models and document paths used
  
**3. Build the Docker Image**
```
docker-compose build
```

**4. Run the Docker Container**
```
docker-compose up -d
```
Access app at: http://localhost:8501

*Note: `main.py` runs during image build to index PDFs. Ollama must still be installed and running locally.*

To destroy the Docker Container:
```
docker-compose down
```
## Exploratory Data Analysis

This project includes a Jupyter Notebook to extract insights and visualize it

**To run eda.ipynb,**
- Make sure virtual environment is activated.(If not activated, refer step 2 to activate it)
- install Jupyter notebook if not done already:
  ```bash
  pip install notebook
  ```

- Open the eda.ipynb file in Virtual Studio Code and run all the cells 






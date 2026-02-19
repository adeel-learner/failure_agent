# 🧠 Failure Post-Mortem Agent (Agentic GenAI Project)

An intelligent, agent-based system that analyzes failures, identifies root causes, detects behavioral patterns, and generates actionable prevention strategies.

Built using:
- LangGraph (multi-agent orchestration)
- LangChain
- OpenAI LLMs
- SQLite (structured memory)
- FAISS (vector memory)
- Streamlit (UI)

---

## 🚀 Overview

The Failure Post-Mortem Agent is a multi-step AI workflow that:

1. Detects whether an event is a failure
2. Classifies failure category and severity
3. Performs root cause analysis
4. Searches historical failures for recurring patterns
5. Generates prevention strategies
6. Persists structured + semantic memory
7. Displays results in a Streamlit web UI

This project demonstrates an **agentic GenAI architecture with memory and reasoning loops**.

---

## 🏗️ Architecture

# 🧠 Failure Post-Mortem Agent (Agentic GenAI Project)

An intelligent, agent-based system that analyzes failures, identifies root causes, detects behavioral patterns, and generates actionable prevention strategies.

Built using:
- LangGraph (multi-agent orchestration)
- LangChain
- OpenAI LLMs
- SQLite (structured memory)
- FAISS (vector memory)
- Streamlit (UI)

---

## 🚀 Overview

The Failure Post-Mortem Agent is a multi-step AI workflow that:

1. Detects whether an event is a failure
2. Classifies failure category and severity
3. Performs root cause analysis
4. Searches historical failures for recurring patterns
5. Generates prevention strategies
6. Persists structured + semantic memory
7. Displays results in a Streamlit web UI

This project demonstrates an **agentic GenAI architecture with memory and reasoning loops**.

---

## 🏗️ Architecture

User Input
↓
Detection Node (LLM)
↓
Postmortem Node (Root Cause Analysis)
↓
Pattern Matching Node (Vector Recall)
↓
Strategy Generation Node
↓
Memory Update (SQL + FAISS)


### Memory Layers

- **SQLite** → Structured failure records
- **FAISS** → Semantic similarity search
- Dual storage enables learning over time

---

## 📁 Project Structure

failure_agent/
│
├── graph/
│ ├── state.py
│ ├── workflow.py
│
├── nodes/
│ ├── detection.py
│ ├── postmortem.py
│ ├── pattern.py
│ ├── strategy.py
│ ├── memory.py
│
├── memory/
│ ├── database.py
│ ├── vector_store.py
│
├── prompts/
│ ├── detection_prompt.py
│ ├── postmortem_prompt.py
│ ├── pattern_prompt.py
│ ├── strategy_prompt.py
│
├── main.py
├── ui.py


---

## 🛠️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/failure-postmortem-agent.git
cd failure-postmortem-agent

2️⃣ Create virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

3️⃣ Install dependencies
pip install -r requirements.txt


Or manually:

pip install langchain langchain-openai langgraph faiss-cpu streamlit python-dotenv

4️⃣ Add OpenAI API Key

Create .env file:

OPENAI_API_KEY=your_api_key_here

▶️ Run the Application
CLI Mode
python failure_agent/main.py

Web UI (Recommended)
streamlit run failure_agent/ui.py


Browser will open automatically.

🧪 Example Input
Missed sprint deadline because requirements were unclear and I kept switching between tasks.

# Example Output

- Failure Detected: True

- Category: planning_error

- Severity: medium

- Root Causes:

    - Requirement ambiguity

    - Multitasking

- Pattern Summary: Repeated scope clarity issues

- Prevention Strategies:

    - Create requirement checklist

    - Limit concurrent tasks

    - Conduct sprint kickoff clarification meeting

## 🧠 Agent Capabilities

LLM-based failure classification

Structured JSON outputs

Pattern detection using vector similarity

Persistent learning across sessions

Multi-step reasoning workflow

Streamlit interactive UI

## 🔮 Future Improvements

Add evaluation metrics

Add confidence scores

Add self-reflection loop

Add analytics dashboard

Add recurring failure alerts

Add FastAPI backend deployment

Dockerize application

Replace FAISS with production vector DB (Pinecone/Milvus)

## 🧩 Why This Project Matters

This is not a single LLM call.
It demonstrates:

Agentic workflow orchestration

Multi-node reasoning pipeline

Long-term memory architecture

Hybrid storage (structured + semantic)

Production-style AI system design


## ⭐ If You Found This Useful

Star the repository and feel free to contribute!



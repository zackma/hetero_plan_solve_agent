# Plan & Solve Agent (Heterogeneous Architecture)

## Project Overview
This project is an experimental framework designed to verify the accessibility and efficacy of a **"Plan and Solve"** agentic workflow. The core innovation lies in its heterogeneous architecture, which strategically assigns distinct Large Language Models (LLMs) to separate roles: **Planning** and **Execution**.

By decoupling these phases, the system aims to leverage the specific strengths of different models—using high-reasoning models for complex task decomposition and high-efficiency models for concrete task execution.

## Architecture

The system operates on a two-stage pipeline:

1.  **The Planner (Brain)**
    *   **Model**: OpenAI GPT (e.g., GPT-4o) via `llm_planner.py`.
    *   **Role**: Analyzes complex user queries and decomposes them into a strictly ordered sequence of independent, executable sub-tasks.
    *   **Output**: A structured Python list of steps (e.g., `["Step 1", "Step 2", ...]`).

2.  **The Executor (Hands)**
    *   **Model**: Google Gemini (e.g., Gemini 1.5/3.0) via `llm_executor.py`.
    *   **Role**: Takes a specific sub-task from the plan, along with the full context (original question, complete plan, and execution history), and generates the solution for that specific step.
    *   **Output**: Concrete results for the current step.

## Directory Structure

```
plansolve-llm-train/
├── src/
│   ├── llms/
│   │   ├── llm_planner.py   # Interface for the Planning Agent (GPT)
│   │   └── llm_executor.py  # Interface for the Execution Agent (Gemini)
│   ├── prompts/
│   │   ├── Planner_Prompts.md  # System instructions for task decomposition
│   │   └── Executor_Prompts.md # System instructions for step execution
│   └── tools/               # Shared utilities (e.g., markdown reading)
├── .env                     # Configuration for API keys
└── pyproject.toml           # Project dependencies and package config
```

## Key Features

*   **Heterogeneous LLM Integration**: Demonstrates the viability of mixing different model providers (OpenAI & Google) in a single cohesive workflow.
*   **Separation of Concerns**: Isolates high-level logic (Planning) from low-level implementation (Execution), reducing hallucination risks and improving error recovery.
*   **Context-Aware Execution**: The Executor maintains awareness of the overall goal and previous results while focusing on the immediate task.

## Installation & Usage

1.  **Install Dependencies**:
    ```bash
    uv pip install -e .
    ```

2.  **Configure Environment**:
    Ensure your `.env` file contains valid keys for both providers:
    ```env
    GPT_MODEL_ID=gpt-4o
    MODEL_API_KEY=sk-...
    GEMINI_MODEL_ID=gemini-3-flash-preview
    # ... other configs
    ```

3.  **Run Modules**:
    You can test the components individually:
    ```bash
    # Test Planner
    python3 src/llms/llm_planner.py
    
    # Test Executor
    python3 src/llms/llm_executor.py
    ```

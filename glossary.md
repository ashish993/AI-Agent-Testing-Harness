# Glossary

Key terms used throughout this project.

---

| Term | Definition |
|------|-----------|
| **Agent** | A system that perceives inputs, reasons about them, and takes actions to reach a goal. |
| **ReAct** | Reason + Act — a prompting pattern where the LLM alternates between thinking steps (Thought) and tool calls (Action). |
| **Tool** | A function an agent can call to interact with the world (search, calculator, database, API). |
| **Context window** | The maximum number of tokens an LLM can process in one call. Memory strategies exist to work around this limit. |
| **In-context memory** | Storing conversation history directly in the prompt. Simple but limited by context window size. |
| **Summary memory** | Periodically compressing old turns into a summary to save tokens while preserving important facts. |
| **External memory** | Persisting facts outside the model (Redis, SQLite, vector DB) so they survive between sessions. |
| **Multi-agent pipeline** | A system where specialised agents hand off work to each other in a defined sequence or graph. |
| **Planner** | An agent whose sole job is to decompose a complex goal into sub-tasks. |
| **Researcher** | An agent that retrieves or generates answers to specific questions. |
| **Writer** | An agent that formats and synthesises information into human-readable output. |
| **Orchestrator** | Code (or an LLM) that coordinates which agent runs next and passes data between agents. |
| **Stub** | A placeholder implementation used in demos so the code runs without real API keys. Replace with real API calls in production. |
| **System prompt** | The initial instruction given to an LLM that defines its persona, capabilities, and constraints. |
| **Function calling** | An LLM feature (OpenAI, Anthropic) where the model outputs structured JSON instead of free text to invoke a tool. |
| **JSON schema** | A standard format for describing the expected shape of JSON data, used to define tool parameters. |
| **RAG** | Retrieval-Augmented Generation — combining a vector search over a knowledge base with an LLM to ground answers in real documents. |
| **Token** | The basic unit of text processed by an LLM (roughly 0.75 words in English). |
| **Hallucination** | When an LLM generates plausible-sounding but factually incorrect information. |
| **Prompt injection** | An attack where malicious text in the environment tricks an agent into performing unintended actions. |

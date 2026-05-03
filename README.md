# AI Agent Testing Harness

A four-module hands-on workshop for building and deploying AI agents.

## Quick Start

```bash
pip install -r requirements.txt
export OPENAI_API_KEY="your-key"
python module_01_first_agent.py
```

## Modules

| Module | Topic | Key Concepts |
|--------|-------|-------------|
| 1 | First Agent | ReAct loop, tool use |
| 2 | Memory and Tools | Short/long-term memory, web search |
| 3 | Multi-Agent | Planner/researcher/writer pipeline |
| 4 | CLI Deploy | Config, logging, packaging |

## Repository Structure

```
AI-Agent-Testing-Harness/
├── module_01_first_agent.py
├── module_02_memory_tools.py
├── module_03_multi_agent.py
├── module_04_cli.py
├── examples/
│   ├── deep_research.py
│   └── multi_agent_workflow.py
├── AGENTS.md
├── glossary.md
└── CLEANUP.md
```

## Security Note

Never commit API keys. See CLEANUP.md.

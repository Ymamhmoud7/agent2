![logo](https://github.com/Ymamhmoud7/agent2/blob/main/images/logoSmall.png)

![AI](https://img.shields.io/badge/AI-blue)

# Avin AI (Multi-LLM Agent)

A lightweight AI System that chains multiple small language models together to evaluate, plan, and execute complex tasks — without relying on a single large model to do everything.

---

## Core Idea

Most AI assistants throw everything at one big model. This project takes a different approach: **divide the cognitive work across multiple small, specialized LLMs**, each doing what it does best. The result is a pipeline that is faster, more modular, and easier to reason about.

I use 4 LLMs:
- Qwen2.5 (0.5b) which is responsible about first routing. (Action - Not Action)
- Qwen2.5 (3b)   which is responsible about confirming what the last llm decided and then it starts planning how will the user input be dealt with.
- Qwen3.5 (4b)   which is responsible about top-tier tasks such as: complex math , coding , image reading etc

## How It Works (On my device)
-- Any LLMs Mentioned can be changed via `config.py` so you pick what you think fits you the most.

1. User Input goes through Qwen2.5 (0.5b) which acts as a fast triage and just decides "is this an action or just a question?"
2. User Input then goes through Qwen2.5 (3b) which confirms what 0.5b decided and then starts planning.
3. If it is an action Qwen2.5 (3b) analyzes the user input (along with any chat context or AI memories) and decides whether it is a complex action such as a coding project or just a skill use.
4. If it is a skill use , 3b just handles the whole thing by checking the `skills` folder and sending back a json that can be ready and executed by python.
5. If it is complex such as coding something, then it will first need to be forwarded to Qwen3.5 (4b) to generate the code and create instructions for 3b to tell it how to use the code.
6. 3b follows 4b instructions and use its skills to finalize the job.

And this can run within low context length (4k-8k). 

---

## Current State

- **`main.py`** — A `curses`-based terminal UI. Renders a scrollable output area and an input box. Supports live token streaming from the LLM so responses appear in real time, character by character.
- **`router.py`** — Calls a small local model (via Ollama) with a routing prompt. Given any user message, it returns either `"Action"` or `"Not Action"`. Uses near-zero temperature for deterministic classification.
- **`utils/`** — Helpers for sending messages to LLMs and checking/starting the Ollama server.
- **`config.py`** — Stores model names and settings in one place.
- **`prompts/`** — Houses the system prompts, including the routing prompt (`ROUTERING_PROMPT`).
The routing layer is working. When a user sends a message, the 0.5B model classifies it. If it's conversational, it goes straight to the 3B for a reply. If it's an action, the pipeline escalates.

## What's Planned
 
### Stage 1 — Double Confirmation (3B Reassurance)
After the 0.5B flags something as an action, pass the message (and the 0.5B's verdict) to the 3B model for a second opinion. The 3B either confirms or overrides, and if confirmed, begins breaking the task into steps using the available skill set.
 
### Stage 2 — Skill Registry
Define a set of available "skills" the system can execute:
- Create a file
- Edit a file
- Move or delete a file
- Run a shell command
- Search within files
- etc.
These skills are described in a structured format so the LLM can reference them when planning.
 
### Stage 3 — 4B Strategic Planning
The 3B sends the confirmed task + available skills to a 4B (or larger) model. The 4B responds with a high-level execution plan: which skills to use, in what order, and with what parameters.
 
### Stage 4 — JSON Action Layer
The 3B receives the 4B's plan and translates it into a structured JSON action list, for example:
 
```json
[
  { "action": "create_file", "path": "game/main.py", "content": "..." },
  { "action": "create_file", "path": "game/assets/", "content": null },
  { "action": "edit_file",   "path": "game/main.py", "find": "...", "replace": "..." }
]
```
 
A Python runner then reads this JSON and executes each action step by step on the real filesystem.
 
### Stage 5 — Feedback Loop
After execution, the results (success, errors, file contents) are fed back into the session so the 3B can verify the outcome or retry failed steps.
 
---
 
## Example: "Make me a Flappy Bird game"
 
1. **0.5B** — Classifies as `Action`
2. **3B** — Confirms it's an action; identifies needed skills: `create_file`, `write_code`
3. **4B** — Returns a step-by-step plan: create `main.py`, set up pygame loop, define bird physics, add pipe generation, handle collisions
4. **3B** — Translates the plan into a JSON action list
5. **Python runner** — Executes the actions, creating and writing the actual game files
6. **3B** — Reviews the result and reports back to the user
---
 
## Why This Architecture?
 
| Reason | Explanation |
|---|---|
| **Speed** | Small models are fast. The 0.5B triage step adds almost no latency. |
| **Local & private** | Everything runs via Ollama — no API calls, no data leaving the machine. |
| **Modular** | Each layer can be swapped or upgraded independently. |
| **Interpretable** | The JSON action layer makes every step visible and auditable before execution. |
| **Scalable** | Bigger tasks just need a bigger model at the strategy layer — the rest stays the same. |
 
---
 
## Tech Stack
 
- **Python** — Core language
- **Ollama** — Local LLM server
- **curses** — Terminal UI
- **JSON** — Action serialization format between the planning and execution layers
---
 
## Project Status
 
> Early prototype. Routing layer is functional. Planning and execution layers are in design.

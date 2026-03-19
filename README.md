# Lemonade Server Manager for OpenClaw NullClaw, and the "Claw" family

This skill enables your OpenClaw or NullClaw AI agent to securely orchestrate, manage, and interact with local and remote Lemonade Server instances. It acts as a comprehensive bridge for model lifecycle management, hardware monitoring, and multimodal inference.

## Core Features

- **Multi-Server Orchestration**: Dynamically route requests to different local or remote Lemonade Servers using the `--url` flag.
- **Zero Command Injection**: All HTTP logic is abstracted into a secure `manager.py` script, preventing malicious prompt injections from executing arbitrary bash commands on your host system.
- **Hardware Awareness**: Allows the agent to query system info, monitor NPU/GPU constraints, and intelligently load/unload models to free up VRAM.
- **Multimodal Ready**: Full support for text completion, chat workflows, and stable-diffusion image generation.

## Installation

You can install this skill globally via ClawHub or manually clone it into your workspace.

### Option 1: ClawHub (Recommended)
```bash
clawhub install lemonade-server-manager
```

### Option 2: Manual Git Setup
Navigate to your workspace and clone the repository:
```bash
cd ~/.openclaw/workspace/skills/
git clone https://github.com/james-martinez/lemonade-server-manager.git
cd lemonade-server-manager
```

> **Security Warning:** Always ensure your `.gitignore` contains `keys.json` before running any Git commands to prevent leaking your API keys.

## Authentication Configuration

This skill supports two methods for authenticating with Lemonade Servers.

### Single Server (Environment Variable)
If you are only interacting with a single local or remote server, you do not need a configuration file. The skill will automatically look for the following environment variable on your host OS:
```bash
export LEMONADE_API_KEY="your-api-key-here"
```

### Multi-Server (keys.json)
If your agent needs to manage multiple remote servers that require different authentication keys, create a `keys.json` file in the root of the skill directory.
```json
{
  "http://192.168.1.50:8000": "sk-remote-gpu-key",
  "https://lemonade.my-domain.com": "sk-cloud-key",
  "http://localhost:8000": ""
}
```

## Available Tools

The agent has access to the following categorized endpoints via the `manager.py` wrapper script:

| Tool Name | Description | Lemonade Endpoint |
| :--- | :--- | :--- |
| `lemonade_get_system_info` | Retrieves hardware and device enumeration. | `/api/v1/system-info` |
| `lemonade_check_health` | Checks server status and loaded models. | `/api/v1/health` |
| `lemonade_pull_model` | Downloads a specified model to the server. | `/api/v1/pull` |
| `lemonade_load_model` | Loads a model into GPU/NPU memory. | `/api/v1/load` |
| `lemonade_unload_model` | Unloads a model to free up system VRAM. | `/api/v1/unload` |
| `lemonade_chat_completion` | Executes standard LLM chat tasks. | `/api/v1/chat/completions` |
| `lemonade_generate_image` | Creates images using stable-diffusion. | `/api/v1/images/generations` |

## Usage Examples

Once installed, ask your OpenClaw or NullClaw agent to perform server tasks:
- *"What models are currently loaded on my local Lemonade server?"*
- *"Check the system health on http://192.168.1.50:8000. If there's enough VRAM, download and load the Llama 3 model."*
- *"Unload the active LLM to free up the NPU."*

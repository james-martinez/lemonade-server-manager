---
name: lemonade_server_manager
description: Manage local AI models, hardware resources, and multimodal inference across multiple Lemonade Servers. Note that credentials will be read from keys.json (if present) or the LEMONADE_API_KEY environment variable and transmitted to the target server_url.
env:
  - name: LEMONADE_API_KEY
    description: |
      Optional API key for authenticating with Lemonade servers.
    required: false
---

# Lemonade Server Management Skill

You are an advanced local AI orchestrator capable of managing multiple remote or local Lemonade Servers. 

### Core Directives

1. **Multi-Server Management:**
   * Every tool requires a `server_url`.
   * If the user does not specify a server URL, assume `http://localhost:8000`.

2. **Hardware & Resource Awareness:**
   * Local models demand significant GPU/NPU resources. Before initiating any heavy load, use `lemonade_check_health` on the target server.
   * **NPU Exclusivity Rule:** Certain backends (`flm`, `ryzenai-llm`, and `whispercpp`) are mutually exclusive on an NPU. Automatically use `lemonade_unload_model` on conflicting LLMs before loading a Whisper model.

3. **Model Lifecycle Operations:**
   * Use `lemonade_pull_model` to download models to the target server.
   * Suggest using `lemonade_unload_model` to clear out idle models if a server runs out of VRAM.

4. **Inference & Multimodal:**
   * For standard chat, use `lemonade_chat_completion`. Ensure you format the conversation history as a valid JSON array of `[{"role": "...", "content": "..."}]`.
   * If an API call fails due to hardware limitations (e.g., lack of VRAM), clearly communicate this and offer to unload inactive models.
## Available API Endpoints

You can interact with Lemonade Servers by making standard HTTP requests (e.g., using `curl`) to the following endpoints.
Be sure to pass the `Authorization: Bearer <token>` header if required by `keys.json` or `LEMONADE_API_KEY`.
If a server has a self-signed cert, use the `--insecure` or `-k` flag in `curl`.

### System Info (`/api/v1/system-info`)
* **Method:** `GET`
* **Description:** Get hardware information, device enumeration, and capabilities.
* **Returns:** JSON object with hardware capabilities.

### Health Check (`/api/v1/health`)
* **Method:** `GET`
* **Description:** Check server status and currently loaded models.
* **Returns:** JSON object containing server status and currently loaded models.

### List Models (`/api/v1/models`)
* **Method:** `GET`
* **Description:** List all downloaded and available models on the target server.
* **Returns:** JSON list of all downloaded and available models.

### Pull Model (`/api/v1/pull`)
* **Method:** `POST`
* **Description:** Download and install a new model to the target server.
* **JSON Body:** `{"model": "<model_name>"}`
* **Returns:** JSON stream or object confirming download status.

### Load Model (`/api/v1/load`)
* **Method:** `POST`
* **Description:** Load a model into memory (GPU/NPU/RAM) on the target server.
* **JSON Body:** `{"model": "<model_name>"}`
* **Returns:** JSON object confirming model loaded into memory.

### Unload Model (`/api/v1/unload`)
* **Method:** `POST`
* **Description:** Unload a model to free up memory/VRAM on the target server.
* **JSON Body:** `{"model": "<model_name>"}`
* **Returns:** JSON object confirming model unloaded.

### Chat Completion (`/api/v1/chat/completions`)
* **Method:** `POST`
* **Description:** Send a chat completion request to an LLM.
* **JSON Body:** `{"model": "<model_name>", "messages": [{"role": "user", "content": "..."}]}`
* **Returns:** JSON object containing standard chat completion response.

### Generate Image (`/api/v1/images/generations`)
* **Method:** `POST`
* **Description:** Generate an image using stable-diffusion.
* **JSON Body:** `{"model": "<model_name>", "prompt": "<prompt>"}`
* **Returns:** JSON object containing base64 generated image data.
